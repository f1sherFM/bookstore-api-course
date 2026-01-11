"""
Router for working with authors
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Author, User
from ..schemas import Author as AuthorSchema, AuthorCreate, AuthorUpdate
from ..auth import get_current_active_user, get_current_superuser

router = APIRouter()


@router.get("/", response_model=List[AuthorSchema])
async def get_authors(db: Session = Depends(get_db)):
    """Get list of authors"""
    authors = db.query(Author).all()
    return authors


@router.get("/{author_id}", response_model=AuthorSchema)
async def get_author(author_id: int, db: Session = Depends(get_db)):
    """Get author by ID"""
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    return author


@router.post("/", response_model=AuthorSchema, status_code=status.HTTP_201_CREATED)
async def create_author(
    author_data: AuthorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Create author"""
    author = Author(**author_data.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@router.put("/{author_id}", response_model=AuthorSchema)
async def update_author(
    author_id: int,
    author_data: AuthorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Update author"""
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    
    update_data = author_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(author, field, value)
    
    db.commit()
    db.refresh(author)
    return author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Delete author"""
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    
    db.delete(author)
    db.commit()
    return None