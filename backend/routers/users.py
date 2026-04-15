from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user, get_db, get_password_hash

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[schemas.UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get all users (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return db.query(models.User).order_by(models.User.id.asc()).all()


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get a specific user by ID (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=schemas.UserOut, status_code=201)
def create_user(
    payload: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Create a new user (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Check if username already exists
    existing_user = db.query(models.User).filter(models.User.username == payload.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")
    
    new_user = models.User(
        username=payload.username,
        hashed_password=get_password_hash(payload.password),
        is_admin=payload.is_admin,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    payload: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Update a user (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    updates = payload.model_dump(exclude_unset=True)
    
    # Hash password if updating it
    if "password" in updates and updates["password"]:
        updates["hashed_password"] = get_password_hash(updates["password"])
        del updates["password"]
    
    for field, value in updates.items():
        if field != "password":  # Skip password field
            setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Delete a user (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Prevent deleting self
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
