from fastapi import FastAPI

from akinator import Akinator

from addCharachters import AddCharachters, Character

import pandas as pd

from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def start():
  df = pd.read_csv('base.csv')
  a = Akinator(df)
  a.genTreeFromDf()
  return a

a = start()
 
@app.post("/executions")
def create_execution():
  return {"requisition_id": a.createExecution()}

@app.get("/questions/{execution_id}")
def get_question(execution_id):
  return {"result": a.getQuestion(int(execution_id))}

class Answer(BaseModel):
    answer: int

@app.post("/questions/{execution_id}")
async def send_answer(execution_id, answer: Answer):
    return {"result": a.execute(int(execution_id), answer.answer)}

class addCharacterRequest(BaseModel):
  name: str
  values: list[int]

@app.post("/add_character")
async def addCharacter(char: addCharacterRequest):
  charCreator = AddCharachters()
  c = Character(char.name)
  c.addValues(char.values)
  charCreator.addCharacter(c)
  charCreator.commitChanges()
  global a
  a = start()
  return c

async def getLabels():
  return