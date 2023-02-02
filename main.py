from typing import Union

from fastapi import FastAPI

from akinator import Akinator

import pandas as pd

from pydantic import BaseModel

app = FastAPI()


df = pd.read_csv('base.csv')
a = Akinator(df)
a.genTreeFromDf()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/execution")
def create_execution():
  return {"requisition_id": a.createExecution()}

@app.get("/question/{execution_id}")
def get_question(execution_id):
  return {"result": a.getQuestion(int(execution_id))}



class Answer(BaseModel):
    answer: int

@app.post("/questions/{execution_id}")
async def send_answer(execution_id, answer: Answer):
    return {"result": a.execute(int(execution_id), answer.answer)}