"""Base class for GeoRSS services."""

from georss_client.consts import ATTR_ATTRIBUTION  # noqa: F401

from .consts import (  # noqa: F401
    CUSTOM_ATTRIBUTE,
    UPDATE_ERROR,
    UPDATE_OK,
    UPDATE_OK_NO_DATA,
)
from .feed import GeoRssFeed  # noqa: F401
from .feed_entry import FeedEntry  # noqa: F401
