# to prevent back button if logged out from opening previous page, ensure no caching happens
from flask import Response

resp = Response("")
resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')