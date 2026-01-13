"""
Main application entry point for the Flask Roadmap API.

This file serves as the entry point for running the Flask application.
It's the file you run to start the web server locally.

Key Concepts for Beginners:
- Entry Point: This is where the application starts when you run 'python run.py'
- Flask App Factory: We use the create_app() function to build our Flask application
- Development Mode: The app runs in debug mode for easier development
- Host and Port: The server listens on all interfaces (0.0.0.0) on port 5000
"""

from app import create_app
import os

# Create the Flask application instance using the app factory pattern
# The app factory pattern allows us to create multiple app instances with different configurations
# For Vercel deployment, we check the environment and use production config if deployed
config_name = 'production' if os.environ.get('VERCEL') else 'development'
app = create_app(config_name)

# This block only runs when the file is executed directly (not imported)
# It's a Python convention to use this pattern for executable scripts
if __name__ == '__main__':
    # Start the Flask development server
    # debug=True: Enables automatic reloading when code changes and detailed error pages
    # host='0.0.0.0': Makes the server accessible from any IP address (not just localhost)
    # port=5000: The port number where the server will listen for requests
    app.run(debug=True, host='0.0.0.0', port=5000)