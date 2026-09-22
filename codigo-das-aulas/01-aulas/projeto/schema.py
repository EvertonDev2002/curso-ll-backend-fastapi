from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


# entrada
class UserSchema(BaseModel):
    username: str
    email: EmailStr


# saída
class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int


class UserDB(UserSchema):
    id: int


# saída
class UserList(BaseModel):
    users: list[UserPublic]
