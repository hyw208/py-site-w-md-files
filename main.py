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
file = environment.get_template("file") # to render md file panel
body = environment.get_template("body") # to render combo of folder panel & md text panel
html = environment.get_template("html") # to render html 

app = FastAPI()

content = os.getenv('MD_FILES_DIR', 'content') 
logging.info(f"####### content directory of md files: {content} #######")

def get_folders_and_md_files_and_file_text(path):
    logging.info(f"####### raw path w/o content dir: {path} #######")

    # full path starting from content path ps. os.path.join(content, path) doesn't give desire result when path is empty
    abs_path = os.sep.join([content, path]) 
    logging.info(f"####### abs_path with content dir: {abs_path} #######")
    
    # path from url without the leading content path
    rel_path = abs_path.removeprefix(content) 
    logging.info(f"####### rel_path w/o content dir: {rel_path} #######")

    if not os.path.exists(abs_path):
        logging.error(f"The abs_path {abs_path} does not exist!")
        raise ValueError(f"The path {path} does not exist!")

    items = {
        'subfolders': [],
        'md_files': []
    }

    file_name = ""
    abs_file_dir = ""
    rel_file_dir = ""
    file_content = ""
    if os.path.isfile(abs_path):
        logging.info(f"####### abs_path {abs_path} is a file #######")
        file_name = os.path.basename(abs_path)
        """ 
        abs_file_dir = os.path.dirname(abs_path)
        
        the line about doesn't handle well for case, eg. content/home.md 
        where abs_file_dir becomes 'content' instead of the desired 'content/'
        """
        tokens = abs_path.split(os.sep)
        tokens[-1] = ""
        abs_file_dir = os.sep.join(tokens)
        
        rel_file_dir = abs_file_dir.removeprefix(content)
        try:
            with open(abs_path, "r") as f:
                file_content = f.read() 
        except Exception as ex:
                file_content = f"error reading file {abs_path}, {ex}"
    else:
        logging.info(f"####### abs_path {abs_path} is a directory #######")

    abs_scan_dir = abs_file_dir if abs_file_dir else abs_path
    rel_scan_dir = abs_scan_dir.removeprefix(content)
    logging.info(f"####### abs_scan_dir is {abs_scan_dir} #######")
    logging.info(f"####### rel_scan_dir is {rel_scan_dir} #######")

    with os.scandir(abs_scan_dir) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(".md"):
                _fn = entry.path.removeprefix(content)
                items['md_files'].append({'name': entry.name,'rel_path': _fn})
            elif entry.is_dir():
                _sn = entry.path.removeprefix(content)
                items['subfolders'].append({'name': entry.name,'rel_path': _sn})

    return rel_scan_dir, items['subfolders'], items['md_files'], file_name, file_content

def get_html_content(file_path):
    # get abs and relative paths and names
    rel_scan_dir, subfolders, md_files, file_name, file_content = get_folders_and_md_files_and_file_text(file_path)

    # get sub folders and files & render folder portion
    _folder = folder.render(subfolders=subfolders, md_files=md_files)
    logging.debug("####### " + _folder)

    # get file content and render md into html
    _file = file.render(file_content=markdown.markdown(file_content))
    logging.debug("####### " + _file)
    
    # now render all 
    _style = style.render()
    _header = header.render()
    _body = body.render(rel_scan_dir=rel_scan_dir, 
                            file_name=file_name,
                                folder=_folder, file=_file)

    _html = html.render(style=_style, header=_header, body=_body)
    return _html

@app.get("/favicon.ico", include_in_schema=False)
def get_favicon(name: str):
    return FileResponse("screen.png")

@app.get("/{file_path:path}", response_class=HTMLResponse)
def get_html(file_path: str):
    return get_html_content(file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)