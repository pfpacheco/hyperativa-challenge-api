from typing import List

from flask import Request, make_response, Response
from starlette.exceptions import HTTPException
from starlette.status import (HTTP_302_FOUND, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR,
                              HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)

from src.main.routes.credit_card.services.credit_card_service import CreditCardService
from src.main.routes.credit_card.vo.creditcard_vo import HeaderVO, ItemVO


class CreditCardController:

    def __init__(self):
        self.service = CreditCardService()

    async def process_request(self, request: Request) -> Response:
        if request.json:
            body = request.json
            item = ItemVO(line=body.get('line'), batch_number=body.get('batch_number'),
                          credit_card_number=body.get('credit_card_number'))
            header = HeaderVO(name=body.get('name'), date=body.get('date'), batch_name=body.get('batch_name'),
                              registers=body.get('registers'))
            try:
                header_vo = await self.create_header(header_vo=header)
                item_vo = await self.create_item(header_id=header_vo.id, item_vo=item)

                response = self.process_response(header=header_vo, item=item_vo)

                return make_response(
                    {
                        'code': HTTP_201_CREATED,
                        'status': 'CREATED',
                        'content': response
                    })

            except Exception as e:
                raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def process_file(self, request: Request) -> Response:
        file = request.files.get('flat_data')
        if not file:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='No file provided')

        try:
            # Read and decode the file content
            lines = file.read().decode('utf-8').splitlines()
            if not lines:
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Bad Request')

            header_vo = None
            responses: List[{}] = []

            for i in range(0, len(lines)):

                if lines[i][0:1].isalpha():
                    # Process the headers
                    header = HeaderVO(
                        name=lines[i][0:28],
                        date=lines[i][29:37],
                        batch_name=lines[i][37:45],
                        registers=lines[i][49:51]
                    )
                    header_vo = await self.create_header(header_vo=header)
                else:
                    # Process the items
                    item = ItemVO(
                        line=lines[i][0:1],
                        batch_number=lines[i][1:7],
                        credit_card_number=lines[i][7:26]
                    )
                    item_vo = await self.create_item(header_id=header_vo.id, item_vo=item)
                    responses.append(self.process_response(header=header_vo, item=item_vo))
            return make_response({
                'code': HTTP_201_CREATED,
                'status': 'CREATED',
                'content': responses
            })

        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            file.close()

    async def find_credit_card(self, credit_card_number: str) -> Response:
        try:
            if credit_card_number:
                item = await self.service.find_by_credit_card_number(credit_card_number)
                if item.header_id is not None:
                    header = await self.service.find_by_header_id(item.header_id)
                    if header.name is not None:
                        return make_response({
                            'code': HTTP_302_FOUND,
                            'status': 'FOUND',
                            'content': {
                                'card_holder_name': header.name,
                                'card_masked_number': await self.mask_credit_card(item),
                                'is_active': True
                            }
                        })
                    else:
                        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Name Not Found')
                else:
                    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Credit Card Number Not Found')
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return

    @staticmethod
    async def mask_credit_card(item):
        return item.credit_card_number[0:4] + '-' + 4 * 'X' + '-' + 4 * 'X' + '-' + item.credit_card_number[12:16]

    @staticmethod
    def process_response(header, item):
        response = {
            'id': header.id,
            'name': header.name,
            'date': header.date,
            'batch_name': header.batch_name,
            'registers': header.registers,
            'item': {
                'item_id': item.id,
                'line': item.line,
                'batch_number': item.batch_number,
                'credit_card_number': item.credit_card_number,
            },
            'created_at': header.created_at,
            'updated_at': header.updated_at,
        }
        return response

    async def create_header(self, header_vo: HeaderVO) -> HeaderVO:
        new_header = await self.service.create_new_header(header=header_vo)
        return new_header

    async def create_item(self, header_id: int, item_vo: ItemVO) -> ItemVO:
        new_item = await self.service.create_new_item(header_id=header_id, item=item_vo)
        return new_item
