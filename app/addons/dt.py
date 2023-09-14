import requests, json
# Sender to dependency track via cUrl
#####################################
def dtSend(projectName: str, projectRep: str, projectBranch: str, projectIp:str, headers: str):

    files = {
        'autoCreate':       (None, 'true'),
        'projectName':      (None, projectName+'/'+projectRep),
        'projectVersion':   (None, projectBranch),
        'bom':              ('sbom.xml', open('/code/sbom.xml', 'rb'), 'application/xml')
    }

    response = requests.post( projectIp + '/api/v1/bom', 
                              headers=headers, 
                              files=files )

# uuID getter
#############
def uuidGet(gitName: str, gitRep: str, gitBranch: str, projectIp: str, headers: str):
    uuid_resp = 'not_found'
    resp = requests.get(projectIp + '/api/v1/project', headers=headers)
    parsed = json.loads(resp.content)
    for el in parsed:
        if el['name'] == gitName+'/'+gitRep and el['version'] == gitBranch:
            uuid_resp  = el["uuid"]
    return uuid_resp

# Logs
######
def to_log(url, headers):
    resp = requests.get(url, headers=headers)
    return json.loads(resp.content)