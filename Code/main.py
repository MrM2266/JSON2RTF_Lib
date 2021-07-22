from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import JSON2RTF_lib as RTF

fake_users_db = {
    "jirka": {
        "username": "jirka",
        "hashed_password": "fakehashedsecret"
    },
    "jana": {
        "username": "alice",
        "hashed_password": "fakehashedsecret2"
    },
}

app = FastAPI()

def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
        

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access_token": user.username, "token_type": "bearer"}

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...), current_user: User = Depends(get_current_user)):
    if len(files)!=2:
        raise HTTPException(status_code=400, detail="Too many files or too few were uploaded")

    RTF.Init()
    for file in files:
        if file.content_type=="application/json" and file.filename[-5:]==".json":
            RTF.LoadJson( await file.read(), 1)
            await file.close()
        if file.filename[-4:]==".rtf":
            inputRTF = await file.read()
            RTF.LoadRTF(inputRTF.decode())
            await file.close()

    files.clear()
    RTF.ProcessRTF()

    output=RTF.GetOutput()

    return HTMLResponse(content=output)

@app.get("/")
async def main():
    content = """
    <body>
    <br>
    <form action="/token/" enctype="multipart/form-data" method="post">
    <label for="fname">Username:</label><br>
    <input type="text" id="username" name="username"><br><br>
    <label for="fname">Authorization code:</label><br />
    <input id="password" name="password" type="text" />
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)