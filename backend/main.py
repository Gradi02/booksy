from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
import schemas
from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_db,
)
from database import Base, engine
from seed_loader import initialize_data


app = FastAPI(title="Booksy Inventory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        initialize_data(db)
    finally:
        db.close()


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=schemas.UserInDB)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.get("/devices", response_model=list[schemas.DeviceOut])
def list_devices(
    db: Session = Depends(get_db), _: models.User = Depends(get_current_user)
):
    return db.query(models.Device).order_by(models.Device.id.asc()).all()


@app.get("/devices/{device_id}", response_model=schemas.DeviceOut)
def get_device(
    device_id: int, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)
):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@app.post("/devices", response_model=schemas.DeviceOut, status_code=201)
def create_device(
    payload: schemas.DeviceCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    device = models.Device(**payload.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@app.put("/devices/{device_id}", response_model=schemas.DeviceOut)
def update_device(
    device_id: int,
    payload: schemas.DeviceUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


@app.delete("/devices/{device_id}", status_code=204)
def delete_device(
    device_id: int, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)
):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()
