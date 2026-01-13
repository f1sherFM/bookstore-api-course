"""
Minimal Flask app for Vercel testing.
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simple test data
ROADMAP_DATA = {
    "success": True,
    "data": [
        {
            "id": 1,
            "title": "📚 BookStore API Learning Roadmap",
            "description": "Production-ready FastAPI system - from beginner to DevOps expert",
            "node_type": "root",
            "parent_id": None,
            "github_url": "https://github.com/f1sherFM/bookstore-api-course",
            "children": [
                {
                    "id": 2,
                    "title": "🚀 Quick Explorer (5 min)",
                    "description": "Just want to see it work? Get the API running and make your first request",
                    "node_type": "basic",
                    "parent_id": 1,
                    "github_url": "https://github.com/f1sherFM/bookstore-api-course#-quick-explorer-5-minutes",
                    "children": []
                }
            ]
        }
    ],
    "message": "Roadmap retrieved successfully"
}

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask Roadmap API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>🚀 Flask Roadmap API</h1>
        <p>API is running successfully on Vercel!</p>
        
        <h2>Available Endpoints:</h2>
        <div class="endpoint">
            <strong>GET /api/v1/roadmap</strong> - Get roadmap tree structure
        </div>
        <div class="endpoint">
            <strong>GET /api/v1/health</strong> - Health check
        </div>
        <div class="endpoint">
            <strong>GET /test</strong> - Simple test endpoint
        </div>
        
        <script>
            // Test the API
            fetch('/api/v1/roadmap')
                .then(response => response.json())
                .then(data => {
                    console.log('API Response:', data);
                    document.body.innerHTML += '<h2>✅ API Test Successful!</h2><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                })
                .catch(error => {
                    console.error('API Error:', error);
                    document.body.innerHTML += '<h2>❌ API Test Failed</h2><p>' + error + '</p>';
                });
        </script>
    </body>
    </html>
    '''

@app.route('/test')
def test():
    return jsonify({
        'status': 'ok',
        'message': 'Simple Flask app is working on Vercel!',
        'environment': 'production'
    })

@app.route('/api/v1/health')
def health():
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'Roadmap API is running',
        'database': 'static_data',
        'node_count': 2
    })

@app.route('/api/v1/roadmap')
def roadmap():
    return jsonify(ROADMAP_DATA)

@app.route('/api/v1/nodes')
def nodes():
    return jsonify({
        'success': True,
        'data': [
            {
                'id': 1,
                'title': '📚 BookStore API Learning Roadmap',
                'description': 'Production-ready FastAPI system - from beginner to DevOps expert',
                'node_type': 'root',
                'parent_id': None,
                'github_url': 'https://github.com/f1sherFM/bookstore-api-course'
            },
            {
                'id': 2,
                'title': '🚀 Quick Explorer (5 min)',
                'description': 'Just want to see it work? Get the API running and make your first request',
                'node_type': 'basic',
                'parent_id': 1,
                'github_url': 'https://github.com/f1sherFM/bookstore-api-course#-quick-explorer-5-minutes'
            }
        ],
        'count': 2,
        'message': 'All nodes retrieved successfully'
    })

if __name__ == "__main__":
    app.run(debug=True)