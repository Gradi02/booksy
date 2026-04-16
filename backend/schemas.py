from datetime import date
from pydantic import BaseModel, ConfigDict, field_validator

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

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool = False
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        # Default admin user is allowed without @booksy.com
        if v == 'admin':
            return v
        if not v.endswith('@booksy.com'):
            raise ValueError('Username must end with @booksy.com (except admin)')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    is_admin: bool | None = None
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if v is None:
            return v
        # Default admin user is allowed without @booksy.com
        if v == 'admin':
            return v
        if not v.endswith('@booksy.com'):
            raise ValueError('Username must end with @booksy.com (except admin)')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


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

    model_config = ConfigDict(from_attributes=True)


class AICommand(BaseModel):
    """Structured command from AI for frontend actions"""
    action: str  # "filter", "sort", "search", "click", "navigate"
    target: str | None = None  # target field/button (e.g., "status", "sort_by", "device_id_5")
    value: str | None = None  # value for the action (e.g., "Available", "date", "delete")
    description: str | None = None  # human-readable description


class AIResponse(BaseModel):
    """Response from AI endpoint containing commands and explanation"""
    explanation: str  # Human-readable explanation
    commands: list[AICommand] = []  # List of actions to execute
    success: bool = True
