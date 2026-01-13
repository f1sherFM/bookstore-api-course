"""Script to recreate database with new schema."""

import os
from app import create_app, db

# Remove old database files
for db_file in ['roadmap.db', 'roadmap_dev.db']:
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Removed {db_file}")

# Create new database
app = create_app('development')
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
    
    # Seed data
    from app.utils.seed_data import create_python_roadmap
    create_python_roadmap()
    print("Seed data added successfully!")

print("Database recreation completed!")