"""API routes for roadmap endpoints."""

from flask import Blueprint, jsonify, request
from app.models.node import Node
from app.schemas.node_schema import node_schema, nodes_schema
from app import db

api_bp = Blueprint('api', __name__)


@api_bp.route('/roadmap', methods=['GET'])
def get_roadmap():
    """
    Get roadmap tree structure.
    
    Returns only root nodes with their nested children.
    """
    try:
        # Get all root nodes (nodes without parent)
        root_nodes = Node.get_root_nodes()
        
        if not root_nodes:
            return jsonify({
                'success': True,
                'data': [],
                'message': 'No roadmap data found'
            }), 200
        
        # Use schema to serialize with nested children
        result = []
        for root_node in root_nodes:
            result.append(node_schema.dump_nested_tree(root_node))
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Roadmap retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve roadmap'
        }), 500


@api_bp.route('/nodes', methods=['GET'])
def get_all_nodes():
    """Get all nodes (flat structure) for debugging purposes."""
    try:
        nodes = Node.query.all()
        result = []
        for node in nodes:
            result.append({
                'id': node.id,
                'title': node.title,
                'description': node.description,
                'node_type': node.node_type,
                'parent_id': node.parent_id,
                'github_url': node.github_url
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result),
            'message': 'All nodes retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve nodes'
        }), 500


@api_bp.route('/nodes/<int:node_id>', methods=['GET'])
def get_node(node_id):
    """Get a specific node with its children."""
    try:
        node = Node.query.get_or_404(node_id)
        result = node_schema.dump_nested_tree(node)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': f'Node {node_id} retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f'Failed to retrieve node {node_id}'
        }), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        node_count = Node.query.count()
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'database': 'connected',
            'node_count': node_count,
            'message': 'Roadmap API is running'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'message': 'Health check failed'
        }), 500


@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Resource not found',
        'message': 'The requested resource was not found'
    }), 404


@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An internal server error occurred'
    }), 500