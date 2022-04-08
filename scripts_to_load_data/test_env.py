from dotenv import load_dotenv
from pathlib import Path
import os
dotenv_path = Path("/home/justsomeguy/data_website_v2/.env")
load_dotenv(dotenv_path = dotenv_path)

print(dotenv_path)
print(os.getenv("LOCAL"))