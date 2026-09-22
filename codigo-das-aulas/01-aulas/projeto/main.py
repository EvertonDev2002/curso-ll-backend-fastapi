from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from schema import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá, mundo!"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(
        **user.model_dump(),
        id=len(database) + 1,
    )

    database.append(user_with_id)

    return user_with_id


@app.get("/users/", status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {"users": database}


@app.put("/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    print(f'tamanho do banco: {len(database)}')
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado"
        )

    user_with_id = UserDB(email=user.email, username=user.username, id=user_id)

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete("/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado"
        )
    return database.pop(user_id - 1)
