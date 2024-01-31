"""Tests for feed entry."""
import datetime
import unittest
from unittest import mock

from georss_client import FeedEntry


class TestFeedEntry(unittest.TestCase):
    """Test cases or feed entry."""

    def test_simple_feed_entry(self):
        """Test feed entry behaviour."""
        feed_entry = FeedEntry(None, None)
        assert repr(feed_entry) == "<FeedEntry(id=None)>"
        self.assertIsNone(feed_entry.geometry)
        self.assertIsNone(feed_entry.coordinates)
        self.assertIsNone(feed_entry.title)
        self.assertIsNone(feed_entry.category)
        self.assertIsNone(feed_entry.attribution)
        self.assertIsNone(feed_entry.description)
        self.assertIsNone(feed_entry.published)
        self.assertIsNone(feed_entry.updated)
        self.assertIsNone(
            feed_entry._search_in_external_id(r"External ID (?P<custom_attribute>.+)$")
        )
        self.assertIsNone(
            feed_entry._search_in_title(r"Title (?P<custom_attribute>.+)$")
        )
        self.assertIsNone(
            feed_entry._search_in_description(r"Description (?P<custom_attribute>.+)$")
        )

    def test_feed_entry_search_in_attributes(self):
        """Test feed entry behaviour."""
        rss_entry = mock.MagicMock()
        type(rss_entry).guid = mock.PropertyMock(return_value="Test 123")
        type(rss_entry).title = mock.PropertyMock(return_value="Title 123")
        type(rss_entry).description = mock.PropertyMock(return_value="Description 123")
        type(rss_entry).category = mock.PropertyMock(
            return_value=["Category 1", "Category 2"]
        )
        updated = datetime.datetime(2019, 4, 1, 8, 30, tzinfo=datetime.timezone.utc)
        type(rss_entry).updated_date = mock.PropertyMock(return_value=updated)

        feed_entry = FeedEntry(None, rss_entry)
        assert repr(feed_entry) == "<FeedEntry(id=Test 123)>"

        assert (
            feed_entry._search_in_external_id(r"Test (?P<custom_attribute>.+)$")
            == "123"
        )
        assert feed_entry._search_in_title(r"Title (?P<custom_attribute>.+)$") == "123"
        assert (
            feed_entry._search_in_description(r"Description (?P<custom_attribute>.+)$")
            == "123"
        )
        assert feed_entry.category == "Category 1"
        assert feed_entry.description == "Description 123"
        assert feed_entry.updated == updated
