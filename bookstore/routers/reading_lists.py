"""
Router for working with reading lists
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import ReadingList, ReadingListItem, Book, User as UserModel
from ..schemas import (
    ReadingList as ReadingListSchema,
    ReadingListCreate, ReadingListUpdate,
    ReadingListItemCreate
)
from ..auth import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[ReadingListSchema])
async def get_reading_lists(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Get current user's reading lists"""
    reading_lists = db.query(ReadingList).options(
        joinedload(ReadingList.user),
        joinedload(ReadingList.items).joinedload(ReadingListItem.book)
    ).filter(ReadingList.user_id == current_user.id).all()
    
    return reading_lists


@router.get("/public", response_model=List[ReadingListSchema])
async def get_public_reading_lists(db: Session = Depends(get_db)):
    """Get public reading lists"""
    reading_lists = db.query(ReadingList).options(
        joinedload(ReadingList.user),
        joinedload(ReadingList.items).joinedload(ReadingListItem.book)
    ).filter(ReadingList.is_public == True).all()
    
    return reading_lists


@router.get("/{list_id}", response_model=ReadingListSchema)
async def get_reading_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Get reading list by ID"""
    reading_list = db.query(ReadingList).options(
        joinedload(ReadingList.user),
        joinedload(ReadingList.items).joinedload(ReadingListItem.book)
    ).filter(ReadingList.id == list_id).first()
    
    if not reading_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading list not found"
        )
    
    # Check access permissions
    if (reading_list.user_id != current_user.id and 
        not reading_list.is_public and 
        not current_user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return reading_list


@router.post("/", response_model=ReadingListSchema, status_code=status.HTTP_201_CREATED)
async def create_reading_list(
    list_data: ReadingListCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Create reading list"""
    reading_list_dict = list_data.model_dump()
    reading_list_dict["user_id"] = current_user.id
    
    reading_list = ReadingList(**reading_list_dict)
    db.add(reading_list)
    db.commit()
    db.refresh(reading_list)
    
    return reading_list


@router.put("/{list_id}", response_model=ReadingListSchema)
async def update_reading_list(
    list_id: int,
    list_data: ReadingListUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Update reading list"""
    reading_list = db.query(ReadingList).filter(ReadingList.id == list_id).first()
    if not reading_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading list not found"
        )
    
    # Check access permissions
    if reading_list.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    update_data = list_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(reading_list, field, value)
    
    db.commit()
    db.refresh(reading_list)
    return reading_list


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reading_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Delete reading list"""
    reading_list = db.query(ReadingList).filter(ReadingList.id == list_id).first()
    if not reading_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading list not found"
        )
    
    # Check access permissions
    if reading_list.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(reading_list)
    db.commit()
    return None


@router.post("/{list_id}/books", status_code=status.HTTP_201_CREATED)
async def add_book_to_list(
    list_id: int,
    item_data: ReadingListItemCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Add book to reading list"""
    
    # Check list exists
    reading_list = db.query(ReadingList).filter(ReadingList.id == list_id).first()
    if not reading_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading list not found"
        )
    
    # Check access permissions
    if reading_list.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check book exists
    book = db.query(Book).filter(Book.id == item_data.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Check book not already in list
    existing_item = db.query(ReadingListItem).filter(
        ReadingListItem.reading_list_id == list_id,
        ReadingListItem.book_id == item_data.book_id
    ).first()
    
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book already in reading list"
        )
    
    # Add book to list
    item_dict = item_data.model_dump()
    item_dict["reading_list_id"] = list_id
    
    item = ReadingListItem(**item_dict)
    db.add(item)
    db.commit()
    
    return {"message": "Book added to reading list successfully"}


@router.delete("/{list_id}/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_book_from_list(
    list_id: int,
    book_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Remove book from reading list"""
    
    # Check list exists
    reading_list = db.query(ReadingList).filter(ReadingList.id == list_id).first()
    if not reading_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading list not found"
        )
    
    # Check access permissions
    if reading_list.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Find list item
    item = db.query(ReadingListItem).filter(
        ReadingListItem.reading_list_id == list_id,
        ReadingListItem.book_id == book_id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found in reading list"
        )
    
    db.delete(item)
    db.commit()
    return None