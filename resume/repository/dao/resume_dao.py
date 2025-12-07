from sqlalchemy.orm import Session

from resume.common.base.base_dao import BaseDao
from resume.common.decorators.application_context import singleton
from resume.common.decorators.auto_session import auto_session
from resume.common.mybatis.generate import get_child_statement
from resume.common.logger import get_logger
from resume.model.resume_model import ResumeRes
from resume.settings import settings
from resume.service.client.database import sqlitedb

@singleton("resume_dao")
class ResumeDao(BaseDao):
    """
    resume 查询
    """

    def __init__(self):
        super().__init__()
        if settings.ACTIVE_DATABASE == 'sqlite':
            self.db_client = sqlitedb.client
        # 获取当前文件路径, 需要用到xml的 加上下面这样，定义mapper对象
        self.mapper = self.init_mapper("resume.xml")
        self.logger = get_logger()

    @auto_session(commit=True)
    def insert_resume(self, resume_data: dict, session: Session=None):
        if settings.ACTIVE_DATABASE == 'sqlite':
            child_id = 'insert_resume_sqlite'
        else:
            child_id = 'insert_resume'
        stmt = get_child_statement(self.mapper, child_id=child_id, params=resume_data)
        return self.raw_insert(stmt, resume_data, session=session)

    @auto_session(commit=True)
    def query_resume(self, recruitment_type, session: Session = None):
        params = {'recruitment_type': recruitment_type}
        stmt = get_child_statement(self.mapper, child_id="query_resume")
        return self.raw_fetch_first(stmt, params, ResumeRes, session=session)
