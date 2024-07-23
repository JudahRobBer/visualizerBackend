import requests
from pprint import pprint
import json

def main():
    with open("testfile.py") as file:
        source = file.read()
        source = {"source":source}
        response = requests.post(f"http://localhost:8000/endpoint/",data=json.dumps(source))
        response_data = response.json()
        pprint(response_data)

main()