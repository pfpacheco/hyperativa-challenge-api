from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from src.main.database.db import SessionLocal

from src.main.routes.credit_card.vo.creditcard_vo import HeaderVO, ItemVO
from src.main.routes.credit_card.models.credit_card_model import HeaderModel, ItemModel


class CreditCardService:
    def __init__(self):
        self.db = SessionLocal()

    async def create_new_header(self, header: HeaderVO) -> HeaderVO:
        try:
            if header is None:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Header not found')
            else:
                model = HeaderModel(name=header.name.rstrip(), date=header.date,
                                    batch_name=header.batch_name, registers=header.registers)
                self.db.add(model)
                self.db.commit()
                self.db.refresh(model)
                header = HeaderVO(id=model.id, name=model.name.rstrip(), date=header.date, batch_name=model.batch_name,
                                  registers=model.registers, created_at=model.created_at,
                                  updated_at=model.updated_at)
        except Exception as httpException:
            self.db.rollback()
            raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=str(httpException))
        finally:
            self.db.flush()
        return header

    async def create_new_item(self, header_id: int,  item: ItemVO) -> ItemVO:
        try:
            if item is None:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Item not found')
            else:
                model = ItemModel(header_id=header_id, line=item.line, batch_number=item.batch_number,
                                  credit_card_number=item.credit_card_number)
                self.db.add(model)
                self.db.commit()
                self.db.refresh(model)
                item = ItemVO(id=model.id, header_id=model.header_id, line=item.line,
                              batch_number=item.batch_number, credit_card_number=item.credit_card_number,
                              created_at=model.created_at, updated_at=model.updated_at)
        except Exception as httpException:
            self.db.rollback()
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(httpException))
        finally:
            self.db.flush()
        return item

    async def find_credit_card_by_header_id(self, header_id: int) -> ItemVO:
        try:
            if header_id is None:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Credit Card Number not found')
            else:
                items_vo = self.db.query(ItemModel).filter(ItemModel.header_id == header_id).all()
                return items_vo
        except Exception as httpException:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(httpException))
        finally:
            self.db.flush()

    async def find_by_header_id(self, header_id: int) -> HeaderVO:
        try:
            if header_id is None:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Header id not found')
            else:
                header_vo = self.db.query(HeaderModel).filter(HeaderModel.id == header_id).first()
                return header_vo
        except Exception as httpException:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(httpException))
        finally:
            self.db.flush()
