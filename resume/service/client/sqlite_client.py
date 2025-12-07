from sqlalchemy import create_engine, text, QueuePool, Row
from sqlalchemy.orm import Session, sessionmaker
from typing import Type

from resume.common.logger import get_logger
from resume.common.util import sqlalchemy_util

T = sqlalchemy_util.T

logger = get_logger()


class SqliteClient:
    def __init__(self, db_file):
        """
        :param service_config:

        拼接config配置

        """
        sqlalchemy_database_url = f"sqlite:///{db_file}"
        # logger.info(f"init SQLALCHEMY_DATABASE_URL: {sqlalchemy_database_url}")
        self.engine = create_engine(
            sqlalchemy_database_url,
            connect_args={"check_same_thread": False},  # 多线程支持
            echo=True,
        )

    def get_session(self):
        return Session(self.engine)

    def get_session_by_sessionmaker(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init(self, sql):
        with Session(self.engine) as session:
            result = session.execute(text(sql))
            session.commit()
        return result

    # 初始化数据库
    # def init_db():
    #     conn = sqlite3.connect('resumes.db')
    #     cursor = conn.cursor()
    #     cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS resumes (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             resume_id TEXT UNIQUE,
    #             name TEXT NOT NULL,
    #             job_title TEXT,
    #             data TEXT NOT NULL,
    #             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    #             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #         )
    #     ''')
    #     conn.commit()
    #     conn.close()
    #
    #
    # init_db()

    def save_or_update(self, sql, params):
        """
        新增或者更新操作
        """
        with Session(self.engine) as session:
            result = session.execute(text(sql), params)
            session.commit()
        return result

    def raw_query(self, sql, params):
        """
        原生sql查询
        """
        with Session(self.engine) as session:
            result = session.execute(text(sql), params)
        return result

    def raw_fetch_first(self, sql, params, model_class: Type[T]) -> T:
        """
        原生查询，并返回对应的格式数据
        """
        row = self.raw_query(sql, params).first()
        if not row:
            return None
        return self.parse_row_to_model(row, model_class)

    def raw_fetch_list(self, sql, params, model_class: Type[T]) -> list[T]:
        """
        原生查询，并返回对应的格式数据
        """
        rows = self.raw_query(sql, params).all()
        if not rows:
            return []
        return self.parse_rows_to_model(rows, model_class)

    def delete(self, sql, params):
        return self.save_or_update(sql, params)

    def parse_row_to_model(self, input: Row, model_class: Type[T]) -> T:
        """
        将查询结果转为T类型对象
        """
        return sqlalchemy_util.parse_row_to_model(input, model_class)

    def parse_rows_to_model(self, input: list[Row], model_class: Type[T]) -> list[T]:
        """
        将查询结果列表转为T类型对象
        """
        return sqlalchemy_util.parse_rows_to_model(list, model_class)

