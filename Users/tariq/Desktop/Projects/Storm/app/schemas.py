from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from .models import UserRole, SubscriptionStatus, SubscriptionPlan

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    role: UserRole
    avatar_url: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# Subscription Schemas
class SubscriptionBase(BaseModel):
    plan: SubscriptionPlan

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    plan: Optional[SubscriptionPlan] = None
    status: Optional[SubscriptionStatus] = None

class SubscriptionResponse(SubscriptionBase):
    id: int
    user_id: int
    status: SubscriptionStatus
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Project Schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# API Key Schemas
class APIKeyBase(BaseModel):
    name: str
    project_id: Optional[int] = None

class APIKeyCreate(APIKeyBase):
    pass

class APIKeyResponse(APIKeyBase):
    id: int
    key_preview: str  # Only show first 8 characters
    is_active: bool
    last_used: Optional[datetime] = None
    usage_count: int
    rate_limit: int
    created_at: datetime
    expires_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class APIKeyCreateResponse(APIKeyResponse):
    api_key: str  # Full key only shown once during creation

# Dashboard Schemas
class DashboardStats(BaseModel):
    total_projects: int
    total_api_calls: int
    active_api_keys: int
    current_plan: SubscriptionPlan
    usage_this_month: int
    plan_limit: int

class UsageStats(BaseModel):
    date: str
    requests: int
    errors: int
    avg_response_time: float

class DashboardData(BaseModel):
    stats: DashboardStats
    recent_usage: List[UsageStats]
    recent_projects: List[ProjectResponse]

# Notification Schemas
class NotificationBase(BaseModel):
    title: str
    message: str
    notification_type: str = "info"

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationResponse(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Generic Response Schemas
class MessageResponse(BaseModel):
    message: str

class PaginatedResponse(BaseModel):
    items: List[BaseModel]
    total: int
    page: int
    size: int
    pages: int

# Error Schemas
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None