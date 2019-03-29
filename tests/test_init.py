"""Tests for base classes."""
import datetime
import unittest
from unittest import mock
from unittest.mock import MagicMock

from georss_client import GeoRssDistanceHelper, FeedEntry
from georss_client.xml_parser.geometry import Point, Polygon


class TestGeoRssDistanceHelper(unittest.TestCase):
    """Tests for the GeoJSON distance helper."""

    def test_extract_coordinates_from_point(self):
        """Test extracting coordinates from point."""
        mock_point = Point(-30.0, 151.0)
        latitude, longitude = GeoRssDistanceHelper.\
            extract_coordinates(mock_point)
        assert latitude == -30.0
        assert longitude == 151.0

    def test_extract_coordinates_from_polygon(self):
        """Test extracting coordinates from polygon."""
        mock_polygon = Polygon([Point(-30.0, 151.0),
                                Point(-30.0, 151.5),
                                Point(-30.5, 151.5),
                                Point(-30.5, 151.0),
                                Point(-30.0, 151.0)])
        latitude, longitude = GeoRssDistanceHelper.\
            extract_coordinates(mock_polygon)
        self.assertAlmostEqual(latitude, -30.2, 1)
        self.assertAlmostEqual(longitude, 151.2, 1)

    def test_extract_coordinates_from_unsupported_geometry(self):
        """Test extracting coordinates from unsupported geometry."""
        mock_unsupported_geometry = MagicMock()
        latitude, longitude = GeoRssDistanceHelper.\
            extract_coordinates(mock_unsupported_geometry)
        self.assertIsNone(latitude)
        self.assertIsNone(longitude)

    def test_distance_to_point(self):
        """Test calculating distance to point."""
        home_coordinates = [-31.0, 150.0]
        mock_point = Point(-30.0, 151.0)
        distance = GeoRssDistanceHelper.\
            distance_to_geometry(home_coordinates, mock_point)
        self.assertAlmostEqual(distance, 146.8, 1)

    def test_distance_to_polygon(self):
        """Test calculating distance to point."""
        home_coordinates = [-31.0, 150.0]
        mock_polygon = Polygon([Point(-30.0, 151.0),
                                Point(-30.0, 151.5),
                                Point(-30.5, 151.5),
                                Point(-30.5, 151.0),
                                Point(-30.0, 151.0)])
        distance = GeoRssDistanceHelper.\
            distance_to_geometry(home_coordinates, mock_polygon)
        self.assertAlmostEqual(distance, 110.6, 1)

    def test_distance_to_unsupported_geometry(self):
        """Test calculating distance to unsupported geometry."""
        home_coordinates = [-31.0, 150.0]
        mock_unsupported_geometry = MagicMock()
        distance = GeoRssDistanceHelper.\
            distance_to_geometry(home_coordinates, mock_unsupported_geometry)
        assert distance == float("inf")


class TestFeedEntry(unittest.TestCase):

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

        mock_rss_entry = dict()
        feed_entry = FeedEntry(None, mock_rss_entry)
        assert repr(feed_entry) == "<FeedEntry(id=None)>"

    def test_feed_entry_search_in_attributes(self):
        """Test feed entry behaviour."""
        rss_entry = mock.MagicMock()
        type(rss_entry).guid = mock.PropertyMock(return_value="Test 123")
        type(rss_entry).title = mock.PropertyMock(return_value="Title 123")
        type(rss_entry).description = mock.PropertyMock(
            return_value="Description 123")
        type(rss_entry).category = mock.PropertyMock(
            return_value=["Category 1", "Category 2"])
        updated = datetime.datetime(2019, 4, 1, 8, 30,
                                    tzinfo=datetime.timezone.utc)
        type(rss_entry).updated_date = mock.PropertyMock(return_value=updated)

        feed_entry = FeedEntry(None, rss_entry)
        assert repr(feed_entry) == "<FeedEntry(id=Test 123)>"

        assert feed_entry._search_in_external_id(
            r'Test (?P<custom_attribute>.+)$') == "123"
        assert feed_entry._search_in_title(
            r'Title (?P<custom_attribute>.+)$') == "123"
        assert feed_entry._search_in_description(
            r'Description (?P<custom_attribute>.+)$') == "123"
        assert feed_entry.category == "Category 1"
        assert feed_entry.description == "Description 123"
        assert feed_entry.updated == updated
