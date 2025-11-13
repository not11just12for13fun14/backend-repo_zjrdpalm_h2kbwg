"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Hoodie Wala specific schemas

class Hoodie(BaseModel):
    """
    Hoodie products
    Collection name: "hoodie"
    """
    name: str = Field(..., description="Hoodie name")
    description: Optional[str] = Field(None, description="Hoodie description")
    price: float = Field(..., ge=0, description="Price")
    colors: List[str] = Field(default_factory=list, description="Available colors")
    sizes: List[str] = Field(default_factory=lambda: ["S","M","L","XL"], description="Available sizes")
    image_url: Optional[str] = Field(None, description="Image URL")
    in_stock: bool = Field(True, description="Stock availability")

class ContactMessage(BaseModel):
    """
    Contact form submissions
    Collection name: "contactmessage"
    """
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    phone: Optional[str] = Field(None, description="Phone number")
    message: str = Field(..., description="Message body")
