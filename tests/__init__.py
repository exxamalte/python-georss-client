"""Tests for georss-client library."""
from georss_client import GeoRssFeed, FeedEntry


class MockGeoRssFeed(GeoRssFeed):

    def _new_entry(self, home_coordinates, rss_entry, global_data):
        """Generate a new entry."""
        return FeedEntry(home_coordinates, rss_entry)
