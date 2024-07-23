from fastapi import FastAPI,Body
import variableDependency
from pydantic import BaseModel
from typing import Annotated


#server is activated from the command line with "fastapi dev graphAPI.py"
app = FastAPI()

@app.get("/")
async def read_root():
    return {"Root":"Page"}

#simple data model to wrap the request body
class SourceWrapper(BaseModel):
    source:str


"""
source is passed as a request body as a json document of the form
{
    "source": source
}
a request of this form needs the front end to create a dict like object, serialize it to json,
and send it as the request body to make a correct api call
the returned document is a json document formatted as:
{
'links': list[dict], where each dict is of form {'source':str,'target':str}
'nodes': list[dict], where each dict is of form {'Input':bool,'Printed':bool,'id';str}
}
"""
@app.post("/endpoint/")
async def generate_graph(source:Annotated[SourceWrapper,Body()]):
    try:
        graph = variableDependency.create_vdg(source.model_dump()["source"])
        return graph
    except:
        return "pain"
    
    