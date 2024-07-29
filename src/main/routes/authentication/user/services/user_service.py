from database.db import SessionLocal

from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from starlette.exceptions import HTTPException

from routes.authentication.user.vo.user_vo import UserVO
from routes.authentication.user.models.user_model import UserModel


class UserService:

    def __init__(self):
        self.db = SessionLocal()

    async def create_user(self, user: UserVO) -> UserVO:
        try:
            if user is None:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='User Not Found')
            else:
                model = UserModel(name=user.name, is_active=user.is_active, username=user.username,
                                  password=user.password)
                self.db.add(model)
                self.db.commit()
                self.db.refresh(model)
                user = UserVO(id=model.id, name=model.name, is_active=model.is_active, username=model.username,
                              password=model.password, created_at=model.created_at, updated_at=model.updated_at)
        except Exception as httpException:
            self.db.rollback()
            raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=str(httpException))
        finally:
            self.db.flush()
        return user

    async def find_user_by_username(self, username: str) -> UserVO:
        try:
            if username is None:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Username Not Found')
            else:
                user_vo = self.db.query(UserModel).filter(UserModel.username == username).one_or_none()
                if user_vo is None:
                    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='User not found')
                else:
                    return user_vo
        except Exception as httpException:
            raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=str(httpException))
        finally:
            self.db.flush()
