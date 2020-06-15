import requests
import json
url="http://localhost:8080/search"
params={"tags":[1,2,3]}

headers = {'content-type': 'application/json'}
r=requests.post(url,data=json.dumps(params), headers=headers)
print(r.text)
