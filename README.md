# What is it? 
It's a website using a folder of markdown files. 

# How to run it? 

# Misc

1. UV installtion on mac: brew install uv

2. Init project: uv init py-site-w-md-files

3. Launch vscode: code py-site-w-md-files

4. Create .venv: uv venv --python 3.12

5. Activate venv: source .venv/bin/activate

6. Add fastapi: uv add "fastapi[standard]"

7. Create main.py and copy & paste the following 
        from fastapi import FastAPI
        app = FastAPI()
        @app.get("/")
        def read_root():
            return {"message": "Hello World"}

8. Run: 
    a. "uv run fastapi run main.py"
    b. or "uv run uvicorn main:app --reload"
    c. or "uv run --env-file=.env uvicorn main:app --reload"

9. Launch app: http://0.0.0.0:8000

11. Now, we are ready to add code and 3rd party libs 

12. Add lib, eg. uv add fastapi[standard] Jinja2 markdown





