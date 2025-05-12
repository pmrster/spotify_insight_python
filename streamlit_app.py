import streamlit as st
import streamlit.components.v1 as components
from jinja2 import Environment, FileSystemLoader
from spotify.get_data import GetSpotifyUserData
from render_template import RenderTemplateFile

st.set_page_config(page_title="My Spotify data", page_icon="🎧",layout="wide")

if 'spotify_user_data' not in st.session_state:
    st.session_state["spotify_user_data"] = None
    
if 'spotify_top_artist_data' not in st.session_state:
    st.session_state["spotify_top_artist_data"] = None
    
if 'spotify_top_track_data' not in st.session_state:
    st.session_state["spotify_top_track_data"] = None

#######

st.title("Spotify Data App")
st.caption("update: 2025.11.10")

 
st.write()
 
access_token = st.text_input(label="spotify access token", type="password")



## get data
if access_token:
    
    #### get data
    res_user_data = GetSpotifyUserData(access_token = access_token).get_user_profile()
    st.session_state["spotify_user_data"] = res_user_data
    if st.session_state["spotify_user_data"]:
        user_data = {
                "user_id" : st.session_state["spotify_user_data"]["id"],
                "user_display_name" : st.session_state["spotify_user_data"]["display_name"],
                "user_img_url" : st.session_state["spotify_user_data"]["images"][0]["url"],
                
            } 
    
        res_top_artist_data = GetSpotifyUserData(access_token = access_token).get_top_artist_6m()
        st.session_state["spotify_top_artist_data"] = res_top_artist_data
    
        if st.session_state["spotify_top_artist_data"]:
            
            res_top_track_data = GetSpotifyUserData(access_token = access_token).get_top_track_6m()
            st.session_state["spotify_top_track_data"] = res_top_track_data
            
            if st.session_state["spotify_top_track_data"]:
            
             
                RenderTemplateFile(user_data,res_top_artist_data,res_top_track_data).load_component()
     
         
else:
    st.write("Please fill spotify access token")            