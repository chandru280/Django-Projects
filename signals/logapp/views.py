import logging
from django.http import HttpResponse

logger = logging.getLogger('django')

def test_logging(request):
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    return HttpResponse("Logs created and stored in DB.")
