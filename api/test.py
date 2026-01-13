"""
Simple test endpoint for Vercel debugging.
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from Vercel!',
        'status': 'working'
    })

@app.route('/api/test')
def test():
    return jsonify({
        'message': 'API test endpoint working',
        'status': 'ok'
    })

if __name__ == "__main__":
    app.run()