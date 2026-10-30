"""Sentry integration for the application."""

import sentry_sdk
from structlog import get_logger

from app.config import settings

logger = get_logger(__name__)


def init_sentry() -> bool:
    """Initialize Sentry when SENTRY_DSN is configured."""
    if not settings.sentry_dsn:
        return False

    try:
        sentry_sdk.init(dsn=settings.sentry_dsn)
    except Exception as exc:
        logger.warning("Sentry initialization failed", error=str(exc), exc_info=True)
        return False

    logger.info("Sentry initialized")
    return True
