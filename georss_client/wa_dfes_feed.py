"""
WA Department of Fire and Emergency Services (DFES) Feed.

Fetches GeoRSS feed from WA Department of Fire and Emergency Services (DFES)
Feed.
"""
import calendar
import logging
import pytz
from datetime import datetime

from typing import Optional

from georss_client import GeoRssFeed, FeedEntry
from georss_client.consts import CUSTOM_ATTRIBUTE
from georss_client.exceptions import GeoRssException

_LOGGER = logging.getLogger(__name__)

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

    @property
    def published(self) -> Optional[datetime]:
        """Return the published date of this entry."""
        if self._rss_entry:
            published_date = self._rss_entry.get('published_parsed', None)
            if published_date:
                return datetime.fromtimestamp(calendar.timegm(
                    published_date), tz=pytz.utc)
        return None


class WaDfesWarningsFeedEntry(WaDfesFeedEntry):
    """Department of Fire and Emergency Services (DFES) Warnings feed entry."""

    @property
    def category(self) -> str:
        """Return the type of this entry."""
        return self._search_in_summary(REGEXP_ATTR_CATEGORY_WARNINGS)

    @property
    def region(self) -> Optional[str]:
        """Return the region of this entry."""
        if self._rss_entry:
            return self._rss_entry.get('dfes_region', None)
        return None


class WaDfesAllIncidentsFeedEntry(WaDfesFeedEntry):
    """Department of Fire and Emergency Services (DFES) All Incidents feed
    entry."""

    @property
    def category(self) -> str:
        """Return the type of this entry."""
        return self._search_in_summary(REGEXP_ATTR_CATEGORY_ALL_INCIDENTS)

    @property
    def region(self) -> str:
        """Return the region of this entry."""
        return self._search_in_summary(REGEXP_ATTR_REGION)