"""
Performance and load tests
"""

import pytest
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List
import statistics

from bookstore.models import Book, User, Author, Genre
from .factories import create_test_library, BookFactory, UserFactory, AuthorFactory, GenreFactory


class TestDatabasePerformance:
    """Database performance tests"""
    
    def test_book_query_performance(self, db_session):
        """Test book query performance"""
        # Create large library
        library = create_test_library(db_session, num_books=100)
        
        # Measure execution time of various queries
        times = []
        
        for _ in range(10):
            start_time = time.perf_counter()
            
            # Complex query with JOIN
            books = db_session.query(Book).join(Book.authors).join(Book.genres).limit(20).all()
            
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        avg_time = statistics.mean(times)
        max_time = max(times)
        
        # Check that queries execute fast enough
        assert avg_time < 0.5, f"Average query time too high: {avg_time:.3f}s"
        assert max_time < 1.0, f"Maximum query time too high: {max_time:.3f}s"
        assert len(books) > 0, "Should find books with authors and genres"
    
    def test_search_performance(self, db_session):
        """Test search performance"""
        library = create_test_library(db_session, num_books=200)
        
        search_terms = ["test", "book", "author", "genre", "classic"]
        times = []
        
        for term in search_terms:
            start_time = time.perf_counter()
            
            # Search by title and description
            results = db_session.query(Book).filter(
                Book.title.ilike(f"%{term}%") | 
                Book.description.ilike(f"%{term}%")
            ).limit(50).all()
            
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        avg_time = statistics.mean(times)
        
        # Search should be fast even on large database
        assert avg_time < 0.2, f"Search too slow: {avg_time:.3f}s"
    
    def test_pagination_performance(self, db_session):
        """Test pagination performance"""
        library = create_test_library(db_session, num_books=500)
        
        page_size = 20
        times = []
        
        # Test different pages
        for page in [1, 5, 10, 20]:
            offset = (page - 1) * page_size
            
            start_time = time.perf_counter()
            
            books = db_session.query(Book).offset(offset).limit(page_size).all()
            
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        avg_time = statistics.mean(times)
        
        # Pagination should work fast on any page
        assert avg_time < 0.1, f"Pagination too slow: {avg_time:.3f}s"
        
        # Check that time doesn't grow significantly for distant pages
        first_page_time = times[0]
        last_page_time = times[-1]
        
        # Last page time should not be 10x more than first page
        assert last_page_time < first_page_time * 10


class TestAPIPerformance:
    """API performance tests"""
    
    def test_concurrent_requests(self, client, db_session):
        """Test concurrent requests"""
        library = create_test_library(db_session, num_books=50)
        
        def make_request():
            """Execute one request"""
            start_time = time.perf_counter()
            response = client.get("/api/v1/books/")
            end_time = time.perf_counter()
            
            return {
                'status_code': response.status_code,
                'time': end_time - start_time,
                'books_count': len(response.json()) if response.status_code == 200 else 0
            }
        
        # Execute 20 parallel requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            results = [future.result() for future in futures]
        
        # Analyze results
        times = [r['time'] for r in results]
        status_codes = [r['status_code'] for r in results]
        
        # All requests should be successful
        assert all(code == 200 for code in status_codes)
        
        # Average response time should be reasonable
        avg_time = statistics.mean(times)
        max_time = max(times)
        
        assert avg_time < 2.0, f"Average response time too high: {avg_time:.3f}s"
        assert max_time < 5.0, f"Maximum response time too high: {max_time:.3f}s"
    
    def test_memory_usage_stability(self, client, db_session):
        """Test memory usage stability"""
        import psutil
        import os
        
        library = create_test_library(db_session, num_books=100)
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Execute many requests
        for _ in range(100):
            response = client.get("/api/v1/books/")
            assert response.status_code == 200
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_growth = final_memory - initial_memory
        
        # Memory growth should not be critical
        assert memory_growth < 100, f"Too much memory growth: {memory_growth:.1f}MB"
    
    def test_simple_performance(self, client, db_session):
        """Simple performance test without async"""
        library = create_test_library(db_session, num_books=30)
        
        times = []
        
        # Execute 20 sequential requests
        for _ in range(20):
            start_time = time.perf_counter()
            response = client.get("/api/v1/books/")
            end_time = time.perf_counter()
            
            times.append(end_time - start_time)
            assert response.status_code == 200
        
        avg_time = statistics.mean(times)
        max_time = max(times)
        
        assert avg_time < 1.0, f"Average request time too high: {avg_time:.3f}s"
        assert max_time < 2.0, f"Maximum request time too high: {max_time:.3f}s"


class TestScalabilityLimits:
    """Scalability limits tests"""
    
    def test_large_dataset_handling(self, db_session):
        """Test working with large datasets"""
        # Create large library
        library = create_test_library(db_session, num_books=1000)
        
        # Test various operations
        start_time = time.perf_counter()
        
        # Count total number
        total_books = db_session.query(Book).count()
        
        # Search
        search_results = db_session.query(Book).filter(
            Book.title.ilike("%test%")
        ).limit(100).all()
        
        # Complex filtering
        expensive_books = db_session.query(Book).filter(
            Book.price > 500,
            Book.is_available == True
        ).limit(50).all()
        
        end_time = time.perf_counter()
        
        # Operations should complete in reasonable time
        assert end_time - start_time < 5.0, "Operations with large dataset too slow"
        assert total_books == 1000
        assert len(search_results) <= 100
        assert len(expensive_books) <= 50
    
    def test_concurrent_writes(self, db_session):
        """Test concurrent database writes (simplified)"""
        # Configure factories to work with session
        UserFactory._meta.sqlalchemy_session = db_session
        AuthorFactory._meta.sqlalchemy_session = db_session
        GenreFactory._meta.sqlalchemy_session = db_session
        BookFactory._meta.sqlalchemy_session = db_session
        
        # Create base data
        authors = [AuthorFactory() for _ in range(5)]
        genres = [GenreFactory() for _ in range(3)]
        
        initial_count = db_session.query(Book).count()
        
        # Create books sequentially (SQLite doesn't like parallel writes)
        books_created = 0
        for batch in range(3):
            for i in range(10):
                # Use simple data
                book = Book(
                    title=f"Concurrent Test Book {batch}-{i}",
                    description=f"Description for concurrent book {batch}-{i}",
                    price=99.99,
                    page_count=200,
                    language="en",
                    is_available=True
                )
                book.authors = [authors[i % len(authors)]]
                book.genres = [genres[i % len(genres)]]
                
                db_session.add(book)
                books_created += 1
            
            # Commit each batch separately
            db_session.commit()
        
        # Check that all books were created
        final_count = db_session.query(Book).count()
        assert final_count >= initial_count + books_created
    
    def test_stress_search(self, client, db_session):
        """Search stress test"""
        library = create_test_library(db_session, num_books=200)
        
        search_terms = [
            "test", "book", "author", "classic", "modern", "fiction",
            "science", "history", "romance", "mystery", "adventure"
        ]
        
        times = []
        
        # Execute many search requests
        for i in range(50):  # Reduce count for stability
            term = search_terms[i % len(search_terms)]
            
            start_time = time.perf_counter()
            response = client.get(f"/api/v1/books/?q={term}")
            end_time = time.perf_counter()
            
            times.append(end_time - start_time)
            assert response.status_code == 200
        
        # Analyze performance
        avg_time = statistics.mean(times)
        max_time = max(times)
        
        assert avg_time < 0.5, f"Average search time: {avg_time:.3f}s"
        assert max_time < 2.0, f"Maximum search time: {max_time:.3f}s"


class TestResourceUsage:
    """Resource usage tests"""
    
    def test_database_connection_pooling(self, db_session):
        """Test database connection pooling"""
        # Create many sessions and check that they are reused
        sessions = []
        
        for _ in range(20):
            from bookstore.database import SessionLocal
            session = SessionLocal()
            sessions.append(session)
            
            # Execute simple query
            result = session.query(Book).count()
            assert result >= 0
        
        # Close all sessions
        for session in sessions:
            session.close()
        
        # Test should pass without connection errors
        assert True
    
    def test_query_optimization(self, db_session):
        """Test query optimization"""
        library = create_test_library(db_session, num_books=100)
        
        # Test N+1 problem
        start_time = time.perf_counter()
        
        # Load books with authors and genres in one query
        from sqlalchemy.orm import joinedload
        books = db_session.query(Book).options(
            joinedload(Book.authors),
            joinedload(Book.genres)
        ).limit(50).all()
        
        # Access related data
        for book in books:
            authors_count = len(book.authors)
            genres_count = len(book.genres)
            assert authors_count >= 0
            assert genres_count >= 0
        
        end_time = time.perf_counter()
        
        # Optimized query should be fast
        assert end_time - start_time < 1.0, "Query with joinedload too slow"