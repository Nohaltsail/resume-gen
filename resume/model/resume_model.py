from typing import Optional, List

from pydantic import BaseModel

from resume.model.resume_item import Experience, Education, Skill, Project, Language, Honor


class ResumeData(BaseModel):
    id: Optional[int] = None
    resume_id: Optional[str] = None
    name: Optional[str] = None
    photo: Optional[str] = None  # base64 字符串
    recruitment_type: Optional[str] = None
    job_title: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    self_evaluation: Optional[str] = None
    education: Optional[List[Education]]
    experience: Optional[List[Experience]]
    skills: Optional[List[Skill]]
    projects: Optional[List[Project]]
    languages: Optional[List[Language]]
    honors: Optional[List[Honor]]
    template: Optional[str] = "modern"


class ResumeRes(BaseModel):
    id: Optional[int] = None
    resume_id: Optional[str] = None
    name: Optional[str] = None
    recruitment_type: Optional[str] = None
    job_title: Optional[str] = None
    data: Optional[str] = None
    style: Optional[str] = "modern"


class ResumePdfRes(BaseModel):
    name: str
    path: Optional[str] = None
    content: Optional[str] = ''


