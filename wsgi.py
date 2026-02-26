import sys
import os

# Add your project directory to the sys.path
project_home = '/home/velloreai/vellore-ai'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['PYTHONUNBUFFERED'] = '1'

# Import your Flask app
from app import app as application
