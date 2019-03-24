"""
WA Department of Fire and Emergency Services (DFES) Feed.

Fetches GeoRSS feed from WA Department of Fire and Emergency Services (DFES)
Feed.
"""
import logging

from typing import Optional

from georss_client import GeoRssFeed, FeedEntry
from georss_client.consts import CUSTOM_ATTRIBUTE
from georss_client.exceptions import GeoRssException
from georss_client.feed_manager import FeedManagerBase

_LOGGER = logging.getLogger(__name__)

ADDITIONAL_NAMESPACES = {
    'http://emergency.wa.gov.au/xmlns/dfes': 'dfes'
}

ATTRIBUTION = "Department of Fire and Emergency Services"

REGEXP_ATTR_CATEGORY_WARNINGS = '<b>Category: </b>(?P<{}>[^<]+)</div>'\
    .format(CUSTOM_ATTRIBUTE)
REGEXP_ATTR_CATEGORY_ALL_INCIDENTS = '^(?P<{}>[^<]+) <'\
    .format(CUSTOM_ATTRIBUTE)
REGEXP_ATTR_REGION = '<region>(?P<{}>[^<]+)</region>'\
    .format(CUSTOM_ATTRIBUTE)

URL_PREFIX = 'https://www.emergency.wa.gov.au/data/'
URLS = {
    'warnings': URL_PREFIX + 'message.rss',
    'all_incidents': URL_PREFIX + 'incident_FCAD.rss',
}

XML_TAG_DFES_REGION = 'dfes:region'


class WaDfesFeedManager(FeedManagerBase):
    """Feed Manager for Department of Fire and Emergency Services feed."""

    def __init__(self, generate_callback, update_callback, remove_callback,
                 coordinates, feed, filter_radius=None,
                 filter_categories=None):
        """Initialize the DFES Feed Manager."""
        feed = WaDfesFeed(
            coordinates,
            feed,
            filter_radius=filter_radius,
            filter_categories=filter_categories)
        super().__init__(feed, generate_callback, update_callback,
                         remove_callback)


class WaDfesFeed(GeoRssFeed):
    """Department of Fire and Emergency Services (DFES) feed."""

    def __init__(self, home_coordinates, feed, filter_radius=None,
                 filter_categories=None):
        """Initialise this service."""
        if feed in URLS:
            super().__init__(home_coordinates, URLS[feed],
                             filter_radius=filter_radius,
                             filter_categories=filter_categories)
            self._feed = feed
        else:
            _LOGGER.error("Unknown feed category %s", feed)
            raise GeoRssException("Feed category must be one of %s".format(
                URLS.keys()))

    def _new_entry(self, home_coordinates, rss_entry, global_data):
        """Generate a new entry."""
        if self._feed == 'warnings':
            return WaDfesWarningsFeedEntry(home_coordinates, rss_entry)
        if self._feed == 'all_incidents':
            return WaDfesAllIncidentsFeedEntry(home_coordinates, rss_entry)

    def _additional_namespaces(self):
        """Provide additional namespaces, relevant for this feed."""
        return ADDITIONAL_NAMESPACES

    def _filter_entries(self, entries):
        """Filter the provided entries."""
        entries = super()._filter_entries(entries)
        if self._filter_categories:
            return list(filter(lambda entry:
                               entry.category in self._filter_categories,
                               entries))
        return entries


class WaDfesFeedEntry(FeedEntry):
    """Department of Fire and Emergency Services (DFES) feed entry."""

    def __init__(self, home_coordinates, rss_entry):
        """Initialise this service."""
        super().__init__(home_coordinates, rss_entry)

    @property
    def attribution(self) -> str:
        """Return the attribution of this entry."""
        return ATTRIBUTION


class WaDfesWarningsFeedEntry(WaDfesFeedEntry):
    """Department of Fire and Emergency Services (DFES) Warnings feed entry."""

    @property
    def category(self) -> str:
        """Return the type of this entry."""
        return self._search_in_description(REGEXP_ATTR_CATEGORY_WARNINGS)

    @property
    def region(self) -> Optional[str]:
        """Return the region of this entry."""
        if self._rss_entry:
            return self._rss_entry.get_additional_attribute(
                XML_TAG_DFES_REGION)
        return None


class WaDfesAllIncidentsFeedEntry(WaDfesFeedEntry):
    """Department of Fire and Emergency Services (DFES) All Incidents feed
    entry."""

    @property
    def category(self) -> str:
        """Return the type of this entry."""
        return self._search_in_description(REGEXP_ATTR_CATEGORY_ALL_INCIDENTS)

    @property
    def region(self) -> str:
        """Return the region of this entry."""
        return self._search_in_description(REGEXP_ATTR_REGION)
