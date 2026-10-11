
import json
import boto3
import requests

from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

url = "https://jcrnc2gvyg.execute-api.us-east-1.amazonaws.com/detect"

body = json.dumps({"key": "input/person.jpg"})

session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()

request = AWSRequest(
    method="POST",
    url=url,
    data=body,
    headers={"Content-Type": "application/json"}
)

SigV4Auth(credentials, "execute-api", "us-east-1").add_auth(request)

response = requests.post(
    url,
    data=body,
    headers=dict(request.headers),
    timeout=180
)

print("HTTP status:", response.status_code)
print("Response:", response.text)
