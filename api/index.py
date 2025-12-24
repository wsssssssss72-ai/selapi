from fastapi import FastAPI
import sys
import os

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

# Vercel expects this to be named 'app'
# This file simply imports and re-exports your FastAPI app