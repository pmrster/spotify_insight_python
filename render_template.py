import streamlit as st
import streamlit.components.v1 as components
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

# #### render html template
print("trying to render template")
current_dir = os.path.dirname(os.path.abspath(__file__))

# project_dir = os.path.abspath(os.path.join(current_dir, '..'))
project_dir = os.path.abspath(current_dir)
print("project dir:", project_dir )

# folder_root = os.path.abspath(os.path.join(page_dir, '..', '..'))
folder_path = os.path.join(project_dir , 'templates')
print("folder path:", folder_path )


template_loader = Environment(loader=FileSystemLoader(folder_path))
# template_loader = jinja2.FileSystemLoader(folder_path)  
print(f"template_loader: {template_loader}")


# try:
#     template = template_loader.get_template('home.html')
#     print(f"template base_page: {template}")
# except Exception as e:
#     print(f"error on get env jinja: {e}")
    
    
    
       
class RenderTemplateFile:
    def __init__(self,user_data=None,res_top_artist_data=None,res_top_track_data=None):
        self.user_data = user_data
        self.res_top_artist_data = res_top_artist_data
        self.res_top_track_data = res_top_track_data
        
    
    def load_component(self):
        try:
            template = template_loader.get_template("elements.html")
            print(f"template base_page: {template}")
        except Exception as e:
            print(f"error on get env jinja: {e}")
        
        static_path = os.path.join(project_dir , 'static')
        print("static_path: ", static_path)
        
        with open(f"{static_path}/styles.css") as f:
            css_styles = f.read()
            
        try:

            rendered_html = template.render(
                user_data=self.user_data,
                top_artist_data=self.res_top_artist_data,
                top_track_data=self.res_top_track_data,
                css=css_styles)
            
        except Exception as e:
            print("error on render template:", e)
            
        print("finish gen html template")

        components.html(rendered_html, height=10000, scrolling=True)
        
        