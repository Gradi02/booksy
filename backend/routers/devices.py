from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user, get_db

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("", response_model=list[schemas.DeviceOut])
def list_devices(
    db: Session = Depends(get_db), _: models.User = Depends(get_current_user)
):
    """Get all devices."""
    return db.query(models.Device).order_by(models.Device.id.asc()).all()


@router.get("/{device_id}", response_model=schemas.DeviceOut)
def get_device(
    device_id: int, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)
):
    """Get a specific device by ID."""
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("", response_model=schemas.DeviceOut, status_code=201)
def create_device(
    payload: schemas.DeviceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Create a new device (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    device = models.Device(**payload.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@router.put("/{device_id}", response_model=schemas.DeviceOut)
def update_device(
    device_id: int,
    payload: schemas.DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Update a device (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


@router.patch("/{device_id}/status/{status_value}", response_model=schemas.DeviceOut)
def toggle_device_status(
    device_id: int,
    status_value: models.DeviceStatus,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Update a device's status (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    device.status = status_value
    db.commit()
    db.refresh(device)
    return device


@router.delete("/{device_id}", status_code=204)
def delete_device(
    device_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    """Delete a device (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()
