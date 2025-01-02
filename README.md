# What is it? 
It's a simple website pointing to a local folder containing sub-folders & markdown files. 

![alt text](screen.png)

# Installation 
1. UV python package mgmt installtion: eg use 'brew install uv' on mac

# How to run it? 
Still trying to figure out how to use uv python package mgr to create cli app. Meanwhile,  
1. check out code and cd into the folder 
2. run cmd: 'uv venv' (to create virtual env)
3. run cmd: 'source .venv/bin/activate' (to activate virtual env)
4. run cmd: 'uv sync' (to get virtual env installed with needed libs)
5. run cmd: 'uv run --env-file=.env uvicorn main:app' (to start the web app)
6. open browser and input url http://0.0.0.0:8000/

# What's next? 
1. you can remove all sub folders and md files except md files mentioned in templates/header file. 
2. or you can point the content folder in .env file to folder other than content
3. or you can customize files under templates folder, eg. look and feel, change welcome message to something else

# Misc
1. UV installtion on mac: brew install uv
2. Init project: uv init py-site-w-md-files and cd into it
3. Create a package with cmd: uv init --package md-website-pkg
4. Test it by running cmd: uv run --directory md-website-pkg md-website-pkg
5. Create a lib with cmd: uv init --lib md-website-lib
6. Test it by running cmd: uv run --directory md-website-lib python -c "import md_website_lib; print(md_website_lib.hello())"
7. Launch vscode: code py-site-w-md-files
8. Create .venv: uv venv --python 3.12
9. Activate venv: source .venv/bin/activate
10. Add fastapi: uv add "fastapi[standard]"
11. Run: 
    a. "uv run fastapi run main.py"
    b. or "uv run uvicorn main:app --reload"
    c. or "uv run --env-file=.env uvicorn main:app --reload"





