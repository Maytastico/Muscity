from flask_login.utils import login_fresh
from flask_restful import Resource
from flask_jwt_extended import jwt_required


class TitlesList(Resource):
    @jwt_required
    def get(self):
        return {'audio':'Geil!'}

class Titles(Resource):
    def get(self, id):
        return {'audio':'Super Geil!'}

    def put(self, id):
        return {'audio':'modified'}

    def delete(self, id):
        return {'audio':'deleted'}