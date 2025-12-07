import threading
from functools import wraps
from typing import Any

from resume.common.logger import get_logger

logger = get_logger()


def to_snake_case(name):
    """Converts CamelCase to snake_case."""
    import re

    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


class ApplicationContext:
    """
    IoC 容器，配置 singleton 实现单例注入
    """

    _services_by_name = {}
    _services_by_type = {}
    _lock = threading.Lock()

    @classmethod
    def register_with_lock(cls, namespace: str, name: str, service: Any):
        with cls._lock:
            cls.register(namespace, name, service)

    @classmethod
    def register(cls, namespace: str, name: str, service: Any):
        if namespace not in cls._services_by_name:
            cls._services_by_name[namespace] = {}
            cls._services_by_type[namespace] = {}
        logger.info(f"register namespace:{namespace} name:{name}")
        if name in cls._services_by_name[namespace]:
            logger.info(f"already register namespace:{namespace} name:{name}")
            return
        cls._services_by_name[namespace][name] = service
        cls._services_by_type.setdefault(namespace, {})[service.__class__] = service

    @classmethod
    def get(cls, identifier: Any, namespace: str = "default"):
        if isinstance(identifier, str):
            if namespace not in cls._services_by_name:
                raise ValueError(f"Namespace '{namespace}' 没有找到.")
            service = cls._services_by_name[namespace].get(identifier)
            if not service:
                raise ValueError(f"Service '{namespace}:{identifier}' 没有找到.")
            return service
        if namespace not in cls._services_by_type:
            raise ValueError(f"Namespace '{namespace}' 没有找到.")
        service = cls._services_by_type[namespace].get(identifier)
        if not service:
            raise ValueError(f"Service 类型 '{identifier.__name__}' 没有找到.")
        logger.info(f"找到实例：{namespace}:{identifier}")
        return service

    @classmethod
    def get_or_register(cls, cls_type: Any, *init_args: dict, **init_kwargs: dict):
        with cls._lock:
            if "namespace" in init_kwargs:
                namespace = init_kwargs["namespace"]
            else:
                namespace = "default"
            if namespace not in cls._services_by_name:
                cls._services_by_name[namespace] = {}
            if namespace not in cls._services_by_type:
                cls._services_by_type[namespace] = {}

            # If not registered, initialize and register the service
            if "bean" in init_kwargs:
                bean = init_kwargs["bean"]
                del init_kwargs["bean"]
            else:
                bean = to_snake_case(cls_type.__name__)

            # if name is None:
            #     name = to_snake_case(cls_type.__name__)
            logger.info(f"namespace：bean -> {namespace}:{bean}")
            if namespace in cls._services_by_name and bean in cls._services_by_name[namespace]:
                service = cls._services_by_name[namespace][bean]
                if service:
                    logger.info(f"找到实例：{namespace}:{bean}")
                    return service

            init_params = {}
            # init_params = {"namespace": namespace}
            for arg_name, arg_type in cls_type.__init__.__annotations__.items():
                if arg_name != "return":  # Skip the return type annotation
                    if arg_name in cls._services_by_name[namespace]:
                        init_params[arg_name] = cls.get(arg_name, namespace)
            init_params.update(init_kwargs)
            instance = cls_type(*init_args, **init_params)
            cls.register(namespace, bean, instance)
            return instance


def service(namespace: str = "default", name: str = None, *service_args, **service_kwargs):
    def decorator(cls):
        @wraps(cls)
        def wrapper(*args, **kwargs):
            # Retrieve dependencies from ApplicationContext
            init_args = {}
            for arg_name, arg_type in cls.__init__.__annotations__.items():
                if arg_name != "return":  # Skip the return type annotation
                    if arg_name in ApplicationContext._services_by_name[namespace]:
                        init_args[arg_name] = ApplicationContext.get(arg_name, namespace)
            # Merge dependencies with provided args and service_args/service_kwargs
            init_args.update(kwargs)
            instance = cls(*service_args, **service_kwargs, **init_args)
            if name is None:
                service_name = to_snake_case(cls.__name__)
            else:
                service_name = name
            ApplicationContext.register(namespace, service_name, instance)
            return instance

        return wrapper

    return decorator


def singleton(name):
    def decorator(cls):
        # 创建实例
        def create_instance():
            init_args = {}
            # 根据属性类型自动注入
            for arg_name, arg_type in cls.__init__.__annotations__.items():
                if arg_type in ApplicationContext._services_by_type:
                    init_args[arg_name] = ApplicationContext.get(arg_type)
            return cls(**init_args)

        namespace = "default"
        instance = create_instance()
        ApplicationContext.register_with_lock(namespace, name, instance)
        return cls

    return decorator


# def singleton(name):
#     def decorator(cls):
#         @wraps(cls)
#         def wrapper(*args, **kwargs):
#             if name is None:
#                 service_name = to_snake_case(cls.__name__)
#             else:
#                 service_name = name
#             namespace = "default"
#             # 创建实例
#             def create_instance():
#
#                 init_args = {}
#                 # 根据属性类型自动注入
#                 for arg_name, arg_type in cls.__init__.__annotations__.items():
#                     if arg_type in ApplicationContext._services_by_type.get(namespace, {}):
#                         init_args[arg_name] = ApplicationContext.get(arg_type, namespace)
#                 return cls(**init_args)
#
#             instance = create_instance()
#             ApplicationContext.register(namespace, service_name, instance)
#             return instance
#
#         return wrapper
