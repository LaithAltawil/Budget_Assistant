import os
import dotenv as env

def config():
    env.load_dotenv()

# Call config immediately when this module is imported
config()
