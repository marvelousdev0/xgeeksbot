import requests
import json

headers = {"Accept": "application/json"}

def getCareerPaths():
    url = 'http://localhost:8000/api/v1/paths'
    print()
    print("<==== Career Paths ====>")
    data = requests.get(url)
    data = data.json()
    print(data)
    print()

    if (data):
        return data
    else:
        return None

def getCareerPathDetails(career_path):
    url = 'http://localhost:8000/api/v1/paths/{}'.format(career_path)
    print()
    print("<==== Career ====>")
    data = requests.get(url)
    data = data.json()
    print(data)
    print()

    if (data):
        return data
    else:
        return None