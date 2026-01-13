"""Node model for roadmap tree structure."""

from app import db
from sqlalchemy.orm import relationship, backref


class Node(db.Model):
    """Node model representing roadmap items in a tree structure."""
    
    __tablename__ = 'nodes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    node_type = db.Column(db.String(50), nullable=False, default='basic')
    parent_id = db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=True)
    github_url = db.Column(db.String(500), nullable=True)
    
    # Self-referential relationship
    children = relationship(
        'Node',
        backref=backref('parent', remote_side=[id]),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __init__(self, title, description=None, node_type='basic', parent_id=None, github_url=None):
        """Initialize Node instance."""
        self.title = title
        self.description = description
        self.node_type = node_type
        self.parent_id = parent_id
        self.github_url = github_url
    
    def __repr__(self):
        """String representation of Node."""
        return f'<Node {self.id}: {self.title}>'
    
    def to_dict(self, include_children=True):
        """Convert node to dictionary with optional children."""
        result = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'node_type': self.node_type,
            'parent_id': self.parent_id,
            'github_url': self.github_url
        }
        
        if include_children:
            result['children'] = [
                child.to_dict(include_children=True) 
                for child in self.children.all()
            ]
        
        return result
    
    @classmethod
    def get_root_nodes(cls):
        """Get all root nodes (nodes without parent)."""
        return cls.query.filter_by(parent_id=None).all()
    
    def get_all_descendants(self):
        """Get all descendants of this node recursively."""
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants
    
    def get_depth(self):
        """Get the depth of this node in the tree (root = 0)."""
        if self.parent_id is None:
            return 0
        return self.parent.get_depth() + 1