from fastapi import FastAPI

def getApp():
    app = FastAPI()
    
    # orgnize apis across routers/modules, *** order does matter ***
    from routers import misc, search, browse
    app.include_router(misc.router)
    app.include_router(search.router)
    app.include_router(browse.router)

    return app