from flask_restful import Resource
from flask import jsonify, request, make_response
from mongoengine.errors import DoesNotExist, NotUniqueError
from bson import ObjectId, json_util
from app.models import CodeSystem, ConceptGroup, Concept, Tag, ConceptVersion
from marshmallow import Schema, fields, ValidationError
import json
import traceback
import io
import pandas as pd
from collections import defaultdict
from app.controllers import CodeSystemController
from flask import current_app as app
import requests


class PostCodeSystemInputSchema(Schema):
    # team_id = fields.String(required=True)          # team id
    name = fields.String(required=True)
    # description of the version
    description = fields.String(required=False)

    file = fields.Field(required=True)              # file of the code system
    # version of the code system
    version = fields.String(required=True)


class GetCodeSystemInputSchema(Schema):
    version = fields.String(missing='latest')


class DeleteCodeSystemInputSchema(Schema):
    version = fields.String(required=True)


class CodeSystemResource(Resource):

   def get(self):
      """
        Get code system information and concepts.

        Returns:
            res (Response): HTTP Response
                - code (int): HTTP status code
                - msg (str): Message indicating the status
                - data (dict): Dictionary containing the code system details and concepts
                    - name (str): Name of the code system
                    - description (str): Description of the code system
                    - version (str): Version of the code system
                    - create_at (datetime): Timestamp of code system creation
                    - create_by (dict): Creator information
                    - groups (list): List of concept group details
                        - id (str): ID of the concept group
                        - name (str): Name of the concept group
                        - concepts (list): List of concept details
                            - id (str): ID of the concept
                            - name (str): Name of the concept
                            - description (str): Description of the concept
                            - update_at (datetime): Timestamp of concept update
                            - create_at (datetime): Timestamp of concept creation
        """

      try:
         in_schema = GetCodeSystemInputSchema().load(request.args)
      except ValidationError as err:
         return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
      

        if in_schema['version'] == 'latest':
            code_system = CodeSystem.objects(
                deleted=False).order_by('-create_at').first()
        else:
            code_system = CodeSystem.objects(
                version=in_schema['version'], deleted=False).first()

        if not code_system:
            return make_response(jsonify(code=404, err="INVALID_INPUT", msg="No code system found, please upload the latest UIL!"), 404)

        result = CodeSystemController.get_code_system_data(code_system)

        auth_url = app.config['AUTH_SERVICE_URL']
        res = requests.get(
            auth_url+'/user', params={'user_id': code_system.create_by})
        if res.status_code != 200:
            return make_response(jsonify(code=400, err="CREATER_NOT_FOUND", msg="The creater of this code system is not found in database"), 400)

        data = {
            'name': code_system.name,
            'description': code_system.description,
            'version': code_system.version,
            'create_at': code_system.create_at,
            'create_by': res.json()['data'],
            'groups': result
        }

        return make_response(jsonify(code=200, msg='ok', data=data))

    def post(self):
        """
        Create a new version of the code system.

        Returns:
            res (Response): HTTP Response
                - code (int): HTTP status code
                - msg (str): Message indicating the status
                - data (dict): Dictionary containing the newly created code system details
                    - code_system_id (str): ID of the code system
                    - name (str): Name of the code system
                    - version (str): Version of the code system
                    - description (str): Description of the code system
        """
        data = {}
        data.update(request.files)
        data.update(request.form)
        try:
            # Create new code system API input schema
            in_schema = PostCodeSystemInputSchema().load(data)

        except ValidationError as err:
            print(err)
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

        try:
            user_id = request.headers.get('User-ID')

            file = in_schema['file']
            if file.filename == '':
                return make_response(jsonify(code=400, err="FILE_NOT_FOUND", msg="File is not found!"), 400)
            if not file:
                return make_response(jsonify(code=400, err="NO_FILE", msg="No file is selected!"), 400)

            data = io.BytesIO(file.read())
            df = pd.read_excel(data)
            df.fillna('', inplace=True)

            code_system = CodeSystem(
                name=in_schema['name'],
                description=in_schema['description'],
                create_by=user_id,
                version=in_schema['version']
            )

            existing_concepts = {
                concept.name: concept for concept in Concept.objects().all()}
            existing_groups = {
                group.name: group for group in ConceptGroup.objects().all()}
            existing_tags = {(tag.name, tag.source): tag for tag in Tag.objects().all()}

            new_concepts = []
            new_groups = []
            new_tags = []
            new_concept_versions = []

            for _, row in df.iterrows():
                concept_name = str(row['Indication'])
                group_name = str(row['Groups'])
                alias = str(row['User alias']).strip()
                tag_names = [tag.strip() for tag in str(row['Tags']).split(
                    ',')] if str(row['Tags']).strip() != '' else []
                my_tag_names = [tag.strip() for tag in str(row['My tags']).split(
                    ',')] if str(row['My tags']).strip() != '' else []

                if row['Indication'] not in existing_concepts:
                    concept = Concept(name=concept_name)
                    new_concepts.append(concept)
                    existing_concepts[concept_name] = concept
                concept = existing_concepts[concept_name]

                if row['Groups'] not in existing_groups:
                    group = ConceptGroup(name=group_name)
                    new_groups.append(group)
                    existing_groups[group_name] = group
                group = existing_groups[group_name]

                tags = []
                for tag_name in tag_names + my_tag_names:
                    source = 'official' if tag_name not in my_tag_names else 'user'
                    if (tag_name, source) not in existing_tags:
                        tag = Tag(name=tag_name, source=source)
                        new_tags.append(tag)
                        existing_tags[(tag_name, source)] = tag
                    else:
                        tag = existing_tags[(tag_name, source)]
                    tags.append(tag)
                new_concept_versions.append(ConceptVersion(
                    code_system=code_system,
                    concept=concept,
                    alias=alias,
                    tags=tags,
                    group=group
                ))

            try:
                code_system.save()
                if len(new_concepts) > 0:
                    Concept.objects.insert(new_concepts, load_bulk=False)
                if len(new_groups) > 0:
                    ConceptGroup.objects.insert(new_groups, load_bulk=False)
                if len(new_tags) > 0:
                    Tag.objects.insert(new_tags, load_bulk=False)
                if len(new_concept_versions) > 0:
                    ConceptVersion.objects.insert(
                        new_concept_versions, load_bulk=False)
                return make_response(jsonify(code=200, msg='ok', data={'code_system_id': str(code_system.id),
                                                                       "name": code_system.name,
                                                                       "version": code_system.version,
                                                                       "description": code_system.description}), 200)

            except NotUniqueError as err:
                print(err)
                return make_response(jsonify(code=400, err="NOT_UNIQUE_ERROR", msg="Code system with this name or version already exists!"), 400)

        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

    def delete(self):
        try:
            in_schema = DeleteCodeSystemInputSchema().load(request.args)
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

   def delete(self):
        """
        Delete a code system version.

        Returns:
            res (Response): HTTP Response
                - code (int): HTTP status code
                - msg (str): Message indicating the status
                - data (dict): Dictionary containing the details of the deleted code system
                    - name (str): Name of the code system
                    - description (str): Description of the code system
                    - version (str): Version of the code system
                    - deleted (bool): Flag indicating if the code system is deleted
         """
        try:
             in_schema = DeleteCodeSystemInputSchema().load(request.args)
        except ValidationError as err:
            err
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        # Delete the codesystem given a unique version as input
        code_system = CodeSystem.objects(version=in_schema['version']).first()
        if not code_system:
            return make_response(jsonify(code=404, err="NOT_FOUND", msg="Code system version not found"))
        
        ConceptVersion.objects(code_system=code_system).delete()
        code_system.delete()

        data = {
            'name': code_system.name,
            'description': code_system.description,
            'version': code_system.version,
            'deleted': code_system.deleted
        }
        return make_response(jsonify(code=200, msg='ok', data=data), 200)
