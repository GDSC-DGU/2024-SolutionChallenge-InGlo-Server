import requests
from dotenv import load_dotenv
import os
from logging import getLogger
load_dotenv()

logger = getLogger('django')

response = requests.post(os.getenv('ISSUE_CREATE_API'))
logger.info('-------------------Issue create API called successfully.----------------------------')