"""
Router for working with reviews
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Review, Book, User as UserModel
from ..schemas import Review as ReviewSchema, ReviewCreate, ReviewUpdate
from ..auth import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[ReviewSchema])
async def get_reviews(
    book_id: int = None,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """Get list of reviews with filtering"""
    query = db.query(Review).options(
        joinedload(Review.user),
        joinedload(Review.book)
    )
    
    if book_id:
        query = query.filter(Review.book_id == book_id)
    
    if user_id:
        query = query.filter(Review.user_id == user_id)
    
    reviews = query.all()
    return reviews


@router.get("/{review_id}", response_model=ReviewSchema)
async def get_review(review_id: int, db: Session = Depends(get_db)):
    """Get review by ID"""
    review = db.query(Review).options(
        joinedload(Review.user),
        joinedload(Review.book)
    ).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return review


@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Create review"""
    
    # Check book exists
    book = db.query(Book).filter(Book.id == review_data.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Check user hasn't already reviewed this book
    existing_review = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.book_id == review_data.book_id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this book"
        )
    
    # Create review
    review_dict = review_data.model_dump()
    review_dict["user_id"] = current_user.id
    
    review = Review(**review_dict)
    db.add(review)
    db.commit()
    db.refresh(review)
    
    return review


@router.put("/{review_id}", response_model=ReviewSchema)
async def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Update review"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Check access permissions
    if review.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    update_data = review_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(review, field, value)
    
    db.commit()
    db.refresh(review)
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Delete review"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Check access permissions
    if review.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(review)
    db.commit()
    return None