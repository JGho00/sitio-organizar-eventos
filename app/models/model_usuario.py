from sqlmodel import SQLModel, Field

class Usuario(SQLModel,table = True):
    id_usuario:int|None = Field(primary_key=True)
    username:str = Field()
    email:str = Field()
    password_hash:str = Field()
    rol :str = Field()