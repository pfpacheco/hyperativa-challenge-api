from flask import request
from flask.blueprints import Blueprint
from flask_jwt_extended import jwt_required

from starlette.status import HTTP_405_METHOD_NOT_ALLOWED, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.exceptions import HTTPException

from src.main.routes.credit_card.controllers.credit_card_controller import CreditCardController

route = Blueprint('credit_card', __name__)


@route.route('/rest/api/v1/credit_card', methods=['POST'])
@jwt_required()
async def credit_card():
    if request.method == 'POST':
        controller: CreditCardController = CreditCardController()
        if 'application/json' in request.headers['Content-Type']:
            return await controller.process_request(request=request)
        elif 'multipart/form-data' in request.headers['Content-Type']:
            return await controller.process_file(request=request)
        else:
            return HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail='This header is invalid')
    else:
        return HTTPException(status_code=HTTP_405_METHOD_NOT_ALLOWED, detail='Method Not Allowed')


@route.route('/rest/api/v1/credit_card/<header_id>/', methods=['GET'])
@jwt_required()
async def get_credit_card(header_id: int):
    if request.method == 'GET':
        controller: CreditCardController = CreditCardController()
        return await controller.find_credit_card(header_id=header_id)
    else:
        return HTTPException(status_code=HTTP_405_METHOD_NOT_ALLOWED, detail='Method Not Allowed')
