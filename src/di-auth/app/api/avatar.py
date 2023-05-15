from flask_restful import Resource
from flask import send_from_directory, request, make_response, jsonify
from marshmallow import Schema, fields, ValidationError, post_load, validate, validates, validates_schema
from PIL import Image
from mongoengine.errors import DoesNotExist
from app.models import User
import os, hashlib, time
from flask import current_app as app

class GetAvatarInputSchema(Schema):
    avatar = fields.String(required=True)

class PostAvatarInputSchema(Schema):
    new_avatar = fields.Field(required=True)

class AvatarResource(Resource):

    def post(self):
        """Upload the avatar
        """
        try:
            in_schema = PostAvatarInputSchema()
            in_schema = in_schema.load(request.files)
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        # Check if the image exits in request
        file = in_schema['new_avatar']
        if file.filename == '':
            return make_response(jsonify(code=400, err="NO_SELECTED_FILE"), 400)

        # check if the file is an image
        try:
            Image.open(file)
        except IOError as err:
            return make_response(jsonify(code=400, err="NOT_IMAGE_ERROR"), 400)
        
        # Check image size is smaller than 1MB
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        if file_size > 1024*1024:
            return make_response(jsonify(code=400, err="FILE_TOO_LARGE"), 400)
        
        # Find the user
        user_id = '645deb4a2a296fec6af44411'
        try:
            user = User.objects(id=user_id).first()
        except DoesNotExist as err:
            return make_response(jsonify(code=400, err="USER_NOT_EXIST"), 400)

        # Generate the file name and save the avatar
        try:
            # Save the avatar in directory
            file.seek(0)
            hash_object = hashlib.sha1(file.read())
            hex_dig = hash_object.hexdigest()
            filename = f'{hex_dig[:8]}{int(time.time())}'
            
            file.seek(0)
            img = Image.open(file)
            img = img.convert('RGB')
            img.thumbnail((128,128))
            old_avatar = user.avatar
            user.avatar = filename

            # Save the new avatar, remove old avatar, and update user avatar field
            try:
                os.remove(os.path.join(app.config['AVATAR_FOLDER'], f"{old_avatar}.jpg"))
            except FileNotFoundError as err:
                pass

            img.save(os.path.join(app.config['AVATAR_FOLDER'],f'{filename}.jpg'),'JPEG')
            user.save()
            return make_response(jsonify(code=200, msg="ok", data={'avatar': filename}), 200)

        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)
        
        
    def get(self):
        """send the avatar
        """
        try:
            in_schema = GetAvatarInputSchema().load(request.args)
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            avatar = in_schema['avatar']
            return send_from_directory(app.config['AVATAR_FOLDER'], f'{avatar}.jpg')
        except Exception as err:
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)
        