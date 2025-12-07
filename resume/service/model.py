"""服务配置模型"""

from typing import Generic, TypeVar
from pydantic import BaseModel, Field


class ServiceConfig(BaseModel):
    """基础服务配置"""

    name: str
    namespace: str
    type: str = Field("", description="服务类型")
    llm_env: dict = {}
    config: dict = {}


# 服务类
T = TypeVar("T")


class NamedService(BaseModel, Generic[T]):

    config: ServiceConfig
    client: T

    class Config:
        arbitrary_types_allowed = True
