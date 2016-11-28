COMPANY = 'BFA' # company info
USER_NAME = 'bgathecha@bankablefrontier.com'
PASSWORD = 'D3v3l0p3r_OPENAIR'
NETSUITE_API_KEY='2KGDv0wMsWrrJ1HtxmmF' # secret key

import os
import random
SECRET_KEY = os.urandom(int(random.random()*24))
BCRYPT_LOG_ROUNDS = 12