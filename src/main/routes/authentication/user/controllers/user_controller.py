import os

from dotenv import load_dotenv

from datetime import timedelta

from cryptography.fernet import Fernet

from flask import Request, Response, make_response
from flask_jwt_extended import create_access_token

from starlette.status import (HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST,
                              HTTP_401_UNAUTHORIZED,
                              HTTP_406_NOT_ACCEPTABLE,
                              HTTP_500_INTERNAL_SERVER_ERROR)
from starlette.exceptions import HTTPException

from src.main.routes.authentication.user.vo.user_vo import UserVO
from src.main.routes.authentication.user.services.user_service import UserService


class UserController:

    def __init__(self):
        load_dotenv()
        self.fernet = Fernet(os.getenv('LANGFLOW_SECRET_KEY'))
        self.service = UserService()
        self.response = None

    async def create_user(self, request: Request) -> Response:
        if request.json is None:
            return make_response({'status_code': HTTP_404_NOT_FOUND, 'detail': 'Request body is missing'})
        else:
            body = request.json
            if body.get('password') != body.get('password_confirmation'):
                return make_response({'status_code': HTTP_406_NOT_ACCEPTABLE, 'detail':'Passwords do not match'})
            else:
                user = UserVO(name=body.get('name'), is_active=body.get('is_active'), username=body.get('username'),
                              password=self.fernet.encrypt(str(body.get('password')).encode()), email=body.get('email'))
                try:
                    user_vo = await self.service.create_user(user)
                    password = self.fernet.decrypt(str(user_vo.password)).decode()
                    self.response = make_response({'status_code': HTTP_201_CREATED,
                                                   'detail': 'User created successfully',
                                                   'content': {
                                                        'id': user_vo.id,
                                                        'name': user_vo.name,
                                                        'is_active': user_vo.is_active,
                                                        'username': user_vo.username,
                                                        'password': password.replace(password, len(password) * '*'),
                                                        'created_at': user_vo.created_at,
                                                        'updated_at': user_vo.updated_at
                                                   }})
                except Exception as httpException:
                    return make_response({'status_code':HTTP_500_INTERNAL_SERVER_ERROR,
                                          'detail': httpException.__cause__})
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
                if str(self.fernet.decrypt(current_user.password).decode()) == request.json.get('password'):
                    access_token = create_access_token(identity=current_user.username,
                                                       expires_delta=timedelta(minutes=30))
                    return make_response({'status_code': HTTP_202_ACCEPTED, 'authorization': f'Bearer {access_token}',
                                          'detail': 'Accepted'})

                else:
                    return make_response({'status_code': HTTP_401_UNAUTHORIZED, 'detail': 'Unauthorized'})
