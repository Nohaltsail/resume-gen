from typing import Optional
from pydantic import BaseModel


class Education(BaseModel):
    degree: str
    period: str
    school: str
    gpa: Optional[str] = None


class Experience(BaseModel):
    title: str
    period: str
    company: str
    location: Optional[str] = None
    description: Optional[str] = None


class Skill(BaseModel):
    name: str
    level: int


class Language(BaseModel):
    name: str
    level: str


class Honor(BaseModel):
    name: str
    period: str


class Project(BaseModel):
    name: str
    period: str
    description: Optional[str] = None


