import requests
import os
from dotenv import load_dotenv
import os 
from fastapi import FastAPI, Request, responses
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import secrets
import base64
import hashlib
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qs
import uvicorn

from datetime import datetime

from prep_request import prep_req
from get_access_token import get_token

load_dotenv()

access_token_manual = os.environ.get("SPOTIFY_ACCESS_TOKEN_MANUAL")


 ### 
# uvicorn test_login:app --reload --host 0.0.0.0 --port 5173

app = FastAPI(debug=True)


redirect_uri = 'https://rich-foal-regularly.ngrok-free.app/callback'


prep_data = prep_req()


#######################

@app.get("/")
async def root():
    print("this is main page")
    return {"message": "please go to /login"}


@app.get("/login")
async def root():
    print("Go to login page...")
    
    
    scope = "user-read-private user-read-email user-top-read playlist-read-private user-read-currently-playing user-follow-read user-library-read"
    
    
    
    auth_url = "https://accounts.spotify.com/authorize"
    
    params = {
        'response_type': 'code',
        'client_id': prep_data["client_id"],
        'scope': scope,
        'code_challenge_method': 'S256',
        'code_challenge': prep_data["code_challenge"],  # Replace with your generated code_challenge
        'redirect_uri': redirect_uri,
    }
    # Build the query string using urlencod
    query_string = urlencode(params)
    
    spotify_auth_url = f"{auth_url}?{query_string}"
    print("spotify_auth_url: ", spotify_auth_url)
    
    
    
    return RedirectResponse(spotify_auth_url)




### for callback after get user auth
@app.get("/callback")
async def callback(request: Request, code: str):

    print("hi from post callback")
    current_url = request.url
    
    print(f"current url: {current_url}")
    print("[CODE]: ", code )


    if code:
        print(f"Extracted code: {code}")
        # prep_data = prep_req()
        
        
        access_token = get_token(code, code_verifier=prep_data["code_verifier"], client_id=prep_data["client_id"], redirect_uri=redirect_uri)
        print("[ACCESS TOKEN from callback]: ", access_token)
        
        return {"access_token": access_token} 
        
        


    else:
        print("Code parameter not found in the URL.")


    return {"message": "Login successful (or failed)"}  # Replace with appropriate response



def get_token(code, code_verifier, client_id, redirect_uri):
    get_token_endpoint ="https://accounts.spotify.com/api/token"
    payload = {
        "client_id": client_id,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }
    print("get token payload: ", payload)
    
    try:
        response = requests.post(get_token_endpoint , data=payload)
        print("[RESPONSE FROM GET TOKEN]: ", response)
        print("[RESPONSE TEXT FROM GET TOKEN]: ", response.text)
        # print("[RESPONSE STATUS]: ", response.status)
        response_data = response.json()
        print("[RESPONSE FROM GET TOKEN]: ", response_data)
        print("[ACCESS TOKEN]: ", response_data["access_token"])
    except Exception as e:
        print("get error on access token request :", e)

    return response_data["access_token"]




@app.get("/get_data")
async def callback(request: Request, access_token: str = None):
    print("hi from get data")
    current_url = request.url
    
    print(f"current url: {current_url}")
    # print("access_token: ", access_token)
    
    if not access_token_manual:
        print("no access token")
        print("access_token: ", access_token)
    else:
        print("this is access token: ", access_token_manual)
        
        
     
    
    
    final_res_data = {
        "message" : "this is result"
    }

        
    return final_res_data 
        
    
    


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
    
#, host="0.0.0.0"