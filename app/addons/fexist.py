import os

# Path finding methods
######################
class FExist: 
    @staticmethod   
    def folderExist(path: str):
        return os.path.exists(path)
    
    @staticmethod
    def fileExist(path: str):
        return os.path.isfile(path)