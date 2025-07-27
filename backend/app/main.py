from fastapi import FastAPI, Depends
from openai import OpenAI

from functions import *


app = FastAPI()

openai_client = OpenAI()


@app.route("/start")
def start():
    pass


@app.route("/action")
def action(client: Depends()):
    pass
