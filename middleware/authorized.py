from fastapi import Request , HTTPException
import jwt

async def authorized( request: Request):
    try:
        token =  request.headers.get("Authorization") or request.cookies.get("token") or request.query_params.get("token")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized token not found")
        payload = jwt.decode(token, key={"secret"}, algorithms=["HS256"])
        if not payload:
            raise HTTPException(status_code=401, detail="Unauthorized token not valid")
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized {e}")
          
        