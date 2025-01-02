import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from jinja2 import Template, Environment, FileSystemLoader
import markdown
from pathlib import Path
import logging
import time
import uvicorn

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

content = os.getenv('MD_FILES_content', 'content') 
logging.info(f"####### content directory of md files: {content} #######")

def get_folders_and_md_files_and_file_text(path):
    # full path starting from content path ps. os.path.join(content, path) doesn't give desire result when path is empty
    file_path = os.sep.join([content, path]) 
    logging.info(f"####### file path with content: {file_path} #######")
    # path from url without the leading content path
    relative_file_path = file_path.removeprefix(content) 
    logging.info(f"####### relative file path w/o content: {relative_file_path} #######")

    if not os.path.exists(file_path):
        raise ValueError(f"The path {path} does not exist!")

    items = {
        'subfolders': [],
        'md_files': []
    }

    file_name = ""
    file_dir = ""
    relative_file_dir = ""
    relative_file_name = ""
    file_text = ""
    if os.path.isfile(file_path):
        logging.info(f"####### {file_path} is file #######")
        file_name = os.path.basename(file_path)
        file_dir = os.path.dirname(file_path)
        relative_file_name = file_name.removeprefix(content)
        relative_file_dir = file_dir.removeprefix(content)
        try:
            with open(file_path, "r") as f:
                file_text = f.read() 
        except Exception as ex:
                file_text = f"error reading file {file_path}, {ex}"
        file_path = file_dir
    else:
        logging.info(f"####### {file_path} is directory #######")

    with os.scandir(file_path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(".md"):
                _fn = entry.path.removeprefix(content)
                items['md_files'].append({'name': entry.name,'relative_path': _fn})
            elif entry.is_dir():
                _sn = entry.path.removeprefix(content)
                items['subfolders'].append({'name': entry.name,'relative_path': _sn})

    return items['subfolders'], items['md_files'], file_text, relative_file_dir, relative_file_name, relative_file_path

def get_html_content(file_path):
    # get abs and relative paths and names
    subfolders, md_files, file_text, relative_file_dir, relative_file_name, relative_file_path = get_folders_and_md_files_and_file_text(file_path)

    # get sub folders and files & render folder portion
    _folder = folder.render(subfolders=subfolders, md_files=md_files)
    logging.debug("####### " + _folder)

    # get file content and render md into html
    _content = content.render(file_text=markdown.markdown(file_text))
    logging.debug("####### " + _content)
    
    # now render all 
    _style = style.render()
    _header = header.render()
    _body = body.render(relative_file_path=relative_file_path, 
                            relative_file_name=relative_file_name,
                                folder=_folder, content=_content)

    _html = html.render(style=_style, header=_header, body=_body)
    return _html

@app.get("/icons/{name}")
def get_icon(name: str):
    # either file-icon.png or folder-icon.png
    return FileResponse(f"{name}-icon.png")

@app.get("/{file_path:path}", response_class=HTMLResponse)
def get_html(file_path: str):
    return get_html_content(file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)