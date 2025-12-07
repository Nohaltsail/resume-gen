from datetime import datetime
from typing import TypeVar, Type, Any, Dict

from pydantic import BaseModel
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T")


def parse_row_to_model(input: Row, model_class: Type[T]) -> T:
    """
    将查询结果转为T类型对象
    """
    row_data = {}
    for field_name, field_index in input._key_to_index.items():
        # 时间转为字符串
        value = input[field_index]
        if isinstance(value, (datetime)):
            value = value.strftime("%Y-%m-%d %H:%M:%S")
            row_data[field_name] = value
        else:
            row_data[field_name] = input[field_index]
    return model_class(**row_data)


def parse_rows_to_model(input: list[Row], model_class: Type[T]) -> list[T]:
    """
    将查询结果列表转为T类型对象
    """
    return [parse_row_to_model(row, model_class) for row in input]


def parse_model_to_dict(model: Any) -> dict:
    """
    将model实例转为dict
    """
    if isinstance(model, BaseModel):
        return model.dict()
    elif isinstance(model, dict):
        return model
    elif isinstance(model, DeclarativeBase):
        """Convert SQLAlchemy model object to dictionary."""
        return sqlalchemy_model_to_dict(model)
    # 确保model有__dict__属性再尝试访问
    elif hasattr(model, "__dict__"):
        return model.__dict__
    else:
        raise TypeError(f"Unsupported type: {type(model)}. Cannot convert to dict.")


def sqlalchemy_model_to_dict(model_instance: DeclarativeBase) -> Dict:
    """Convert a SQLAlchemy model instance into a dictionary."""
    data = {}
    for column in model_instance.__table__.columns:
        # 时间转为字符串
        value = getattr(model_instance, column.name)
        # if value is None:
        #     continue
        if isinstance(value, (datetime)):
            value = value.strftime("%Y-%m-%d %H:%M:%S")
        data[column.name] = value
    return data
