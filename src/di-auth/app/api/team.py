from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError
from app.models import Team, UserTeam
from bson import ObjectId
from flask import request, make_response, jsonify

class PostTeamInputSchema(Schema):
    name = fields.String(required=True)                  # team id

class GetTeamInputSchema(Schema):
    team_id = fields.String(required=True)

class PutTeamInputSchema(Schema):
    team_id = fields.String(required=True)
    new_name = fields.String(required=True)

class TeamResource(Resource):

    def post(self):
        """Create a new team and add the creator as the team member
        """
        try:
            in_schema = PostTeamInputSchema()
            in_schema = in_schema.load(request.get_json())
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            # TODO: Get user id from header token
            user_id = "645a59c3052f3ebedab52d78"

            new_team = Team(name=in_schema['name'],
                            create_by=ObjectId(user_id),
            )
            new_team.save()

            new_user_team = UserTeam(user_id=ObjectId(user_id),
                                 team_id=new_team.id,
                                 role="owner")
            new_user_team.save()
            data = {
                'team_id':str(new_team.id),
                'name':new_team.name
            }
            return make_response(jsonify(code=200, msg="ok", data=data), 200)

        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)
        

    def get(self):
        """Get team members and informations
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
                {"$match": {"team_id": ObjectId(in_schema['team_id']), "status": "valid"}},
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
                    "email": "$user_info.email",
                    "gender": "$user_info.gender",
                    "role": "$role",
                    "status": "$status"
                }}
            ]
            users = list(UserTeam.objects.aggregate(*pipeline))
            data = {
                "team_id": str(team.id),
                "team_name": team.name,
                "users": users
            }

            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)


    def put(self):
        """Update the team name
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
        