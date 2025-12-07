from functools import wraps
from resume.settings import settings
from resume.common.logger import get_logger
from resume.service.client.database import mysqldb
from resume.service.client.database import sqlitedb

logger = get_logger()

if settings.ACTIVE_DATABASE == 'sqlite':
    _session_load = sqlitedb.client.get_session
else:
    _session_load = mysqldb.client.get_session


def auto_session(commit: bool = False):
    """
    自动生成session，生成的session自动close
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 确定 session 参数的位置
            get_session = False
            session = kwargs.get("session")
            if session is None and args:
                session = args[-1]

            if session is None or not hasattr(session, "close"):
                # 没有传入session，则生成session
                get_session = True
                logger.debug("auto create session")
                session = _session_load()
                kwargs["session"] = session

            try:
                result = func(*args, **kwargs)
                if commit:
                    logger.debug("commit session")
                    session.commit()
                return result
            finally:
                if get_session:
                    logger.debug("auto close session")
                    # 如果是获取的session，则做关闭操作
                    session.close()

        return wrapper

    return decorator
