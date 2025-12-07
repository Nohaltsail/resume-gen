from typing import Optional, Dict
import dotenv

import yaml
from resume.common.logger import get_logger
from resume.service.client.mysql_client import MysqlClient
from resume.service.client.sqlite_client import SqliteClient
from resume.service.model import NamedService
from resume.service.model import ServiceConfig
from resume.service.impl.mysql_db import get_mysql_db
from resume.service.impl.sqlite_db import get_sqlite_db
from resume.settings import SERVICE_YAML_PATH


logger = get_logger()


class ServiceRegistry:
    """服务配置"""

    # 注册的服务实例，部分不能有多实例
    _singleton_services: Dict[str, NamedService]

    def __init__(
        self,
        config_file: Optional[str] = None,
        config_str: Optional[str] = None,
    ) -> None:
        dotenv.load_dotenv()
        if config_file is None and config_str is None:
            raise ValueError("config_file or config_str must be provided")
        elif config_file:
            self._services = self._load_service_config_from_file(config_file)
        else:
            self._services = self._load_service_config_from_str(config_str)

        self._singleton_services = {}

    def _load_service_config_from_file(self, service_file: str) -> dict[str, list[ServiceConfig]]:
        """加载服务配置"""
        with open(service_file, "r") as f:
            config_text = f.read()
            return self._load_service_config_from_str(config_text)

    def _load_service_config_from_str(self, config_content: str) -> dict[str, list[ServiceConfig]]:
        """加载服务配置"""
        config = yaml.safe_load(config_content)
        for service_type, service_configs in config.items():
            config[service_type] = [ServiceConfig.model_validate(service_config) for service_config in service_configs]

        return config

    def get_service_config(
        self, service_type: str, name: str, namespace: Optional[str] = None
    ) -> Optional[ServiceConfig]:
        """获取服务配置"""
        if self._services is None:
            raise ValueError(f"service {service_type} not found")
        elif not self._services[service_type]:
            return None

        if namespace is None:
            namespace = "default"

        for config in self._services[service_type]:
            if config.name == name and config.namespace == namespace:
                return config

    def get_mysql_service(self, name: str, namespace: Optional[str] = None) -> Optional[NamedService[MysqlClient]]:
        """
        获取mysql服务信息


        Args:
        - name: str, 服务名称
        - namespace: str, 名字空间

        Returns:
        - NamedService[Embeddings], mysql服务实例
        """
        _service_key = f"mysql_db_{name}_{namespace}"
        if self._singleton_services is not None and _service_key in self._singleton_services:
            return self._singleton_services[_service_key]

        config = self.get_service_config("mysql_db", name, namespace)
        try:
            mysql_db = get_mysql_db(config)
            self.register_singleton(_service_key, mysql_db)
            return mysql_db
        except Exception as e:
            logger.error(f"get mysql service failed: {e}")
            return None

    def get_sqlite_service(self, name: str, namespace: Optional[str] = None) -> Optional[NamedService[SqliteClient]]:
        """
        获取sqlite服务信息


        Args:
        - name: str, 服务名称
        - namespace: str, 名字空间

        Returns:
        - NamedService[Embeddings], sqlite服务实例
        """
        _service_key = f"sqlite_db_{name}_{namespace}"
        if self._singleton_services is not None and _service_key in self._singleton_services:
            return self._singleton_services[_service_key]

        config = self.get_service_config("sqlite_db", name, namespace)
        try:
            sqlite_db = get_sqlite_db(config)
            self.register_singleton(_service_key, sqlite_db)
            return sqlite_db
        except Exception as e:
            logger.error(f"get sqlite service failed: {e}")
            return None

    def register_singleton(self, _service_key, service):
        # 注册单例
        if self._singleton_services is None:
            self._singleton_services = {}
        if _service_key in self._singleton_services:
            logger.warning(f"service {_service_key} already exists")
            return
        self._singleton_services[_service_key] = service


service_registry: ServiceRegistry = ServiceRegistry(SERVICE_YAML_PATH)
