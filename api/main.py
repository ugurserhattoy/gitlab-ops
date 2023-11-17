from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from ProjectListOp import ProjectListFuncs
from SetThingsUp import SetThingsUp
from dotenv import load_dotenv
from typing import List
from AuthOps import Authentication, User, Token, OAuth2PasswordRequestForm
import os
import gitlab

# Environment variables
load_dotenv()

gl = gitlab.Gitlab(url=os.getenv('GLAB_URL'), private_token=os.getenv('PRIVATE_TOKEN'))
gl.auth()
project_list = {}
ProjectListFunction = ProjectListFuncs(gl, project_list)
SetThings = SetThingsUp(gl)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: User):
    return await Authentication.register(user)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await Authentication.login_for_access_token(form_data)

@app.get("/users/me/")
async def read_users_me(current_user: User = Depends(Authentication.get_current_user)):
    return current_user

def init_gitlab(token: str):
    gl = gitlab.Gitlab(url=os.getenv('GLAB_URL'), private_token=token)
    gl.auth()
    return gl
   
class ProjectListQuery(BaseModel):
    id: int = None
    group: str = None
    ppath: str = None
    idList: List[int] = []
    input: str = None

@app.get("/projectlist")
async def get_project_list(current_user: User = Depends(Authentication.get_current_user)):
    return project_list

@app.put("/projectlist")
async def put_project_list(query: ProjectListQuery, current_user: User = Depends(Authentication.get_current_user)):
    gl = init_gitlab(current_user["private_token"])
    ProjectListFunction = ProjectListFuncs(gl, project_list)
    if query.id:
        p = ProjectListFunction.getProjectById(query.id)
        ProjectListFunction.putProjectArgs(p)
        return {str(p.id): project_list[p.id]}
    elif query.group:
        ProjectListFunction.putProjectsByGroup(query.group)
        return project_list

@app.delete("/projectlist")
async def delete_project_list(current_user: User = Depends(Authentication.get_current_user)):
    response = project_list.clear()
    return response

@app.put("/projectlist/{setting}")
async def update_something(setting: str, query: ProjectListQuery, current_user: User = Depends(Authentication.get_current_user)):
    gl = init_gitlab(current_user["private_token"])
    SetThings = SetThingsUp(gl)
    response = getattr(SetThings, setting)(query.input, query.idList)
    return response

@app.delete("/projectlist/{setting}")
async def delete_something(setting: str, query: ProjectListQuery, current_user: User = Depends(Authentication.get_current_user)):
    gl = init_gitlab(current_user["private_token"])
    SetThings = SetThingsUp(gl)
    if setting == 'protectedBranches':
        response = SetThings.removeBranchProtection(query.input, query.idList)
        return response
    else:
        raise HTTPException(status_code=405, detail="Method Not Allowed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001) #log_level="debug"
