import contextvars
import logging

trace_id_var = contextvars.ContextVar("trace_id", default=" -- ")


class TraceIDFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = trace_id_var.get()
        return True
