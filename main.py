import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from jinja2 import Template, Environment, FileSystemLoader
import markdown
from pathlib import Path
import logging
import time

logging.basicConfig(
    level=logging.INFO,  # Set the minimum level to log
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define the log format
    datefmt='%Y-%m-%d %H:%M:%S',  # Specify the date format
)
logging.Formatter.converter = time.gmtime  # Ensures UTC time is used

# jinja templates
environment = Environment(loader=FileSystemLoader("templates/"))
style = environment.get_template("style") # css styles
header = environment.get_template("header") # to render horizontal nav panel
folder = environment.get_template("folder") # to render folder panel
content = environment.get_template("content") # to render md text panel
body = environment.get_template("body") # to render combo of folder panel & md text panel
html = environment.get_template("html") # to render html 

app = FastAPI()

root = os.getenv('MD_FILES_ROOT', 'root') 
logging.info(f"####### root directory of md files: {root} #######")

def get_folders_and_md_files(file_path):
    logging.info(f"####### file_path: {file_path} #######")
    

def getPathsAndFileNames(file_path):
    logging.info(f"####### file_path: {file_path} #######")
    
    sep = os.sep
    # now work with file system path starting from root
    if file_path: 
        # not empty string, eg. file1.md, folder1
        # file_path = f"{root}/{file_path}"
        file_path = os.path.join(root, file_path)
    else: 
        # empty string, meaning root 
        file_path = root

    tokens = file_path.split(sep)
    if file_path.endswith(".md"): 
        # it has file name
        file_name = file_path
        file_path = sep.join(tokens[:-1])
        relative_file_name = sep.join(tokens[1:])
        relative_file_path = sep.join(tokens[1:-1])
    else: 
        # it has no file name
        file_name = ""
        # file_path = file_path
        relative_file_name = ""
        relative_file_path = sep.join(tokens[1:])
    
    logging.info(f"####### abs full file path: {file_path} #######")
    logging.info(f"####### abs file name: {file_name} #######")
    logging.info(f"####### relative file path: {relative_file_path} #######")
    
    return file_path, file_name, relative_file_path, relative_file_name

def getContent(file_path):
    # get abs and relative paths and names
    file_path, file_name, relative_file_path, relative_file_name = getPathsAndFileNames(file_path)

    # get sub folders and files & render folder portion
    items = os.listdir(file_path)
    _folder = folder.render(relative_file_path=(relative_file_path + "/" if relative_file_path else ""), items=items)
    logging.info("#######" + _folder)

    # get file content and render md into html
    md_text = ""
    if file_name: 
        with open(file_name, "r") as f:
            md_text = markdown.markdown(f.read())  
    _content = content.render(md_text=md_text)
    
    # now render all 
    _style = style.render()
    _header = header.render()
    _body = body.render(relative_file_path=relative_file_path, 
                            relative_file_name=relative_file_name, 
                                folder=_folder, content=_content)

    _html = html.render(style=_style, header=_header, body=_body)
    return _html

@app.get("/{file_path:path}", response_class=HTMLResponse)
def getHtml(file_path: str):
    return getContent(file_path)
    