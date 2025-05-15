import logging
from django.utils.timezone import now
from django.db import connection

MAX_MESSAGE_LENGTH = 10000

class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        if not connection or not connection.connection:
            return

        # Prevent infinite recursion
        if record.name == 'logapp.handlers':
            return

        try:
            from logapp.models import LogEntry

            message = record.getMessage()
            if len(message) > MAX_MESSAGE_LENGTH:
                message = message[:MAX_MESSAGE_LENGTH] + '... [truncated]'

            LogEntry.objects.create(
                level=record.levelname,
                message=message,
                logger_name=record.name,
                file_path=record.pathname,
                line_number=record.lineno,
                timestamp=now()
            )
        except Exception:
            # Avoid logging errors here, or it will recurse
            pass
