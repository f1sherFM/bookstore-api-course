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

"""
Interactive Flask Roadmap API for Vercel.
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Complete roadmap data with GitHub links
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
                    "children": [
                        {
                            "id": 3,
                            "title": "Setup Environment",
                            "description": "Clone repo and setup development environment",
                            "node_type": "basic",
                            "parent_id": 2,
                            "github_url": "https://github.com/f1sherFM/bookstore-api-course/blob/main/QUICK_START.md",
                            "children": []
                        },
                        {
                            "id": 4,
                            "title": "Start Development Server",
                            "description": "Run the API locally",
                            "node_type": "basic",
                            "parent_id": 2,
                            "github_url": "https://github.com/f1sherFM/bookstore-api-course/blob/main/run_bookstore.py",
                            "children": []
                        },
                        {
                            "id": 5,
                            "title": "Explore API Documentation",
                            "description": "Interactive Swagger UI",
                            "node_type": "basic",
                            "parent_id": 2,
                            "github_url": "https://github.com/f1sherFM/bookstore-api-course#-api-documentation",
                            "children": []
                        }
                    ]
                },
                {
                    "id": 6,
                    "title": "📱 API User (30 min)",
                    "description": "Want to integrate with the API? Learn authentication, core operations, and advanced features",
                    "node_type": "basic",
                    "parent_id": 1,
                    "github_url": "https://github.com/f1sherFM/bookstore-api-course#-api-user-30-minutes",
                    "children": [
                        {
                            "id": 7,
                            "title": "Authentication Flow",
                            "description": "Learn JWT authentication and user management",
                            "node_type": "basic",
                            "parent_id": 6,
                            "github_url": "https://github.com/f1sherFM/bookstore-api-course/blob/main/bookstore/auth.py",
                            "children": [
                                {
                                    "id": 8,
                                    "title": "Register New User",
                                    "description": "POST /auth/register",
                                    "node_type": "basic",
                                    "parent_id": 7,
                                    "github_url": "https://github.com/f1sherFM/bookstore-api-course/blob/main/bookstore/routers/users.py",
                                    "children": []
                                },
                                {
                                    "id": 9,
                                    "title": "Login & Get JWT Token",
                                    "description": "POST /auth/login",
                                    "node_type": "basic",
                                    "parent_id": 7,
                                    "github_url": "https://github.com/f1sherFM/bookstore-api-course/blob/main/bookstore/auth.py",
                                    "children": []
                                }
                            ]
                        },
                        {
                            "id": 10,
                            "title": "Core Operations",
                            "description": "Essential API operations for books and users",
                            "node_type": "basic",
                            "parent_id": 6,
                            "github_url": "https://github.com/f1sherFM/bookstore-api-course/blob/main/bookstore/routers",
                            "children": [
                                {
                                    "id": 11,
                                    "title": "List Books with Pagination",
                                    "description": "GET /api/v1/books/?page=1&size=10",
                                    "node_type": "basic",
                                    "parent_id": 10,
                                    "github_url": "https://github.com/f1sherFM/bookstore-api-course/blob/main/bookstore/routers/books.py",
                                    "children": []
                                },
                                {
                                    "id": 12,
                                    "title": "Search Books",
                                    "description": "GET /api/v1/books/?q=python",
                                    "node_type": "basic",
                                    "parent_id": 10,
                                    "github_url": "https://github.com/f1sherFM/bookstore-api-course/blob/main/bookstore/routers/books.py",
                                    "children": []
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 13,
                    "title": "👨‍💻 Developer (2 hours)",
                    "description": "Understand the codebase and make your first contribution",
                    "node_type": "intermediate",
                    "parent_id": 1,
                    "github_url": "https://github.com/f1sherFM/bookstore-api-course#-developer-2-hours",
                    "children": [
                        {
                            "id": 14,
                            "title": "Code Structure",
                            "description": "Explore the FastAPI application architecture",
                            "node_type": "intermediate",
                            "parent_id": 13,
                            "github_url": "https://github.com/f1sherFM/bookstore-api-course/blob/main/PROJECT_STRUCTURE.md",
                            "children": [
                                {
                                    "id": 15,
                                    "title": "Main Application",
                                    "description": "FastAPI app setup and configuration",
                                    "node_type": "intermediate",
                                    "parent_id": 14,
                                    "github_url": "https://github.com/f1sherFM/bookstore-api-course/blob/main/bookstore/main.py",
                                    "children": []
                                },
                                {
                                    "id": 16,
                                    "title": "Database Models",
                                    "description": "SQLAlchemy models for books, users, reviews",
                                    "node_type": "intermediate",
                                    "parent_id": 14,
                                    "github_url": "https://github.com/f1sherFM/bookstore-api-course/blob/main/bookstore/models.py",
                                    "children": []
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 17,
                    "title": "☸️ DevOps Engineer (3 hours)",
                    "description": "Master the complete DevOps pipeline and infrastructure",
                    "node_type": "advanced",
                    "parent_id": 1,
                    "github_url": "https://github.com/f1sherFM/bookstore-api-course#️-devops-engineer-3-hours",
                    "children": [
                        {
                            "id": 18,
                            "title": "Docker Deployment",
                            "description": "Containerized deployment with Docker Compose",
                            "node_type": "advanced",
                            "parent_id": 17,
                            "github_url": "https://github.com/f1sherFM/bookstore-api-course/tree/main/deployment/docker",
                            "children": []
                        },
                        {
                            "id": 19,
                            "title": "Kubernetes Deployment",
                            "description": "Cloud-native deployment with Kubernetes",
                            "node_type": "advanced",
                            "parent_id": 17,
                            "github_url": "https://github.com/f1sherFM/bookstore-api-course/tree/main/deployment/k8s",
                            "children": []
                        }
                    ]
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
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📚 BookStore API Learning Roadmap</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: 700;
            }
            
            .header p {
                font-size: 1.2em;
                opacity: 0.9;
            }
            
            .roadmap-container {
                padding: 40px;
            }
            
            .loading {
                text-align: center;
                padding: 40px;
                font-size: 1.2em;
                color: #666;
            }
            
            .roadmap-tree {
                margin-top: 20px;
            }
            
            .node {
                margin: 15px 0;
                border: 2px solid #e1e8ed;
                border-radius: 12px;
                background: white;
                transition: all 0.3s ease;
                overflow: hidden;
            }
            
            .node:hover {
                border-color: #3498db;
                box-shadow: 0 8px 25px rgba(52, 152, 219, 0.15);
                transform: translateY(-2px);
            }
            
            .node-header {
                padding: 20px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: #f8f9fa;
                border-bottom: 1px solid #e1e8ed;
            }
            
            .node-content {
                flex: 1;
            }
            
            .node-title {
                font-size: 1.3em;
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 5px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .node-description {
                color: #666;
                font-size: 0.95em;
                line-height: 1.4;
            }
            
            .node-actions {
                display: flex;
                gap: 10px;
                align-items: center;
            }
            
            .github-link {
                background: #24292e;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                text-decoration: none;
                font-size: 0.9em;
                font-weight: 500;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 5px;
            }
            
            .github-link:hover {
                background: #0366d6;
                transform: scale(1.05);
            }
            
            .expand-btn {
                background: #3498db;
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 0.9em;
                transition: all 0.2s ease;
            }
            
            .expand-btn:hover {
                background: #2980b9;
            }
            
            .children {
                padding: 0 0 0 40px;
                background: #fafbfc;
                display: none;
            }
            
            .children.expanded {
                display: block;
            }
            
            .node-type-badge {
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.8em;
                font-weight: 500;
                text-transform: uppercase;
            }
            
            .node-type-root {
                background: #e74c3c;
                color: white;
            }
            
            .node-type-basic {
                background: #2ecc71;
                color: white;
            }
            
            .node-type-intermediate {
                background: #f39c12;
                color: white;
            }
            
            .node-type-advanced {
                background: #9b59b6;
                color: white;
            }
            
            .stats {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 12px;
                margin-bottom: 30px;
                display: flex;
                justify-content: space-around;
                text-align: center;
            }
            
            .stat {
                flex: 1;
            }
            
            .stat-number {
                font-size: 2em;
                font-weight: 700;
                color: #3498db;
            }
            
            .stat-label {
                color: #666;
                font-size: 0.9em;
                margin-top: 5px;
            }
            
            @media (max-width: 768px) {
                .container {
                    margin: 10px;
                    border-radius: 15px;
                }
                
                .header {
                    padding: 30px 20px;
                }
                
                .header h1 {
                    font-size: 2em;
                }
                
                .roadmap-container {
                    padding: 20px;
                }
                
                .children {
                    padding-left: 20px;
                }
                
                .stats {
                    flex-direction: column;
                    gap: 15px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📚 BookStore API Learning Roadmap</h1>
                <p>Production-ready FastAPI system - from beginner to DevOps expert</p>
            </div>
            
            <div class="roadmap-container">
                <div class="stats">
                    <div class="stat">
                        <div class="stat-number" id="total-nodes">0</div>
                        <div class="stat-label">Learning Topics</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number" id="github-links">0</div>
                        <div class="stat-label">GitHub Links</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">5</div>
                        <div class="stat-label">Learning Paths</div>
                    </div>
                </div>
                
                <div class="loading" id="loading">
                    🔄 Loading roadmap data...
                </div>
                
                <div class="roadmap-tree" id="roadmap-tree" style="display: none;">
                </div>
            </div>
        </div>
        
        <script>
            let totalNodes = 0;
            let githubLinks = 0;
            
            function countNodes(nodes) {
                let count = 0;
                let links = 0;
                
                nodes.forEach(node => {
                    count++;
                    if (node.github_url) links++;
                    if (node.children && node.children.length > 0) {
                        const childStats = countNodes(node.children);
                        count += childStats.count;
                        links += childStats.links;
                    }
                });
                
                return { count, links };
            }
            
            function createNodeElement(node, level = 0) {
                const nodeDiv = document.createElement('div');
                nodeDiv.className = 'node';
                nodeDiv.style.marginLeft = level * 20 + 'px';
                
                const hasChildren = node.children && node.children.length > 0;
                
                nodeDiv.innerHTML = `
                    <div class="node-header" onclick="toggleNode(this)">
                        <div class="node-content">
                            <div class="node-title">
                                ${node.title}
                                <span class="node-type-badge node-type-${node.node_type}">${node.node_type}</span>
                            </div>
                            <div class="node-description">${node.description}</div>
                        </div>
                        <div class="node-actions">
                            ${node.github_url ? `<a href="${node.github_url}" target="_blank" class="github-link" onclick="event.stopPropagation()">
                                <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                                </svg>
                                View Code
                            </a>` : ''}
                            ${hasChildren ? `<button class="expand-btn" onclick="event.stopPropagation(); toggleChildren(this)">
                                <span class="expand-text">Expand</span>
                            </button>` : ''}
                        </div>
                    </div>
                    ${hasChildren ? `<div class="children"></div>` : ''}
                `;
                
                if (hasChildren) {
                    const childrenContainer = nodeDiv.querySelector('.children');
                    node.children.forEach(child => {
                        childrenContainer.appendChild(createNodeElement(child, level + 1));
                    });
                }
                
                return nodeDiv;
            }
            
            function toggleChildren(button) {
                const node = button.closest('.node');
                const children = node.querySelector('.children');
                const expandText = button.querySelector('.expand-text');
                
                if (children.classList.contains('expanded')) {
                    children.classList.remove('expanded');
                    expandText.textContent = 'Expand';
                    button.style.background = '#3498db';
                } else {
                    children.classList.add('expanded');
                    expandText.textContent = 'Collapse';
                    button.style.background = '#e74c3c';
                }
            }
            
            function toggleNode(header) {
                // This function can be used for additional node interactions
            }
            
            // Load roadmap data
            fetch('/api/v1/roadmap')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('roadmap-tree').style.display = 'block';
                    
                    const stats = countNodes(data.data);
                    document.getElementById('total-nodes').textContent = stats.count;
                    document.getElementById('github-links').textContent = stats.links;
                    
                    const treeContainer = document.getElementById('roadmap-tree');
                    data.data.forEach(rootNode => {
                        treeContainer.appendChild(createNodeElement(rootNode));
                    });
                })
                .catch(error => {
                    console.error('Error loading roadmap:', error);
                    document.getElementById('loading').innerHTML = '❌ Failed to load roadmap data';
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