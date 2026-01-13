"""Marshmallow schemas for Node serialization."""

from marshmallow import Schema, fields


class NodeSchema(Schema):
    """Schema for Node model with nested children support."""
    
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String(allow_none=True)
    node_type = fields.String(required=True)
    parent_id = fields.Integer(allow_none=True)
    github_url = fields.String(allow_none=True)
    children = fields.Nested('self', many=True, dump_only=True)
    
    def dump_nested_tree(self, obj, **kwargs):
        """Dump node with all nested children as a tree structure."""
        if isinstance(obj, list):
            return [self._dump_single_node(node) for node in obj]
        return self._dump_single_node(obj)
    
    def _dump_single_node(self, node):
        """Dump a single node with its children recursively."""
        result = {
            'id': node.id,
            'title': node.title,
            'description': node.description,
            'node_type': node.node_type,
            'parent_id': node.parent_id,
            'github_url': node.github_url,
            'children': []
        }
        
        # Recursively add children
        for child in node.children.all():
            result['children'].append(self._dump_single_node(child))
        
        return result


# Schema instances
node_schema = NodeSchema()
nodes_schema = NodeSchema(many=True)