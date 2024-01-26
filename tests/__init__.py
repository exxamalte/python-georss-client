"""Tests for georss-client library."""
from georss_client import FeedEntry, GeoRssFeed


class MockGeoRssFeed(GeoRssFeed):
    """Mock GeoRSS feed."""

    def _new_entry(self, home_coordinates, rss_entry, global_data):
        """Generate a new entry."""
        return FeedEntry(home_coordinates, rss_entry)
