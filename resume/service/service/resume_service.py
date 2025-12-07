import json
import uuid

from avatar.photo import save_photo, get_photo, file_to_base64
from resume.common.logger import get_logger
from resume.model.resume_model import ResumeData, ResumePdfRes, ResumeRes
from resume.repository.dao.resume_dao import ResumeDao
from resume.common.decorators.application_context import ApplicationContext
from resume.common.base.base_serivce import BaseService
from resume.templates.generator import LatexGenerator

logger = get_logger()
latex_gen = LatexGenerator()


class ResumeService(BaseService):
    """
    resume服务类
    """

    def __init__(self):
        super().__init__()
        self.resume_dao = ApplicationContext.get(ResumeDao)

    def generate_pdf(self, resume_data: dict):
        data = ResumeData(**resume_data)
        if not resume_data.get('resume_id'):
            save_data = self.save_content(resume_data)
            data.resume_id = save_data.resume_id
            data.photo = save_data.photo
        else:
            data.photo = get_photo(resume_data.get('resume_id'))

        data.job_title = resume_data.get('jobTitle')
        data.self_evaluation = resume_data.get('selfEvaluation')
        data.recruitment_type = resume_data.get('recruitmentType')
        latex_content = latex_gen.generate_latex_content(data)
        pdf_path = latex_gen.compile_latex_to_pdf(data.resume_id, latex_content)
        return ResumePdfRes(
            name=data.name,
            path=pdf_path
        )

    def save_content(self, resume_data: dict):
        job_title = resume_data.get('jobTitle')
        recruitment_type = resume_data.get('recruitmentType')
        self_evaluation = resume_data.get('selfEvaluation')
        photo_base64 = resume_data.get('photo')
        resume_data = ResumeData(**resume_data)
        resume_id = str(uuid.uuid4())[:8]
        resume_data.resume_id = resume_id
        photo = save_photo(photo_base64, resume_id)
        resume_data.photo = photo
        data = {
                'phone': resume_data.phone,
                'email': resume_data.email,
                'address': resume_data.address,
                'educations': [item.model_dump() for item in resume_data.education],
                'experiences': [item.model_dump() for item in resume_data.experience],
                'projects': [item.model_dump() for item in resume_data.projects],
                'skills': [item.model_dump() for item in resume_data.skills],
                'languages': [item.model_dump() for item in resume_data.languages],
                'honors': [item.model_dump() for item in resume_data.honors],
                'self_evaluation': self_evaluation,
                'photo': photo
            }
        resume_data_dict = {
            'resume_id': resume_data.resume_id,
            'name': resume_data.name,
            'job_title': job_title,
            'recruitment_type': recruitment_type,
            'style': resume_data.template,
            'data': json.dumps(data, ensure_ascii=False)
        }
        self.resume_dao.insert_resume(resume_data_dict)
        return resume_data

    def load_content(self, recruitment_type: str):
        resume_data: ResumeRes = self.resume_dao.query_resume(recruitment_type)
        if not resume_data:
            return None
        data = json.loads(resume_data.data)
        photo_base64 = file_to_base64(data.get('photo', ''))  # data.photo.startswith("data:image")
        return {
          "recruitmentType": resume_data.recruitment_type,
          "name": resume_data.name,
          "jobTitle": resume_data.job_title,
          "phone": data.get('phone'),
          "email": data.get('email'),
          "address": data.get('address'),
          "selfEvaluation": data.get('self_evaluation'),
          "education": data.get('educations'),
          "experience": data.get('experiences'),
          "skills": data.get('skills'),
          "projects": data.get('projects'),
          "honors": data.get("honors"),
          "languages": data.get("languages"),
          "template": resume_data.style,
          "photo": photo_base64,
        }