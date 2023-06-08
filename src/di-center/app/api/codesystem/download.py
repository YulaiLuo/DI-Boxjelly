from flask_restful import Resource
from flask import jsonify, request, make_response, Response
from marshmallow import Schema, fields, ValidationError, validates
from bson import ObjectId
from app.models import CodeSystem, Concept, ConceptGroup
from mongoengine.errors import DoesNotExist, NotUniqueError, MultipleObjectsReturned
import pandas as pd
from app.controllers import CodeSystemController
from io import BytesIO
import xlsxwriter


class DownloadCodeSystemResource(Resource):

   def get(self, version):
      """
      Download the code system given a version.

      Args:
         version (str): The version of the code system.

      Returns:
         response (Response): HTTP Response containing the code system data as an Excel file attachment.
      """
      
      code_system = CodeSystem.objects(version=version).first()
      if not code_system:
         return make_response(jsonify(code=404, err="INVALID_INPUT"), 404)

      groups = CodeSystemController.get_code_system_data(code_system)

      flat_data = []
      for group in groups:
         group_name = group['group_name']
         concept_versions = group['concept_versions']

         for cv in concept_versions:
            flat_data.append({
                  'group_name': group_name,
                  'concept_name': cv['concept_name'],
                  'alias': cv['alias'],
                  'tags': ', '.join(cv['tags']),
                  'my_tags': ', '.join(cv['my_tags']),
            })

      # Create a ByteIO object
      output = BytesIO()

      with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
         df = pd.DataFrame(flat_data)
         df.to_excel(writer, sheet_name='Sheet1', index=False)

      output.seek(0)

      response = Response(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
      response.headers.set('Content-Disposition', 'attachment', filename=f"{code_system.name}-{code_system.version}.xlsx")
   
      return response

      

