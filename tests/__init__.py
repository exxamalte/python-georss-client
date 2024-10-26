"""Tests for georss-client library."""

from georss_client.feed import GeoRssFeed
from georss_client.feed_entry import FeedEntry
from georss_client.xml_parser.feed_item import FeedItem


class MockGeoRssFeed(GeoRssFeed):
    """Mock GeoRSS feed."""

    def _new_entry(
        self,
        home_coordinates: tuple[float, float],
        rss_entry: FeedItem,
        global_data: dict,
    ):
        """Generate a new entry."""
        return FeedEntry(home_coordinates, rss_entry)
