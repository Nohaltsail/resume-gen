import inspect
import os
from pathlib import Path

from sqlalchemy import Row, text
from typing import Type, Any

from sqlalchemy.orm import Session
from resume.common.logger import get_logger
from resume.common.mybatis.generate import create_mapper
from resume.service.client.database import mysqldb, sqlitedb
from resume.common.util import sqlalchemy_util

T = sqlalchemy_util.T

logger = get_logger()


def parse_row_to_model(input: Row, model_class: Type[T]) -> T:
    """
    将查询结果转为T类型对象
    """
    if input is None:
        return None
    return sqlalchemy_util.parse_row_to_model(input, model_class)


class BaseDao:
    """
    用户服务类
    """

    def __init__(self):
        self.db_client = mysqldb.client

    def init_mapper(self, xml: str):
        base_dir = Path(inspect.getmodule(self.__class__).__file__).resolve().parent
        return create_mapper(xml=os.path.join(base_dir, xml))

    def raw_insert(self, sql: str, params: dict, session: Session, commit: bool = False) -> int:
        """
        原生插入，返回主键

        Args
            sql: sql语句
            params: 参数
            session: session

        Return
            int: 主键
        """
        result = session.execute(text(sql), params)
        session.flush()
        if commit:
            session.commit()
        logger.debug(f"insert result: {result.lastrowid}")
        return result.lastrowid

    def raw_fetch_first(self, sql: str, params: dict, model_class: Type[T], session: Session) -> T:
        """
        查询单挑数据
        """
        row = session.execute(text(sql), params=params).first()
        return parse_row_to_model(row, model_class)

    def raw_sql_fetch_first(self, sql: str, model_class: Type[T] = None, session: Session = None) -> T:
        """
        查询单挑， 没有参数
        """
        row = session.execute(text(sql)).first()
        if not model_class:
            return row
        return parse_row_to_model(row, model_class)

    def raw_fetch_list(self, sql, params, model_class: Type[T] = None, session: Session = None) -> list[T]:
        """
        原生查询，并返回对应的格式数据
        """
        if session is None:
            raise Exception("session is None")
        rows = session.execute(text(sql), params).all()
        logger.debug(f"fetch list result: {rows}")
        if model_class is None:
            return rows
        return self.parse_rows_to_model(rows, model_class)

    def raw_sql_fetch_list(self, sql, model_class: Type[T] = None, session: Session = None) -> list[T]:
        """
        原生查询，并返回对应的格式数据
        """
        if session is None:
            raise Exception("session is None")
        rows = session.execute(text(sql)).all()
        logger.debug(f"fetch list result: {rows}")
        if not model_class:
            return rows
        return self.parse_rows_to_model(rows, model_class)

    def raw_update(self, sql: str, session: Session, params: dict = {}, commit: bool = False) -> int:
        """
        查询单挑数据
        """
        row = session.execute(text(sql), params=params)
        session.flush()
        if commit:
            session.commit()
        return row.rowcount

    def parse_rows_to_model(self, input: list[Row], model_class: Type[T]) -> list[T]:
        """
        将查询结果列表转为T类型对象
        """
        if input is None:
            return None
        return sqlalchemy_util.parse_rows_to_model(input, model_class)

    def parse_model_to_dict(self, input: Any) -> dict:
        """
        对象转为dict
        """
        if input is None:
            return None
        return sqlalchemy_util.parse_model_to_dict(input)

    def convert_value_to_model(self, source: Any, target: Any):
        """
        将一个对象同名属性的值覆盖到另一个对象中，不同名属性不处理
        """
        # 创建一个字典，包含target类的属性
        target_attr = {k: getattr(target, k) for k in target.__dict__ if not k.startswith("_")}
        # 更新target_attr字典，使其包含source类的公共属性
        target_attr.update(
            {k: getattr(source, k) for k in source.__dict__ if not k.startswith("_") and hasattr(target, k)}
        )
        # 更新target对象的属性
        target.__dict__.update(target_attr)


