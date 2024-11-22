import sys
import os

sys.path.append('/home/q/quicksteps/venv/lib/python3.10/site-packages/')
sys.path.append('/home/q/quicksteps/dev_prod/public_html')

from app import create_app  

application = create_app()