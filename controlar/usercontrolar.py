
from model.usermodle import User
from utility.validation import UserSignupdata ,UserLoginData
from fastapi import HTTPException
from fastapi import Response
async def signup(data:UserSignupdata):
    try:
       is_exist = await User.find_one(User.email == data.email)
       print("is_exist",is_exist)
       if is_exist:
           print("Email already exists")
           raise HTTPException(status_code=400, detail="Email already exists")
           return
    
       print("user creating")
       new_user = await User(name=data.name,email=data.email,password=data.password ).create()
       return {"message":f"user created successfully {new_user}"}
    except Exception as e:
        print("erro to signup ",)
        raise HTTPException(status_code=400, detail=f"error to signup {e}")
    

async def signin(data: UserLoginData, response: Response):
    try:
        is_exist = await User.find_one(User.email == data.email)
        if not is_exist:
            print("user is not found")
            raise HTTPException(status_code=400, detail="user not found")
        is_verify = User.check_password(is_exist.password, data.password)
        if not is_verify:
            print("email or password is incorrect")
            raise HTTPException(status_code=401, detail="email or password is incorrect")
        jwt = User.genjwttoken({"email": data.email})
        # Set the JWT token as a cookie
        response.set_cookie(key="access_token", value=jwt, httponly=True, samesite="lax")
        return {"token": jwt}
    except Exception as e:
        print(f"error to login {e}")
        raise HTTPException(status_code=400, detail=f"error to login {e}")
    
async def view_profile (user):
    try:
        if not user:
            raise HTTPException(status_code=400, detail="user not found")
        profile_user = await User.find_one(User.email == user)
        if profile_user :return profile_user
        else:raise HTTPException(status_code=400, detail="user not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"error to view profile {e}")