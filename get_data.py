import requests
import os
from dotenv import load_dotenv
import os 
import json

from datetime import datetime

from prep_request import prep_req
from get_access_token import get_token
from transform_data import TransformSpotifyResponse

load_dotenv()

access_token_manual = os.environ.get("SPOTIFY_ACCESS_TOKEN_MANUAL")

client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")



class GetSpotifyUserData:
    def __init__(self, access_token, time_range = None):
      self.access_token = access_token
      self.time_range = time_range
    
    def get_user_profile(self):
        endpoint = "https://api.spotify.com/v1/me"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(endpoint, headers=headers)
        
        print("[RESPONSE CODE]: ", response.status_code)
        print("[RESPONSE]: ", response.text)
        data = response.json()
        print(data)
        file_name = f"{datetime.now().strftime('%Y.%m.%d_%H%M%S')}_spotify_user_data.json"
        # with open(f"response_data/{file_name}", "w", encoding='utf-8') as f:
        #     json_string = json.dumps(data, indent=4,ensure_ascii=False)
        #     f.write(json_string) 
        return data

    def get_top_artist_6m(self):
        endpoint = "https://api.spotify.com/v1/me/top/artists"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "offset": 0,
            "time_range": self.time_range,
            "limit": 20
        }
        response = requests.get(endpoint, headers=headers,params=params)
        
        print("[RESPONSE CODE]: ", response.status_code)
        print("[RESPONSE]: ", response.text)
        data = response.json()
        print(data)
        
        file_name = f"{datetime.now().strftime('%Y.%m.%d_%H%M%S')}_spotify_user_top_artist_6m.json"
        
        # with open(f"response_data/{file_name}", "w", encoding='utf-8') as f:
        #     json_string = json.dumps(data, indent=4,ensure_ascii=False)
        #     f.write(json_string) 
            
        transformed_data = TransformSpotifyResponse(data).transform_top_artist()
        
        return transformed_data

    def get_top_track_6m(self):
        endpoint = "https://api.spotify.com/v1/me/top/tracks"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "offset": 0,
            "time_range": self.time_range,
            "limit": 20
        }
        response = requests.get(endpoint, headers=headers,params=params)
        
        print("[RESPONSE CODE]: ", response.status_code)
        print("[RESPONSE]: ", response.text)
        data = response.json()
        print(data)
        
        file_name = f"{datetime.now().strftime('%Y.%m.%d_%H%M%S')}_spotify_user_top_tracks_6m.json"
        # with open(f"response_data/{file_name}", "w", encoding='utf-8') as f:
        #     json_string = json.dumps(data, indent=4,ensure_ascii=False)
        #     f.write(json_string) 
            
            
        transformed_data = TransformSpotifyResponse(data).transform_top_track_data()
        
        return transformed_data
        
        





# if __name__ == "__main__":
#     # GetSpotifyUserData(access_token = access_token_manual).get_user_profile()
#     # GetSpotifyUserData(access_token = access_token_manual).get_top_artist_6m()
#     GetSpotifyUserData(access_token = access_token_manual).get_top_track_6m()