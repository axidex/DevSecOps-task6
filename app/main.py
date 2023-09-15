from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from git import Repo
import os, shutil, uuid, time

from app.addons.fexist import FExist
from app.addons.dt import dtSend, uuidGet
from app.addons.db import dbGet, dbSend
from app.addons.pdantic import MyDataModel
from app.addons.limiter import rateLimited
from app.addons.security import authenticate_user

# Constants
###########
# https://github.com/0c34/govwa https://github.com/netlify/gocommerce
project_ip      = str(os.environ["IP_DT"])
apiKey          = str(os.environ["API_KEY"])

mongo_host = str(os.environ["IP_DB"])
mongo_port = 27017
mongo_database = "logs"
    
# FastAPI
#########
app = FastAPI()

# CORS
######
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить доступ из любых источников (можете настроить список разрешенных источников)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить любые HTTP-методы (GET, POST, PUT, DELETE и другие)
    allow_headers=["*"],  # Разрешить любые заголовки
)

# FastAPI Methods
#################
@app.get("/")
@rateLimited(maxCalls=10, timeFrame=60)
async def readRoot(user: dict = Depends(authenticate_user)):
    return {"Documentation in": "/docs"}

@app.post("/sca") # 0c34 govwa
@rateLimited(maxCalls=10, timeFrame=60)
async def sca(data: MyDataModel, user: dict = Depends(authenticate_user)):
    headers = {"X-Api-Key": apiKey, "accept": "application/json"}
    gitUrl = data.website_url
    gitName = gitUrl.split('/')[-2]
    gitRep  = gitUrl.split('/')[-1]
    gitBranch = data.git_branch
    repPath = "/code/" + str(uuid.uuid4())
    
    Repo.clone_from(gitUrl, repPath, branch=gitBranch)
    time.sleep(5)

    if FExist.folderExist(repPath):
        os.system('./cyclonedx-gomod app -output ./sbom.xml ' + repPath)
    else:
        return { "result": "the folder with repository does not exist"}
    
    headers = {"X-Api-Key": apiKey, "accept": "application/json"}

    if FExist.fileExist('/code/sbom.xml'):
        dtSend(gitName, gitRep, gitBranch, project_ip, headers)
    else:
        return { "result": "file with sbom does not exist" }
    
    try:
        shutil.rmtree(repPath)
    except OSError as e:
        print(f"Warning with deleting {repPath}: {e}")
    
    uuidResp = uuidGet(gitName, gitRep, gitBranch, project_ip, headers)

    dbSend(mongo_host, mongo_port, mongo_database, uuidResp, project_ip, headers)
    dbGet(mongo_host, mongo_port, mongo_database)

    return { "result": uuidResp }

@app.post("/test")
@rateLimited(maxCalls=10, timeFrame=60)
async def sca(user: dict = Depends(authenticate_user)):
    print("hello")

# @app.post("/test2")
# @rateLimited(maxCalls=10, timeFrame=60)
# async def sca(user: dict = Depends(authenticate_user)):
#     print("hello")