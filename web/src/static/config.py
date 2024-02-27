import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):

    DEBUG = False
    TESTING = False

    DEV = bool(int(os.getenv('DEV')))
    HARMONY_PRIVATE_KEY = os.getenv('HARMONY_PRIVATE_KEY')
    HARMONY_PUBLIC_ADDRESS = os.getenv('HARMONY_PUBLIC_ADDRESS')



