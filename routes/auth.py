from fastapi import APIRouter,Depends,Response
from controlar.usercontrolar import signup ,signin,view_profile
router = APIRouter()
from utility.validation import UserSignupdata ,UserLoginData
from middleware.authorized import authorized
@router.get("/")
async def root(): return {"message": "Hello World"}
@router.post("/signup")
async def register(data: UserSignupdata): return await signup(data)

@router.post("/login")
async def login(data:UserLoginData ,response:Response): return await signin(data ,response)

@router.get("/profile")
async def profile(user: str = Depends(authorized)): return await view_profile(user)