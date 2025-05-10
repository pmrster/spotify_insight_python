from flask import Flask, render_template, request, redirect, url_for, session
import os
import requests
from urllib.parse import urlencode

from prep_request import prep_req
from get_access_token import get_token
from get_data import GetSpotifyUserData
from render_template import RenderTemplateFile

app = Flask(__name__)

app.secret_key = os.urandom(24)  # Important for session management


prep_data = prep_req()


redirect_uri = "https://rich-foal-regularly.ngrok-free.app/callback"


SPOTIPY_API_BASE_URL = "https://api.spotify.com/v1"

@app.route("/")
def login_page():
    print("this is main page")
    # template_loader = RenderTemplateFile().render_template_home()
    # render_template(template_loader)
    return render_template('home.html')



@app.route("/login")
def login():
    print("Go to login page...")

    scope = "user-read-private user-read-email user-top-read playlist-read-private user-read-currently-playing user-follow-read user-library-read"
    auth_url = "https://accounts.spotify.com/authorize"
    
    # prep_data = prep_req()
    params = {
        "response_type": "code",
        "client_id": prep_data["client_id"],
        "scope": scope,
        "code_challenge_method": "S256",
        "code_challenge": prep_data["code_challenge"],  
        "redirect_uri": redirect_uri,
    }
    
    spotify_auth_url = f"{auth_url}?{urlencode(params)}"
    print("spotify_auth_url: ", spotify_auth_url)
    return redirect(spotify_auth_url)



### for callback after get user auth
@app.route("/callback")
def callback():
    print("hi from post callback")
    
    current_url = request.url
    print(f"current url: {current_url}")
    
    code = request.args.get("code")
    print("[CODE]: ", code )
    
    
    if code:
        print(f"Extracted code: {code}")
        access_token = get_token(code, code_verifier=prep_data["code_verifier"], client_id=prep_data["client_id"], redirect_uri=redirect_uri)
        print("[ACCESS TOKEN from callback]: ", access_token)
        
        session["access_token"] = access_token
        return redirect(url_for("my_dashboard"))
    else:
        print("Code parameter not found in the URL.")
        return "Authorization failed"



@app.route("/my_dashboard")
def my_dashboard():
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("home"))

    #### get data
    res_user_data = GetSpotifyUserData(access_token = access_token).get_user_profile()
    
    user_data = {
                "user_id" : res_user_data["id"],
                "user_display_name" : res_user_data["display_name"],
                "user_img_url" : res_user_data["images"][0]["url"],
                
            } 
    
    res_top_artist_data = GetSpotifyUserData(access_token = access_token).get_top_artist_6m()
    
    res_top_track_data = GetSpotifyUserData(access_token = access_token).get_top_track_6m()
    
    # load_component(user_data,res_top_artist_data,res_top_track_data)
    
    
    # render_template_dashboard(user_data,res_top_artist_data,res_top_track_data)

    #    render_template('profile.html', user=user_profile, top_tracks=top_tracks)

    return render_template("my_dashboard.html",user_data=user_data,top_artist_data=res_top_artist_data,top_track_data=res_top_track_data)







# @app.route('/top_artists')
# def top_artists():
#     access_token = session.get('access_token')
#     if not access_token:
#         return redirect(url_for('homepage'))

#     headers = {'Authorization': f'Bearer {access_token}'}

#     # Get user's top artists
#     top_artists_response = requests.get(f'{SPOTIPY_API_BASE_URL}/me/top/artists?limit=10&time_range=short_term', headers=headers)
#     top_artists_response.raise_for_status()
#     top_artists = top_artists_response.json()['items']

#     return render_template('top_artists.html', top_artists=top_artists)



if __name__ == '__main__':
    app.run(debug=True, port=8000)