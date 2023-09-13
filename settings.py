from decouple import config, Csv
from pathlib import Path

# Key Secrets
TOKEN = config('TOKEN', default = None)
PREFIXES = config('PREFIXES', cast = Csv(), default = '//')
INVITE_URL = config('INVITE_URL', cast = str, default = None)

# File Paths
BASE_DIR = Path(__file__).parent 
COGS_DIR = config('COGS_DIR', cast = str, default = BASE_DIR / 'cogs')
LOGS_DIR = config('LOGS_DIR', cast = str, default = BASE_DIR / 'logs')
DATA_DIR = config('DATA_DIR', cast = str, default = BASE_DIR / 'data')

# API Endpoint
API_ENDPOINT = config('API_ENDPOINT')
USERNAME = config('API_USERNAME')
PASSWORD = config('API_PASSWORD')