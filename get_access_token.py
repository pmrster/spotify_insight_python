import requests
import os 




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


