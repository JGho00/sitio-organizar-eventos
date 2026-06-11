from pydantic import BaseModel

class User(BaseModel):

    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


usuarios_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "12345",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "12345",
        "disabled": True,
    },
    "jose": {
        "username": "jose",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "12345",
        "disabled": True,
    },
}


