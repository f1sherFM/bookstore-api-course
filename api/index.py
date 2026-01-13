"""
Vercel serverless function entry point.
This file is specifically designed for Vercel deployment.
"""

import sys
import os

# Add the parent directory to the Python path so we can import our app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Create the Flask application for Vercel
app = create_app('production')

# Vercel expects the Flask app to be available as 'app'
# This is the entry point for all requests
if __name__ == "__main__":
    app.run()