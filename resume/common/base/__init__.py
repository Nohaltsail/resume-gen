from typing import TypeVar

from resume.common.base.base_dao import BaseDao

T = TypeVar("T", bound=BaseDao)


def get_dao_singleton(model_class: T) -> T:
    """
    单例模式
    :param model_class:
    :return:
    """
    return model_class()
