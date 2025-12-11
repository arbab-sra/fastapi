from pydantic import BaseModel
class UserSignupdata (BaseModel):
    name: str
    email: str
    password: str

class UserLoginData (BaseModel):
    email: str
    password: str