from pydantic import BaseModel, HttpUrl
# Pydantic
##########
class MyDataModel(BaseModel):
    website_url: HttpUrl 
    git_branch: str