"""
Router for working with books
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func

from ..database import get_db
from ..models import Book, Author, Genre, Review
from ..schemas import (
    Book as BookSchema, BookCreate, BookUpdate, BookWithStats,
    BookSearchParams, BookSortBy, SortOrder, PaginatedResponse
)
from ..auth import get_current_active_user, get_current_superuser
from ..models import User

router = APIRouter()


def get_books_query(
    db: Session,
    search_params: Optional[BookSearchParams] = None,
    sort_by: BookSortBy = BookSortBy.CREATED_AT,
    sort_order: SortOrder = SortOrder.DESC
):
    """Base query for getting books with filtering and sorting"""
    query = db.query(Book).options(
        joinedload(Book.authors),
        joinedload(Book.genres)
    )
    
    if search_params:
        # Search by title and description
        if search_params.q:
            search_term = f"%{search_params.q}%"
            query = query.filter(
                or_(
                    Book.title.ilike(search_term),
                    Book.description.ilike(search_term)
                )
            )
        
        # Filter by author
        if search_params.author:
            query = query.join(Book.authors).filter(
                Author.name.ilike(f"%{search_params.author}%")
            )
        
        # Filter by genre
        if search_params.genre:
            query = query.join(Book.genres).filter(
                Genre.name.ilike(f"%{search_params.genre}%")
            )
        
        # Filter by price
        if search_params.min_price is not None:
            query = query.filter(Book.price >= search_params.min_price)
        
        if search_params.max_price is not None:
            query = query.filter(Book.price <= search_params.max_price)
        
        # Filter by language
        if search_params.language:
            query = query.filter(Book.language == search_params.language)
        
        # Only available books
        if search_params.available_only:
            query = query.filter(Book.is_available == True)
    
    # Sorting
    if sort_by == BookSortBy.TITLE:
        order_field = Book.title
    elif sort_by == BookSortBy.PRICE:
        order_field = Book.price
    elif sort_by == BookSortBy.PUBLICATION_DATE:
        order_field = Book.publication_date
    elif sort_by == BookSortBy.RATING:
        # Sorting by rating requires subquery
        avg_rating = db.query(func.avg(Review.rating)).filter(Review.book_id == Book.id).scalar_subquery()
        order_field = avg_rating
    else:
        order_field = Book.created_at
    
    if sort_order == SortOrder.DESC:
        query = query.order_by(order_field.desc())
    else:
        query = query.order_by(order_field.asc())
    
    return query


@router.get("/", response_model=List[BookSchema])
async def get_books(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Search query"),
    author: Optional[str] = Query(None, description="Author name"),
    genre: Optional[str] = Query(None, description="Genre"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    language: Optional[str] = Query(None, description="Language"),
    available_only: bool = Query(True, description="Only available books"),
    sort_by: BookSortBy = Query(BookSortBy.CREATED_AT, description="Sort field"),
    sort_order: SortOrder = Query(SortOrder.DESC, description="Sort order"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size")
):
    """Get list of books with search and filtering"""
    search_params = BookSearchParams(
        q=q, author=author, genre=genre,
        min_price=min_price, max_price=max_price,
        language=language, available_only=available_only
    )
    
    query = get_books_query(db, search_params, sort_by, sort_order)
    
    # Pagination
    offset = (page - 1) * size
    books = query.offset(offset).limit(size).all()
    
    return books


@router.get("/stats")
async def get_books_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get book statistics"""
    total_books = db.query(Book).count()
    available_books = db.query(Book).filter(Book.is_available == True).count()
    total_authors = db.query(Author).count()
    total_genres = db.query(Genre).count()
    
    # Average price
    avg_price = db.query(func.avg(Book.price)).filter(Book.price.isnot(None)).scalar()
    
    return {
        "total_books": total_books,
        "available_books": available_books,
        "total_authors": total_authors,
        "total_genres": total_genres,
        "average_price": round(avg_price, 2) if avg_price else None
    }


@router.get("/{book_id}", response_model=BookWithStats)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get book by ID"""
    book = db.query(Book).options(
        joinedload(Book.authors),
        joinedload(Book.genres),
        joinedload(Book.reviews)
    ).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Calculate statistics
    reviews = book.reviews
    review_count = len(reviews)
    average_rating = sum(review.rating for review in reviews) / review_count if review_count > 0 else None
    
    # Create object with additional fields
    book_dict = {
        **book.__dict__,
        "authors": book.authors,
        "genres": book.genres,
        "average_rating": average_rating,
        "review_count": review_count
    }
    
    return BookWithStats(**book_dict)


@router.post("/", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Create new book (superusers only)"""
    
    # Check authors exist
    authors = db.query(Author).filter(Author.id.in_(book_data.author_ids)).all()
    if len(authors) != len(book_data.author_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more authors not found"
        )
    
    # Check genres exist
    genres = db.query(Genre).filter(Genre.id.in_(book_data.genre_ids)).all()
    if len(genres) != len(book_data.genre_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more genres not found"
        )
    
    # Check ISBN uniqueness
    if book_data.isbn:
        existing_book = db.query(Book).filter(Book.isbn == book_data.isbn).first()
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with this ISBN already exists"
            )
    
    # Create book
    book_dict = book_data.model_dump(exclude={"author_ids", "genre_ids"})
    book = Book(**book_dict)
    
    # Add authors and genres
    book.authors = authors
    book.genres = genres
    
    db.add(book)
    db.commit()
    db.refresh(book)
    
    return book


@router.put("/{book_id}", response_model=BookSchema)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Update book (superusers only)"""
    
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Update fields
    update_data = book_data.model_dump(exclude_unset=True, exclude={"author_ids", "genre_ids"})
    
    for field, value in update_data.items():
        setattr(book, field, value)
    
    # Update authors if specified
    if book_data.author_ids is not None:
        authors = db.query(Author).filter(Author.id.in_(book_data.author_ids)).all()
        if len(authors) != len(book_data.author_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more authors not found"
            )
        book.authors = authors
    
    # Update genres if specified
    if book_data.genre_ids is not None:
        genres = db.query(Genre).filter(Genre.id.in_(book_data.genre_ids)).all()
        if len(genres) != len(book_data.genre_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more genres not found"
            )
        book.genres = genres
    
    db.commit()
    db.refresh(book)
    
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Delete book (superusers only)"""
    
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    db.delete(book)
    db.commit()
    
    return None