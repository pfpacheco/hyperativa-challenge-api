from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from starlette.exceptions import HTTPException
from starlette.status import HTTP_405_METHOD_NOT_ALLOWED

from src.main.routes.authentication.user.controllers.user_controller import UserController

route = Blueprint('user', __name__)


@route.route('/rest/api/v1/create_user', methods=['POST'])
@jwt_required()
async def create_user():
    if request.method == 'POST':
        controller: UserController = UserController()
        return await controller.create_user(request=request)
    else:
        return HTTPException(status_code=HTTP_405_METHOD_NOT_ALLOWED, detail='Method Not Allowed')


@route.route('/rest/api/v1/login', methods=['POST'])
async def login():
    if request.method == 'POST':
        controller: UserController = UserController()
        return await controller.process_login(request=request)
    else:
        return HTTPException(status_code=HTTP_405_METHOD_NOT_ALLOWED, detail='Method Not Allowed')
