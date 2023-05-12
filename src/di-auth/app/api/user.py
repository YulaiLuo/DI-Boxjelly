from datetime import datetime
from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError, validates_schema, validate
from app.models import Team, UserTeam, User
from bson import ObjectId
from flask import request, make_response, jsonify
from mongoengine.errors import DoesNotExist

class UserSchema(Schema):
    """
    A class to represent a User Schema, used to validate the input data
    The input should contain first name, last name, and gender fields.

class PutUserInputSchema(Schema):
    # avatar = StringField(required=True)
    first_name = fields.String(required=False,min_len=1)
    last_name = fields.String(required=False,min_len=1)
    nickname = fields.String(required=False,min_len=1)
    gender = fields.String(required=False,validate=validate.OneOf(['male','female','other']))                              # group name
    @validates_schema
    def validate_not_empty(self, data, **kwargs):
        if not data:
            raise ValidationError("EMPTY_REQUEST")
            
class UserResource(Resource):

    def put(self):
        """Update the user profile
        """
        try:
            in_schema = PutUserInputSchema()
            in_schema = in_schema.load(request.get_json())
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

        # TODO: Get user id from token
        user_id = "645da08427eb73c12b252cef"

        try:
            # Update the user's profile
            User.objects(id=user_id).update_one(**in_schema)           
            updated_user = User.objects(id=user_id).first()
        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)
        data = {
            'user_id':str(updated_user.id),
            'name': f'{updated_user.first_name} {updated_user.last_name}',
            'nickname': updated_user.nickname,
            'email':updated_user.email,
            'gender':updated_user.gender
        }
        return make_response(jsonify(code=200, msg="ok", data=data), 200)

    def get(self):
        """Get user profile
        """
        User log in 

        Args:
        email (str): the email of the user
        password (str): the original password(unhashed) of the user

        Returns:
            Response: HTTP Response

        Raises:
            ValidationError: If the input data is invalid
            OperationFailure: If the database operation failed

        Example:
            >>> url = <login_url>
            >>> payload = {'email': 'example@email.com', 'password': 'mypassword'}
            >>> headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            >>> requests.post(url, data=payload, headers=headers)
            {'code': 200, 'msg': 'success'} with status code 200, and set the access token and refresh token in the cookies

            >>> url = <login_url>
            >>> payload = {'email': 'example', 'password': 'mypassword'}
            >>> headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            >>> requests.post(url, data=payload, headers=headers)
            {'code': 400, 'msg': 'INVALID_EMAIL_PASSWORD'} with status code 400

            >>> url = <login_url>
            >>> payload = {'email': 'correct@email.com', 'password': 'incorrect_password'}
            >>> headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            >>> requests.post(url, data=payload, headers=headers)
            {'code': 401, 'msg': 'INCORRECT_PASSWORD'} with status code 401

            >>> url = <login_url>
            >>> payload = {'email': 'user_not_exist@email.com', 'password': 'correct_password'}
            >>> headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            >>> requests.post(url, data=payload, headers=headers)
            {'code': 404, 'msg': 'USER_NOT_FOUND'} with status code 404
        """

        # Validate the input data
        try:
            data = request.form
            register_data = UserSchema().load(data)
        except ValidationError:
            response = jsonify(code=400,err="INVALID_DATA")
            response.status_code = 400
            return response

        # Get the email and password from the request
        email = register_data['email']
        password = register_data['password']

        firstName =  register_data['firstName']
        lastName = register_data['lastName']
        gender = register_data['gender']
        
        # Verify if the URL is valid and not expired
        token = request.args.get('token')
        if not token:
            response = jsonify(code=400, err="INVALID_TOKEN")
            response.status_code = 400
            return response
        
        try:
            # TODO: Get user id from header token 
            # to check if the requester is in the team
            user_id = '645da08427eb73c12b252cef'

            user = User.objects(id=in_schema['user_id']).first()
            if not user:
                return make_response(jsonify(code=404, err="USER_NOT_FOUND"), 404)
            data = {
                'user_id':str(user.id),
                'name': f'{user.first_name} {user.last_name}',
                'nickname': user.nickname,
                'email':user.email,
                'gender':user.gender
            }
            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

        

        # If the user is found and the password is correct, we start the transaction to update the last login time
        try:
            with self.mongo.cx.start_session() as session:
                with session.start_transaction():
                    
                    # Insert the user data
                    self.mongo.db.users.insert_one({
                        'email': email,
                        'password': password,
                        'firstName': firstName,
                        'lastName': lastName,
                        'gender': gender,
                        'created_at': datetime.utcnow()
                    })
                    # Create access and refresh tokens
                    access_token = create_access_token(identity=email)
                    refresh_token = create_refresh_token(identity=email)

                    # Set the JWT cookies in the response
                    response = jsonify(code=200,msg='ok')
                    set_access_cookies(response, access_token)
                    set_refresh_cookies(response, refresh_token)

                    response.status_code = 200
                    return response

        except OperationFailure as e:
            response = jsonify(code=500, err="DATABASE_ERROR")
            response.status_code = 500
            return response


                    # If user exist, password is correct and update success, return 200 status code 
        #             response = jsonify(code=200,msg='ok')

        #             # Set the JWT cookies in the response
        #             set_access_cookies(response, access_token)
        #             set_refresh_cookies(response, refresh_token)

        #             response.status_code = 200
        #             return response
        # except OperationFailure:
        #     response = jsonify(code=400,err="TRANSACTION_FAILED")
        #     response.status_code = 400
        #     return response