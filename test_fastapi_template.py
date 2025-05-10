from dotenv import load_dotenv
import os 
from fastapi import FastAPI, Request, responses
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from datetime import datetime


load_dotenv()

client_id = os.environ.get('SPOTIFY_CLIENT_ID')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')


app = FastAPI()

@app.get("/")
async def root():
    print("this is main page")
    return {"message": "please go to /display"}


@app.get("/login")
async def root():
    print("this is main page")
    return {"message": "please go to /display"}