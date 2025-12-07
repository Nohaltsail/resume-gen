from resume.service.client.database import mysqldb


class BaseService:
    """
    用户服务类
    """

    def __init__(self):
        self.db_client = mysqldb.client
