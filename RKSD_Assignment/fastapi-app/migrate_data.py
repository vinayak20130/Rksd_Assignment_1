import sqlite3
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.connection import Base
from app.models.candidate import Candidate
from app.models.application import Application
from app.models.opening import Opening
from app.models.role import Role
from app.models.stage import Stage
from app.models.experience import Experience

# Connect to the old database
old_conn = sqlite3.connect("test.db")
old_cursor = old_conn.cursor()

# Set up SQLAlchemy session for the new database
SQLALCHEMY_DATABASE_URL = "sqlite:///./fresh_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Function to convert string dates to Python datetime objects
def convert_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print(f"Could not parse date: {date_str}")
            return None

# Function to copy data for a specific table
def copy_table_data(table_name, model_class, id_column=None):
    print(f"\nCopying data for {table_name}...")
    
    # Get all rows from the old database
    try:
        old_cursor.execute(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in old_cursor.description]
        rows = old_cursor.fetchall()
        
        print(f"Found {len(rows)} rows in {table_name}")
        
        # For each row, create a new object in the new database
        success_count = 0
        error_count = 0
        
        for row in rows:
            # Create a dictionary mapping column names to values
            row_dict = dict(zip(columns, row))
            
            # Convert string date/time fields to datetime objects
            date_fields = ['created_at', 'updated_at', 'posted_date', 'deadline', 
                          'application_date', 'start_date', 'end_date']
            for field in date_fields:
                if field in row_dict and row_dict[field] is not None:
                    row_dict[field] = convert_date(row_dict[field])
            
            # Remove any columns that don't exist in the new model
            model_columns = [c.key for c in model_class.__table__.columns]
            row_dict = {k: v for k, v in row_dict.items() if k in model_columns}
            
            # Debug: Print what we're trying to insert
            if success_count == 0:  # Only print for the first row
                print(f"Sample row data (after conversion): {row_dict}")
            
            # Create and add the new object
            try:
                # Check if record already exists
                if id_column and row_dict.get(id_column):
                    existing = db.query(model_class).filter(
                        getattr(model_class, id_column) == row_dict[id_column]
                    ).first()
                    if existing:
                        print(f"Record with {id_column}={row_dict[id_column]} already exists, skipping.")
                        continue
                
                new_obj = model_class(**row_dict)
                db.add(new_obj)
                db.flush()  # Try to flush each object to catch errors early
                success_count += 1
            except Exception as e:
                error_count += 1
                print(f"Error inserting row {row_dict.get(id_column, 'unknown')}: {str(e)}")
                db.rollback()  # Rollback the current object only
        
        # Commit all successful inserts
        if success_count > 0:
            try:
                db.commit()
                print(f"Successfully copied {success_count} rows for {table_name}")
            except Exception as e:
                print(f"Error during final commit for {table_name}: {str(e)}")
                db.rollback()
        
        if error_count > 0:
            print(f"Failed to copy {error_count} rows for {table_name}")
            
    except Exception as e:
        print(f"Error accessing table {table_name}: {str(e)}")

# Start migration
try:
    # Start with tables that don't have foreign key dependencies
    copy_table_data("roles", Role, "role_id")
    copy_table_data("openings", Opening, "opening_id")
    copy_table_data("stages", Stage, "stage_id")
    
    # Then tables with dependencies
    copy_table_data("candidates", Candidate, "candidate_id")
    copy_table_data("applications", Application, "application_id")
    copy_table_data("experiences", Experience, "experience_id")
    
    print("\nData migration completed!")
except Exception as e:
    print(f"\nCritical error during data migration: {str(e)}")
finally:
    # Close connections
    old_conn.close()
    db.close()

# Verify counts in the new database
verify_conn = sqlite3.connect("fresh_db.db")
verify_cursor = verify_conn.cursor()
print("\n=== DATA VERIFICATION ===")
try:
    verify_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = verify_cursor.fetchall()
    for table in tables:
        table_name = table[0]
        verify_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = verify_cursor.fetchone()[0]
        print(f"Table {table_name}: {count} rows")
finally:
    verify_conn.close()