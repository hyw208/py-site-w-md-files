import os
from cachetools import TTLCache, cached
from utils.logging import getLogging
logging = getLogging()

cache_size = int(os.getenv('CACHE_SIZE', '100'))
logging.info(f"####### CACHE_SIZE: {cache_size} #######")

cache_ttl = int(os.getenv('CACHE_TTL', '60')) # in seconds
logging.info(f"####### CACHE_TTL: {cache_ttl} #######")

cache = TTLCache(maxsize=cache_size, ttl=cache_ttl)

def getCache():
    # this is configured cache object
    return cache

def getCached():
    # just a func
    return cached