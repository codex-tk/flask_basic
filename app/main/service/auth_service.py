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

    @staticmethod
    def get_logged_in_user(req):
        auth_token = req.headers.get('Authorization').split(" ")[1]
        if auth_token:
            user_id = User.decode_auth_token(auth_token)
            if not isinstance(user_id, str):
                user = User.query.filter_by(id=user_id).first()
                resp = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }
                return resp, 200
            else:
                err_msg = user_id
                resp = {
                    'status': 'fail',
                    'message': err_msg
                }
                return resp, 401
        else:
            resp = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return resp, 401
