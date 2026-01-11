"""
Router for working with genres
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Genre, User
from ..schemas import Genre as GenreSchema, GenreCreate, GenreUpdate
from ..auth import get_current_active_user, get_current_superuser

router = APIRouter()


@router.get("/", response_model=List[GenreSchema])
async def get_genres(db: Session = Depends(get_db)):
    """Get list of genres"""
    genres = db.query(Genre).all()
    return genres


@router.get("/{genre_id}", response_model=GenreSchema)
async def get_genre(genre_id: int, db: Session = Depends(get_db)):
    """Get genre by ID"""
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    return genre


@router.post("/", response_model=GenreSchema, status_code=status.HTTP_201_CREATED)
async def create_genre(
    genre_data: GenreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Create genre"""
    # Check name uniqueness
    existing_genre = db.query(Genre).filter(Genre.name == genre_data.name).first()
    if existing_genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Genre with this name already exists"
        )
    
    genre = Genre(**genre_data.model_dump())
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre


@router.put("/{genre_id}", response_model=GenreSchema)
async def update_genre(
    genre_id: int,
    genre_data: GenreUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Update genre"""
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    
    update_data = genre_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(genre, field, value)
    
    db.commit()
    db.refresh(genre)
    return genre


@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(
    genre_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Delete genre"""
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    
    db.delete(genre)
    db.commit()
    return None