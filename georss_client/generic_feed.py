"""
Generic GeoRSS feed.

Support for generic GeoRSS feeds from various sources.
"""
from georss_client import GeoRssFeed, FeedEntry
from georss_client.consts import ATTR_ATTRIBUTION


class GenericFeed(GeoRssFeed):
    """Generic GeoJSON feed."""

    def __init__(self, home_coordinates, url, filter_radius=None,
                 filter_categories=None):
        """Initialise this service."""
        super().__init__(home_coordinates, url, filter_radius=filter_radius,
                         filter_categories=filter_categories)

    def _new_entry(self, home_coordinates, rss_entry, global_data):
        """Generate a new entry."""
        attribution = None if not global_data and ATTR_ATTRIBUTION not in \
            global_data else global_data[ATTR_ATTRIBUTION]
        return GenericFeedEntry(home_coordinates, rss_entry, attribution)


class GenericFeedEntry(FeedEntry):
    """Generic feed entry."""

    def __init__(self, home_coordinates, rss_entry, attribution):
        """Initialise this service."""
        super().__init__(home_coordinates, rss_entry)
        self._attribution = attribution

    @property
    def attribution(self) -> str:
        """Return the attribution of this entry."""
        return self._attribution
