import time

from resume.common.mybatis.type_handler import sql_string_format
from resume.common.logger import get_logger

logger = get_logger()


# 函数容器
class PyFunction(object):
    def __init__(self):
        self.function_map = dict()

    def register_func(self, function_name: str, func):
        if function_name in self.function_map:
            logger.warning("function {} exist".format(function_name))
            return
        self.function_map[function_name] = func

    def get_func(self, function_name: str):
        if function_name in self.function_map:
            return self.function_map[function_name]
        return None

    def call_func(self, function_name: str, *args):
        func = self.get_func(function_name)
        if func and callable(func):
            return func(*args)


# -- func
def like(value):
    return sql_string_format(value)


def time_format(date_value, format: str = "%Y-%m-%d %H:%M:%S"):
    return sql_string_format(time.strftime(format, date_value))


default_fun_dict = {}
default_fun_dict["like"] = like

default_fun_dict["time_format"] = time_format

# 参数 转换函数
PY_PARAM_FUNCTION = PyFunction()
# 注册参数转换函数
for fun_name in default_fun_dict:
    PY_PARAM_FUNCTION.register_func(fun_name, default_fun_dict[fun_name])

# 返回值转换函数
PY_RESULT_FUNCTION = PyFunction()
