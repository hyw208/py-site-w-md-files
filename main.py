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
navigation = environment.get_template("navigation")
header_style = environment.get_template("header_style")
body_style = environment.get_template("body_style")
header = environment.get_template("header")
body = environment.get_template("body")
html = environment.get_template("html")

app = FastAPI()

root = os.getenv('MD_FILES_ROOT', 'root') 
logging.info(f"####### root directory of md files: {root} #######")

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

    # get sub folders and files & render navigation portion
    items = os.listdir(file_path)
    _navigation = navigation.render(relative_file_path=(relative_file_path + "/" if relative_file_path else ""), items=items)
    logging.info("#######" + _navigation)

    # get file content and render md into html
    if file_name: 
        with open(file_name, "r") as f:
            md_text = f.read()
            _content = markdown.markdown(md_text)
    else: 
        _content = ""
    
    # now render all 
    _header_style = header_style.render()
    _header = header.render()
    _body_style = body_style.render()
    _body = body.render(relative_file_path=relative_file_path, 
                            relative_file_name=relative_file_name, 
                                navigation=_navigation, content=_content)

    _html = html.render(header_style=_header_style, 
                            body_style=_body_style,
                                header=_header, body=_body)
    return _html

@app.get("/{file_path:path}", response_class=HTMLResponse)
def getHtml(file_path: str):
    return getContent(file_path)
    