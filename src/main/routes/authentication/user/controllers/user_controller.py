from datetime import timedelta

from flask import Request, Response, make_response
from flask_jwt_extended import create_access_token

from starlette.status import (HTTP_202_ACCEPTED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
                              HTTP_406_NOT_ACCEPTABLE,
                              HTTP_500_INTERNAL_SERVER_ERROR)
from starlette.exceptions import HTTPException

from src.main.routes.authentication.user.vo.user_vo import UserVO
from src.main.routes.authentication.user.services.user_service import UserService


class UserController:

    def __init__(self):
        self.service = UserService()
        self.response = None

    async def create_user(self, request: Request) -> Response:
        if request.json is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Request body is missing')
        else:
            body = request.json
            if body.get('password') != body.get('password_confirmation'):
                raise HTTPException(status_code=HTTP_406_NOT_ACCEPTABLE, detail='Passwords do not match')
            else:
                user = UserVO(name=body.get('name'), is_active=body.get('is_active'), username=body.get('username'),
                              password=body.get('password'), email=body.get('email'))
                try:
                    user_vo = await self.service.create_user(user)
                    self.response = make_response(
                        {
                            'id': user_vo.id,
                            'name': user_vo.name,
                            'is_active': user_vo.is_active,
                            'username': user_vo.username,
                            'password': user_vo.password.replace(user_vo.password, len(user_vo.password) * '*'),
                            'created_at': user_vo.created_at,
                            'updated_at': user_vo.updated_at,
                        }
                    )
                except Exception as httpException:
                    raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(httpException))
        return self.response

    async def process_login(self, request: Request) -> Response:
        if request.json.get('username') is None or request.json.get('username') == '':
            return make_response({'status_code': HTTP_400_BAD_REQUEST, 'detail': 'Username is missing'})
        elif request.json.get('password') is None or request.json.get('password') == '':
            return make_response({'status_code': HTTP_400_BAD_REQUEST, 'detail': 'Password is missing'})
        else:
            current_user = await self.service.find_user_by_username(username=request.json.get('username'))
            if current_user is None:
                return make_response({'status_code': HTTP_404_NOT_FOUND, 'detail': 'Not found'})
            else:
                if current_user.password == request.json.get('password'):
                    access_token = create_access_token(identity=current_user.username,
                                                       expires_delta=timedelta(minutes=30))
                    return make_response({'status_code': HTTP_202_ACCEPTED, 'authorization': f'Bearer {access_token}',
                                          'detail': 'Accepted'})

                else:
                    return make_response({'status_code': HTTP_401_UNAUTHORIZED, 'detail': 'Unauthorized'})
