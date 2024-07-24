import requests
from pprint import pprint
import json

def main():
    with open("testfile2.py") as file:
        source = file.read()
        source = {"source":source}
        print(json.dumps(source))
        response = requests.post("http://localhost:8000/endpoint/",data=json.dumps(source))
        response_data = response.json()
        #pprint(response_data)

main()