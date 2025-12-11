
from beanie import Document
from beanie import before_event, Insert
import bcrypt
import jwt
import os
from dotenv import load_dotenv
load_dotenv()
    
class User(Document):
    name: str
    email: str
    password: str

    @before_event(Insert)
    def hash_password_before_save(self):
       if not self.password.startswith("$2b$"):
           self.password = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    def check_password(password: str, plain_password: str) -> bool:
        return bcrypt.checkpw(password=plain_password.encode("utf-8"), hashed_password=password.encode("utf-8"))
    
    def genjwttoken( payload):
        return jwt.encode(payload, key="secret" ,algorithm="HS256" )
    
   