import requests
import os
from dotenv import load_dotenv
import os 
import secrets
import base64
import hashlib


load_dotenv()

###code verifier
def generate_random_string(length):
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(secrets.choice(possible) for _ in range(length))



###code challenge
def sha256(plain):
    data = plain.encode('utf-8')
    return hashlib.sha256(data).digest()
    # return hashlib.sha256(data).hexdigest()



def base64encode(input_bytes):
    
    encoded = base64.b64encode(input_bytes).decode('utf-8')
    
    return encoded.replace('+', '-').replace('/', '_').rstrip('=')


def prep_req():
    ## app key
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

    
    ##code verifier
    code_verifier = generate_random_string(64)
    
    ## get code challenge
    hashed = sha256(code_verifier)
    code_challenge = base64encode(hashed)
    
    res = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code_verifier": code_verifier,
        "code_challenge": code_challenge
    }
    
    print("prep_req: ", res)
    
    
    return res