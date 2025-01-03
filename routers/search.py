from fastapi import APIRouter
from utils.logging import getLogging
logging = getLogging()

router = APIRouter()

@router.get("/search")
def search_files(type: str | None = None, query: str | None = None, page: int = 1):
    logging.info(f"####### type: {type} #######")
    logging.info(f"####### query: {query} #######")
    logging.info(f"####### page: {page} #######")
    return f"search type({type}), query({query}), page({page})"