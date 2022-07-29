from typing import Optional
from sqlmodel import Field, SQLModel

class UserModel(SQLModel, table=True):
    __tablename__ = str = 'users'

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    full_name: str
    job_type: str
    phone: str
    email: str
    image: str
    country: str
    city: str
    onboarding_completion: int
