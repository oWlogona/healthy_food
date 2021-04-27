import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

host = 'localhost'
database = ''
pg_user = ''
pg_password = ''
pg_uri = f'postgresql://{pg_user}:{pg_password}@{host}/{database}'


ADMIN_ID = ''
