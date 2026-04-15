from datetime import date

from pydantic import BaseModel

from models import DeviceStatus


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(BaseModel):
    id: int
    username: str
    is_admin: bool

    class Config:
        from_attributes = True


class DeviceBase(BaseModel):
    name: str
    brand: str | None = None
    purchase_date: date | None = None
    status: DeviceStatus = DeviceStatus.AVAILABLE
    notes: str | None = None
    assigned_to: str | None = None
    history: str | None = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: str | None = None
    brand: str | None = None
    purchase_date: date | None = None
    status: DeviceStatus | None = None
    notes: str | None = None
    assigned_to: str | None = None
    history: str | None = None


class DeviceOut(DeviceBase):
    id: int

    class Config:
        from_attributes = True

    class Config:
        from_attributes = True
