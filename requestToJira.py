import requests
import base64
import json

credentialString = 'shijoonlee@gmail.com:{}'.format('VKumauMyiLEZLlc3i0fz534A')
credentialByte = bytes(credentialString, 'utf-8')
credentialBase64String = base64.b64encode(credentialByte).decode('utf-8') # base64 encoding -> byte -> string
# credentialBase64 = base64.b64encode(b'shijoonlee@gmail.com:VKumauMyiLEZLlc3i0fz534A').decode("utf-8")

credential = "Basic " + credentialBase64String
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Atlassian-Token": 'no-check',
    "Authorization": credential
}

projectKey = 'PJA'

# url = "https://codeenthusiast.atlassian.net/rest/api/3/search?jql=project={projectKey}".format(projectKey = projectKey)
url = "https://codeenthusiast.atlassian.net/rest/api/3/search"

response = requests.request(
   "GET", 
   url,
   headers=headers
)
# print(response.headers)
# print(response.status_code)
# print(response.url)

responseData = json.loads(response.text)


with open('response.json', 'w') as file:
    file.write(json.dumps(responseData, indent=2))

#print(responseData)