from fastapi import FastAPI

app = FastAPI()

# orgnize apis across routers/modules, *** order does matter ***
from routers import misc, search, browse
app.include_router(misc.router)
app.include_router(search.router)
app.include_router(browse.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

