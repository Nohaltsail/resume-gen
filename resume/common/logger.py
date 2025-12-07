"""日志模块，支持根据文件名自动获取logger名称"""

import inspect
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

from resume.common.filter.trace import TraceIDFilter
from resume.settings import LOG_DIR

MAX_LOG_SIZE = 1024 * 1024 * 30
MAX_BACK_COUNTS = 10

def get_trace_id_logger(wrapped, instance, args, kwargs):
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    """
    logger = wrapped(*args, **kwargs)
    # 添加trace_id过滤器
    if logger.filters == []:
        logger.addFilter(TraceIDFilter())
    return logger


def get_logger(name: Optional[str] = None, module_name: Optional[str] = None) -> logging.Logger:
    """
    返回命名logger，如果没有提供名称，则自动获取当前的模块名

    Args:

        name: logger名称
        logger_type: 日志类型，默认为debug

    Return:
        logger
    """
    if not name:
        name = _get_caller_name() or "root"
        logger = logging.getLogger(name)
        # 添加trace_id过滤器
        if logger.filters == []:
            logger.addFilter(TraceIDFilter())
        return logger
    else:
        # 传入名称的，加上模块名，并且自定义handler
        logger: logging.Logger = logging.getLogger(name)
        if len(logger.handlers) == 0:
            logger.root = None
            logger.parent = None
            logger.setLevel(logging.DEBUG)
            logpath = os.path.join(LOG_DIR, module_name)
            if not os.path.exists(logpath):
                os.makedirs(logpath)
            handler = RotatingFileHandler(
                os.path.join(logpath, f"{name}.log"),
                maxBytes=MAX_LOG_SIZE,  # 60MB 一个文件
                backupCount=MAX_BACK_COUNTS,  # 保存10个备份
                encoding="utf-8",
            )
            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(trace_id)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s"
                )
            )
            logger.addHandler(handler)
            logger.addHandler(
                logging.StreamHandler(),
            )
            logger.addFilter(TraceIDFilter())

        return logger


def _get_caller_name() -> Optional[str]:
    current_frame = inspect.currentframe()
    if current_frame is None:
        return None

    caller_frame = current_frame.f_back
    if caller_frame is None:
        return None

    caller_frame = caller_frame.f_back
    if caller_frame is None:
        return None

    module = inspect.getmodule(caller_frame)
    if module:
        return module.__name__
    else:
        return None


# TODO: log is not recording agents
def _setup_logging() -> None:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_directory = os.getenv("LOG_DIR", LOG_DIR)

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # 配置日志记录器，改成切分日志的logger
    file_handler = RotatingFileHandler(
        os.path.join(log_directory, "app.log"),
        maxBytes=MAX_LOG_SIZE,  # 60MB 一个文件
        backupCount=MAX_BACK_COUNTS,  # 保存10个备份
        encoding="utf-8",
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(trace_id)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s")
    )
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(trace_id)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            file_handler,  # 中文乱码问题
            logging.StreamHandler(),
        ],
    )
    # 现有拦截起都加上trace_id过滤器
    logging.getLogger().addFilter(TraceIDFilter())
    for logger_name, logger in logging.getLogger().manager.loggerDict.items():
        if isinstance(logger, logging.Logger):
            logger.addFilter(TraceIDFilter())

    # 重写logging.getLogger方法，后续拦截器初始化都会加上拦截器
    from wrapt import wrap_function_wrapper

    wrap_function_wrapper(
        "logging",
        "getLogger",
        get_trace_id_logger,
    )


_setup_logging()
