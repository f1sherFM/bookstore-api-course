# Flask Roadmap API

A Flask-based REST API for managing and displaying roadmap data in a tree structure, designed for the BookStore API project roadmap.

## 🌟 Features

- **Tree Structure**: Hierarchical roadmap data with parent-child relationships
- **REST API**: Clean API endpoints for roadmap data
- **Nested JSON**: Returns roadmap data as nested JSON with children
- **Seed Data**: Includes Python roadmap example data based on roadmap.sh
- **Error Handling**: Comprehensive error handling and validation
- **CORS Support**: Cross-origin resource sharing enabled
- **Demo Interface**: Interactive web interface to test the API
- **Vercel Ready**: Configured for deployment on Vercel

## 🔗 GitHub Integration

Each roadmap item now includes direct links to the corresponding files and directories in the [BookStore API repository](https://github.com/f1sherFM/bookstore-api-course). When you click on any roadmap item, you'll be taken directly to the relevant code examples, documentation, or implementation files.

### Interactive Roadmap Features

- **Clickable Items**: Every roadmap node links to specific GitHub files
- **Visual Indicators**: GitHub link icons show which items are clickable
- **Direct Navigation**: Jump straight from learning topics to code examples
- **Real Code Examples**: See actual implementation in the BookStore API project

### GitHub URL Mapping

The roadmap intelligently maps learning topics to relevant repository content:

- **Basic Syntax** → Core application files (`bookstore/models.py`, `bookstore/schemas.py`)
- **Data Structures** → Implementation examples in routers and models
- **OOP Concepts** → Class definitions and inheritance examples
- **Advanced Topics** → Advanced patterns in authentication and database handling
- **Testing** → Complete test suite with different testing strategies
- **DevOps** → Docker, Kubernetes, and CI/CD configurations

## 🚀 Quick Start

### Local Development

1. **Clone or create the project directory**:
   ```bash
   cd roadmap-site
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

### Demo Interface

Visit `http://localhost:5000` to see the interactive demo interface with:
- API endpoint testing buttons
- Interactive roadmap tree visualization
- Real-time API responses

## 📁 Project Structure

```
roadmap-site/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── node.py          # Node model with tree structure
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── node_schema.py   # Marshmallow schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   └── api.py           # API endpoints
│   └── utils/
│       ├── __init__.py
│       └── seed_data.py     # Python roadmap seed data
├── static/
│   └── index.html           # Demo interface
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── vercel.json             # Vercel deployment config
└── README.md               # This file
```

## 🔌 API Endpoints

### GET /api/v1/roadmap
Returns the complete roadmap tree structure with nested children.

**Response Example**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Python Developer Roadmap",
      "description": "Complete roadmap for becoming a Python developer",
      "node_type": "root",
      "parent_id": null,
      "children": [
        {
          "id": 2,
          "title": "Basic Syntax",
          "description": "Learn Python basic syntax and fundamentals",
          "node_type": "basic",
          "parent_id": 1,
          "children": [
            {
              "id": 3,
              "title": "Variables",
              "description": "Learn about variables and data types",
              "node_type": "basic",
              "parent_id": 2,
              "children": []
            }
          ]
        }
      ]
    }
  ],
  "message": "Roadmap retrieved successfully"
}
```

### GET /api/v1/nodes
Returns all nodes in a flat structure (for debugging).

### GET /api/v1/nodes/{id}
Returns a specific node with its children.

### GET /api/v1/health
Health check endpoint with database status.

## 🏷️ Node Types

- **root**: Top-level roadmap nodes
- **basic**: Beginner-level topics
- **intermediate**: Intermediate-level topics  
- **advanced**: Advanced-level topics

## 🗄️ Database Schema

The `Node` model has the following fields:

- `id`: Primary key (Integer)
- `title`: Node title (String, required)
- `description`: Node description (Text, optional)
- `node_type`: Type of node (String, required)
- `parent_id`: Foreign key to parent node (Integer, nullable for root nodes)

## 🌱 Seed Data

The application includes Python roadmap seed data based on roadmap.sh structure:

- **Basic Syntax**: Variables, Data Types, Operators, Control Structures, Functions, Comments
- **Data Structures**: Lists, Tuples, Dictionaries, Sets, Strings
- **Object-Oriented Programming**: Classes, Inheritance, Polymorphism, Encapsulation, Abstract Classes
- **Advanced Topics**: Decorators, Generators, Context Managers, Metaclasses, Async/Await
- **Libraries and Frameworks**: 
  - Web Frameworks: Flask, Django, FastAPI
  - Data Science: NumPy, Pandas, Matplotlib, Scikit-learn
- **Testing**: Unit Testing, Pytest, Mocking, Test Coverage

## 🚀 Deployment

### Vercel Deployment

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy to Vercel**:
   ```bash
   vercel
   ```

3. **Configure environment variables** (if needed):
   ```bash
   vercel env add FLASK_ENV production
   ```

### Manual Deployment

For production deployment on other platforms:

1. **Set environment variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   export DATABASE_URL=your-database-url
   ```

2. **Use a production WSGI server like Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

## 🛠️ Development

### Adding New Roadmap Data

1. **Create nodes in the database using the Node model**:
   ```python
   from app.models.node import Node
   from app import db
   
   # Create a new root node
   root = Node(title="New Roadmap", description="Description", node_type="root")
   db.session.add(root)
   db.session.commit()
   
   # Create child nodes
   child = Node(title="Child Topic", description="Child description", 
                node_type="basic", parent_id=root.id)
   db.session.add(child)
   db.session.commit()
   ```

2. **Set appropriate parent_id for hierarchical structure**
3. **Use different node_types to categorize difficulty**

### Extending the API

- **Add new endpoints** in `app/routes/api.py`
- **Create new models** in `app/models/`
- **Add corresponding schemas** in `app/schemas/`

### Testing the API

Use the demo interface at `http://localhost:5000` or test endpoints directly:

```bash
# Health check
curl http://localhost:5000/api/v1/health

# Get roadmap tree
curl http://localhost:5000/api/v1/roadmap

# Get all nodes (flat)
curl http://localhost:5000/api/v1/nodes

# Get specific node
curl http://localhost:5000/api/v1/nodes/1
```

## 🔧 Error Handling

The API includes comprehensive error handling:

- **404 errors** for missing resources
- **500 errors** for server issues
- **Validation errors** for invalid data
- **Database connection error handling**

All errors return JSON responses with consistent structure:

```json
{
  "success": false,
  "error": "Error type",
  "message": "Human-readable error message"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🎯 Use Cases

This roadmap API is perfect for:

- **Learning platforms** showing skill progression paths
- **Project documentation** displaying feature development roadmaps
- **Educational content** organizing curriculum structures
- **Team planning** visualizing project milestones
- **Knowledge bases** structuring hierarchical information

## 🔗 Related Projects

This roadmap API was created for the [BookStore API project](https://github.com/f1sherFM/bookstore-api-course) to display the development roadmap and help users understand the learning path for modern Python development with FastAPI, Docker, and DevOps practices.