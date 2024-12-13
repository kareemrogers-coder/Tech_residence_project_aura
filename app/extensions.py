from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from authlib.integrations.flask_client import OAuth


ma = Marshmallow()
oauth = OAuth()

limiter = Limiter(key_func=get_remote_address)

cache = Cache()