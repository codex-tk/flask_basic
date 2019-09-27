from flask import request
from flask_restplus import Resource

from ..util.dto import AuthDto
from ..service.auth_service import Auth

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):

    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        data = request.json
        return Auth.login_user(data)


@api.route('/logout')
class UserLogout(Resource):

    @api.doc('user login')
    def post(self):
        data = request.headers.get('Authorization')
        return Auth.logout_user(data)
