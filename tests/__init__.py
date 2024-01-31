"""Tests for georss-client library."""
from georss_client.feed import GeoRssFeed
from georss_client.feed_entry import FeedEntry


class MockGeoRssFeed(GeoRssFeed):
    """Mock GeoRSS feed."""

    def _new_entry(self, home_coordinates, rss_entry, global_data):
        """Generate a new entry."""
        return FeedEntry(home_coordinates, rss_entry)
