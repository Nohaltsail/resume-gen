"""
sqlite
使用示例：
```python

```
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel

from resume.common.logger import get_logger
from resume.service.model import ServiceConfig, NamedService
from resume.service.client.sqlite_client import SqliteClient
from resume.settings import settings

logger = get_logger()


class SqliteDBType(Enum):
    Sqlite = "sqlite"


class SqliteConfig(BaseModel):

    db: Optional[str] = None
    db_file: Optional[str] = None


def get_sqlite_db(
    service_config: ServiceConfig,
) -> NamedService[SqliteClient]:
    """获取sqlite实例

    Args:
    - service_config: dict, sqlite数据库配置

    Returns:
    - Session, 一个sqlite的session对象

    """
    if service_config.type == SqliteDBType.Sqlite.value:
        # valid config params
        config = SqliteConfig.model_validate(service_config.config)
        config.db = settings.SQLITE_DATABASE
        config.db_file = settings.SQLITE_DATABASE_PATH

        client = SqliteClient(
            config.db_file
        )
        if settings.ACTIVE_DATABASE == 'sqlite':
            client.init("""
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id TEXT UNIQUE,
                name TEXT NOT NULL,
                job_title TEXT,
                recruitment_type TEXT NOT NULL CHECK (recruitment_type IN ('campus', 'social')),
                data TEXT NOT NULL,
                style VARCHAR(20) DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
        return NamedService(
            config=service_config,
            client=client,
        )
