"""
mysql数据库服务
使用示例：
```python

```
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel

from resume.common.logger import get_logger
from resume.service.model import ServiceConfig, NamedService
from resume.service.client.mysql_client import MysqlClient
from resume.settings import settings

logger = get_logger()


class MysqlDBType(Enum):
    Mysql = "mysql"


class MysqlConfig(BaseModel):
    host: Optional[str] = None
    port: Optional[int] = 3306
    db: Optional[str] = None
    user: Optional[str] = "root"
    password: Optional[str] = None


def get_mysql_db(
    service_config: ServiceConfig,
) -> NamedService[MysqlClient]:
    """获取mysql实例

    Args:
    - service_config: dict, mysql数据库配置

    Returns:
    - Session, 一个mysql的session对象

    """
    if service_config.type == MysqlDBType.Mysql.value:
        # valid config params
        config = MysqlConfig.model_validate(service_config.config)
        config.host = settings.MYSQL_HOST
        config.user = settings.MYSQL_USERNAME
        config.password = settings.MYSQL_PASSWORD
        config.port = settings.MYSQL_PORT

        client = MysqlClient(
            host=config.host,
            port=config.port,
            db=config.db,
            user=config.user,
            password=config.password,
        )
        return NamedService(
            config=service_config,
            client=client,
        )
