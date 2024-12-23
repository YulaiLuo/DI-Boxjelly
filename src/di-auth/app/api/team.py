from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError
from app.models import Team, UserTeam, User
from bson import ObjectId
from flask import request, make_response, jsonify


class PostTeamInputSchema(Schema):
    name = fields.String(required=True)                         # team name
    # emails of the team members
    emails = fields.List(fields.Email(), required=False)
    # uli_file = fields.File(required=True)                     # uli file of the team members
    first_board_name = fields.String(required=False)            # board name
    first_board_description = fields.String(
        required=False)     # board description


class GetTeamInputSchema(Schema):
    team_id = fields.String(required=True)


class PutTeamInputSchema(Schema):
    team_id = fields.String(required=True)
    new_name = fields.String(required=True)


class DeleteTeamInputSchema(Schema):
    team_id = fields.String(required=True)
    user_id = fields.String(required=True)


class PostTransferOwnerInputSchema(Schema):
    team_id = fields.String(required=True)
    new_owner_id = fields.String(required=True)


def convert_objectid_to_str(data):
    for key, value in data.items():
        if isinstance(value, ObjectId):
            data[key] = str(value)
    return data


class TeamResource(Resource):

    def get(self):
        """
        Get all active status team members and information.

        Args:
            team_id (str): The ID of the team.

        Returns:
            res (Response): HTTP Response
                - code (int): HTTP status code
                - msg (str): Message indicating the status
                - data (dict): Dictionary containing the team and member details
                    - team_id (str): The ID of the team
                    - team_name (str): The name of the team
                    - members (list): List of member details
                        - user_id (str): The ID of the user
                        - username (str): The username of the user
                        - first_name (str): The first name of the user
                        - last_name (str): The last name of the user
                        - nickname (str): The nickname of the user
                        - email (str): The email of the user
                        - gender (str): The gender of the user
                        - avatar (str): The avatar of the user
                        - role (str): The role of the user in the team
        """
        try:
            in_schema = GetTeamInputSchema()
            in_schema = in_schema.load(request.args)
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

        try:
            team = Team.objects(id=ObjectId(in_schema['team_id'])).first()
            if not team:
                return make_response(jsonify(code=404, err="TEAM_NOT_FOUND"), 404)

            pipeline = [
                {"$match": {"team_id": ObjectId(
                    in_schema['team_id']), "status": "active"}},
                {"$lookup": {
                    "from": "user",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user_info"
                }},
                {"$unwind": "$user_info"},
                {"$project": {
                    "_id": 0,  # exclude _id field
                    "user_id": "$user_info._id",
                    "username": "$user_info.username",
                    "first_name": "$user_info.first_name",
                    "last_name": "$user_info.last_name",
                    "nickname": "$user_info.nickname",
                    "email": "$user_info.email",
                    "gender": "$user_info.gender",
                    "avatar": "$user_info.avatar",
                    "role": "$role",
                    "status": "$status"
                }}
            ]
            members = list(UserTeam.objects.aggregate(*pipeline))
            members = [convert_objectid_to_str(member) for member in members]
            data = {
                "team_id": str(team.id),
                "team_name": team.name,
                "members": members
            }

            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

    def put(self):
        """
        Update the team name.

        Args:
            team_id (str): The ID of the team.
            new_name (str): The new name for the team.

        Returns:
            res (Response): HTTP Response
                - code (int): HTTP status code
                - msg (str): Message indicating the status
                - data (dict): Dictionary containing the updated team details
                    - id (str): The ID of the team
                    - name (str): The updated name of the team
        """
        try:
            in_schema = PutTeamInputSchema()
            in_schema = in_schema.load(request.get_json())
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

        try:

            team = Team.objects(id=ObjectId(in_schema['team_id'])).first()
            if not team:
                return make_response(jsonify(code=404, err="TEAM_NOT_FOUND"), 404)

            team.name = in_schema['new_name']
            team.save()
            data = {
                "id": str(team.id),
                "name": team.name,
            }
            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)


class TeamMemberResource(Resource):

    def delete(self):
        """
        Delete a team member.

        Args:
        team_id (str): The ID of the team.
        user_id (str): The ID of the user to be deleted.

        Returns:
            res (Response): HTTP Response
                - code (int): HTTP status code
                - msg (str): Message indicating the status
        """
        try:
            in_schema = DeleteTeamInputSchema().load(request.args)
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

        try:
            user_id = request.headers.get('User-ID')
            requester = UserTeam.objects(user_id=ObjectId(user_id)).first()

            if requester.role != "owner":
                return make_response(jsonify(code=403, err="FORBIDDEN"), 403)

            team = Team.objects(id=ObjectId(in_schema['team_id'])).first()
            if not team:
                return make_response(jsonify(code=404, err="TEAM_NOT_FOUND"), 404)

            user_team = UserTeam.objects(user_id=ObjectId(
                in_schema['user_id']), team_id=ObjectId(in_schema['team_id'])).first()
            if not user_team:
                return make_response(jsonify(code=404, err="USER_NOT_FOUND"), 404)

            user = User.objects(id=ObjectId(in_schema['user_id'])).first()
            if not user:
                return make_response(jsonify(code=404, err="USER_NOT_FOUND"), 404)

            user.delete()
            user_team.delete()

            return make_response(jsonify(code=200, msg="ok"), 200)
        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)


class TransferOwnerResource(Resource):

    def post(self):

        """
        Transfer the ownership of a team to a new owner.

        Args:
            team_id (str): The ID of the team.
            new_owner_id (str): The ID of the new owner.

        Returns:
            res (Response): HTTP Response
                - code (int): HTTP status code
                - msg (str): Message indicating the status
                - data (dict): Dictionary containing the updated roles of the users
        """
        
        try:
            in_schema = PostTransferOwnerInputSchema().load(request.get_json())
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

        try:
            user_id = request.headers.get('User-ID')
            requester = UserTeam.objects(id=ObjectId(user_id)).first()
            if requester.role != "owner":
                return make_response(jsonify(code=403, err="FORBIDDEN"), 403)

            new_owner = UserTeam.objects(user_id=ObjectId(in_schema['new_owner_id']),
                                         team_id=ObjectId(in_schema['team_id'])).first()

            if not new_owner:
                return make_response(jsonify(code=404, err="USER_NOT_FOUND"), 404)

            # set up roles
            requester.role = "member"
            requester.save()
            new_owner.role = "owner"
            new_owner.save()

        except Exception as err:
            # rollback
            requester.role = "owner"
            requester.save()
            new_owner.role = "member"
            new_owner.save()
