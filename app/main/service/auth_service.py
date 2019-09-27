from app.main.model.user import User
from app.main.service.blacklist_service import save_token


class Auth:

    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.id)
                if auth_token:
                    return {
                               'status': 'success',
                               'message': 'Successfully logged in.',
                               'Authorization': auth_token.decode()
                           }, 200
            else:
                return {
                           'status': 'fail',
                           'message': 'Email or Password does not match',
                       }, 401
        except Exception as e:
            print(e)
            return {
                       'status': 'fail',
                       'message': 'try again',
                   }, 500

    @staticmethod
    def logout_user(data):
        try:
            if data:
                auth_token = data.split(" ")[1]
            else:
                auth_token = None
            if auth_token:
                resp = User.decode_auth_token(auth_token)
                if not isinstance(resp, str):
                    return save_token(auth_token)
                else:
                    return {'status': 'fail', 'message': resp}, 401
            else:
                return {'status': 'fail', 'message': 'invalid token'}, 403
        except Exception as e:
            print(e)
            return {
                       'status': 'fail',
                       'message': 'try again',
                   }, 500
