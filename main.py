import os
import time
import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from jinja2 import Template, Environment, FileSystemLoader
import markdown
from cachetools import TTLCache, cached

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
error = environment.get_template("error") # to render md file panel
body = environment.get_template("body") # to render combo of folder panel & md text panel
html = environment.get_template("html") # to render html 

website_name = os.getenv('WEBSITE_NAME', 'Welcome to Markdown Website')
logging.info(f"####### WEBSITE_NAME: {website_name} #######")

content = os.getenv('MD_FILES_DIR', 'content') 
logging.info(f"####### MD_FILES_DIR: {content} #######")

header_items = os.getenv('HEADER_ITEMS', 'home,services,contact').split(",")
logging.info(f"####### HEADER_ITEMS: {header_items} #######")

cache_size = int(os.getenv('CACHE_SIZE', '100'))
logging.info(f"####### CACHE_SIZE: {cache_size} #######")

cache_ttl = int(os.getenv('CACHE_TTL', '0')) # in seconds
logging.info(f"####### CACHE_TTL: {cache_ttl} #######")

cache = TTLCache(maxsize=cache_size, ttl=cache_ttl)

@cached(cache)
def get_folders_and_md_files_and_file_text(path):
    logging.info(f"####### raw path w/o content dir: {path} #######")

    file_name, abs_file_dir, rel_file_dir, file_content, error_msg = "", "", "", "", ""

    # full path starting from content path ps. os.path.join(content, path) doesn't give desire result when path is empty
    abs_path = os.sep.join([content, path]) 
    logging.info(f"####### abs_path with content dir: {abs_path} #######")

    if not os.path.exists(abs_path):
        logging.error(f"####### the abs_path '{abs_path}' does not exist! #######")
        error_msg = f"the path '{path}' does not exist!"
        abs_path = os.sep.join([content, ""]) # show the content folder upon error
 
    # path from url without the leading content path
    rel_path = abs_path.removeprefix(content) 
    logging.info(f"####### rel_path w/o content dir: {rel_path} #######")

    items = {
        'subfolders': [],
        'md_files': []
    }

    if not error_msg: 
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
                logging.error(f"####### error reading file '{abs_path}', {ex} #######")
                error_msg= f"error reading file '{path}', {ex}!"

        else:
            logging.info(f"####### abs_path {abs_path} is a directory #######")

    abs_scan_dir = abs_file_dir if abs_file_dir else abs_path
    rel_scan_dir = abs_scan_dir.removeprefix(content)
    logging.info(f"####### abs_scan_dir is {abs_scan_dir} #######")
    logging.info(f"####### rel_scan_dir is {rel_scan_dir} #######")

    with os.scandir(abs_scan_dir) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(".md"):
                items['md_files'].\
                    append({'name': entry.name,'rel_path': entry.path.removeprefix(content)})
            elif entry.is_dir():
                items['subfolders'].\
                    append({'name': entry.name, 'rel_path': entry.path.removeprefix(content)})

    return rel_scan_dir, items['subfolders'], items['md_files'], file_name, file_content, error_msg

@cached(cache)
def get_html_content(file_path):
    # get abs and relative paths and names
    rel_scan_dir, subfolders, md_files, file_name, file_content, error_msg \
        = get_folders_and_md_files_and_file_text(file_path)

    # get sub folders and files & render folder portion
    _folder = folder.render(subfolders=subfolders, md_files=md_files)
    logging.debug("####### " + _folder + "####### ")

    # get file content and render md into html
    _file = error.render(error_msg=error_msg) if error_msg \
        else file.render(file_content=markdown.markdown(file_content))
    logging.debug("####### " + _file + "####### ")
    
    # now render all 
    _style = style.render()
    _header = header.render(website_name=website_name, items=header_items)
    _body = body.render(rel_scan_dir=rel_scan_dir, file_name=file_name, folder=_folder, file=_file)
    _html = html.render(style=_style, header=_header, body=_body)
    return _html

app = FastAPI()

@app.get("/favicon.ico", include_in_schema=False)
def get_favicon(name: str):
    return FileResponse("screen.png")

@app.get("/{file_path:path}", response_class=HTMLResponse)
def get_html(file_path: str):
    return get_html_content(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

