"""
QFES Bushfire Alert Feed.

Fetches GeoRSS feed from QFES Bushfire Alert Feed.
"""
from georss_client import GeoRssFeed, FeedEntry, ATTR_ATTRIBUTION
from georss_client.consts import CUSTOM_ATTRIBUTE
from georss_client.feed_manager import FeedManagerBase

REGEXP_ATTR_STATUS = 'Current Status: (?P<{}>[^<]+)[\n\r]'\
    .format(CUSTOM_ATTRIBUTE)

URL = "https://www.qfes.qld.gov.au/data/alerts/bushfireAlert.xml"

VALID_CATEGORIES = ['Emergency Warning', 'Watch and Act', 'Advice',
                    'Notification']


class QfesBushfireAlertFeedManager(FeedManagerBase):
    """Feed Manager for QFES Bushfire Alert feed."""

    def __init__(self, generate_callback, update_callback, remove_callback,
                 coordinates, filter_radius=None,
                 filter_categories=None):
        """Initialize the QFES Bushfire Alert Feed Manager."""
        feed = QfesBushfireAlertFeed(
            coordinates,
            filter_radius=filter_radius,
            filter_categories=filter_categories)
        super().__init__(feed, generate_callback, update_callback,
                         remove_callback)


class QfesBushfireAlertFeed(GeoRssFeed):
    """QFES Bushfire Alert feed."""

    def __init__(self, home_coordinates, filter_radius=None,
                 filter_categories=None):
        """Initialise this service."""
        super().__init__(home_coordinates, URL, filter_radius=filter_radius)
        self._filter_categories = filter_categories

    def _new_entry(self, home_coordinates, rss_entry, global_data):
        """Generate a new entry."""
        attribution = None if not global_data and ATTR_ATTRIBUTION not in \
            global_data else global_data[ATTR_ATTRIBUTION]
        return QfesBushfireAlertFeedEntry(home_coordinates, rss_entry,
                                          attribution)

    def _filter_entries(self, entries):
        """Filter the provided entries."""
        entries = super()._filter_entries(entries)
        if self._filter_categories:
            return list(filter(lambda entry:
                               entry.category in self._filter_categories,
                               entries))
        return entries


class QfesBushfireAlertFeedEntry(FeedEntry):
    """QFES Bushfire Alert feed entry."""

    def __init__(self, home_coordinates, rss_entry, attribution):
        """Initialise this service."""
        super().__init__(home_coordinates, rss_entry)
        self._attribution = attribution

    @property
    def attribution(self) -> str:
        """Return the attribution of this entry."""
        return self._attribution

    @property
    def status(self) -> str:
        """Return the status of this entry."""
        return self._search_in_description(REGEXP_ATTR_STATUS)
