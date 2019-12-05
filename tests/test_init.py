"""Tests for base classes."""
import datetime
import requests
import unittest
from unittest import mock
from unittest.mock import MagicMock

from georss_client import GeoRssDistanceHelper, FeedEntry, GeoRssFeed, \
    UPDATE_ERROR, UPDATE_OK
from georss_client.xml_parser.geometry import Point, Polygon
from tests import MockGeoRssFeed
from tests.utils import load_fixture

HOME_COORDINATES_1 = (-31.0, 151.0)
HOME_COORDINATES_2 = (-37.0, 150.0)


class TestGeoRssFeed(unittest.TestCase):

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_1.xml')

        feed = MockGeoRssFeed(HOME_COORDINATES_1, None)
        assert repr(feed) == "<MockGeoRssFeed(home=(-31.0, 151.0), " \
                             "url=None, radius=None, categories=None)>"
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 5

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.category == "Category 1"
        assert feed_entry.published == datetime.datetime(2018, 9, 23, 8, 30)
        assert feed_entry.updated == datetime.datetime(2018, 9, 23, 8, 35)
        assert feed_entry.coordinates == (-37.2345, 149.1234)
        self.assertAlmostEqual(feed_entry.distance_to_home, 714.4, 1)

        feed_entry = entries[1]
        assert feed_entry.title == "Title 2"
        assert feed_entry.external_id == "2345"
        self.assertIsNone(feed_entry.attribution)
        assert repr(feed_entry) == "<FeedEntry(id=2345)>"

        feed_entry = entries[2]
        assert feed_entry.title == "Title 3"
        assert feed_entry.external_id == "Title 3"

        feed_entry = entries[3]
        self.assertIsNone(feed_entry.title)
        assert feed_entry.external_id == -7266545992534134585

        feed_entry = entries[4]
        assert feed_entry.title == "Title 5"
        assert feed_entry.external_id == "5678"

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_feed_2(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_2.xml')

        feed = MockGeoRssFeed(HOME_COORDINATES_1, None)
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 1

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.category == "Category 1"
        assert feed_entry.coordinates == (-37.2345, 149.1234)
        self.assertAlmostEqual(feed_entry.distance_to_home, 714.4, 1)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_feed_3(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_3.xml')

        feed = MockGeoRssFeed(HOME_COORDINATES_1, None)
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 3

        feed_entry = entries[0]
        assert feed_entry.external_id == "1234"
        assert feed_entry.coordinates == (-34.93728111547821,
                                          148.59710883878262)
        self.assertAlmostEqual(feed_entry.distance_to_home, 491.7, 1)

        feed_entry = entries[1]
        assert feed_entry.external_id == "2345"
        assert feed_entry.coordinates == (-34.937170989, 148.597182317)
        self.assertAlmostEqual(feed_entry.distance_to_home, 491.8, 1)

        feed_entry = entries[2]
        assert feed_entry.external_id == "3456"
        assert feed_entry.coordinates == (-29.962746645660683,
                                          152.43090880416074)
        self.assertAlmostEqual(feed_entry.distance_to_home, 176.5, 1)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_with_radius_filtering(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_1.xml')

        feed = MockGeoRssFeed(HOME_COORDINATES_2, None, filter_radius=90.0)
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 4
        self.assertAlmostEqual(entries[0].distance_to_home, 82.0, 1)
        self.assertAlmostEqual(entries[1].distance_to_home, 77.0, 1)
        self.assertAlmostEqual(entries[2].distance_to_home, 84.6, 1)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_with_radius_and_category_filtering(self, mock_session,
                                                          mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_1.xml')

        feed = MockGeoRssFeed(HOME_COORDINATES_2, None, filter_radius=90.0,
                           filter_categories=['Category 2'])
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 1
        self.assertAlmostEqual(entries[0].distance_to_home, 77.0, 1)

        feed = MockGeoRssFeed(HOME_COORDINATES_2, None, filter_radius=90.0,
                           filter_categories=['Category 4'])
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 0

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_error(self, mock_session, mock_request):
        """Test updating feed results in error."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = False

        feed = MockGeoRssFeed(HOME_COORDINATES_1, None)
        status, entries = feed.update()
        assert status == UPDATE_ERROR

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_with_request_exception(self, mock_session, mock_request):
        """Test updating feed raises exception."""
        mock_session.return_value.__enter__.return_value.send\
            .side_effect = requests.exceptions.RequestException

        feed = GeoRssFeed(HOME_COORDINATES_1, None)
        status, entries = feed.update()
        assert status == UPDATE_ERROR
        self.assertIsNone(entries)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_bom(self, mock_session, mock_request):
        """Test updating feed with BOM (byte order mark) is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('xml_parser_bom_1.xml')

        feed = MockGeoRssFeed(HOME_COORDINATES_1, None)
        assert repr(feed) == "<MockGeoRssFeed(home=(-31.0, 151.0), " \
                             "url=None, radius=None, categories=None)>"
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 0


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
        self.assertIsNone(feed_entry._search_in_external_id(
            r'External ID (?P<custom_attribute>.+)$'))
        self.assertIsNone(feed_entry._search_in_title(
            r'Title (?P<custom_attribute>.+)$'))
        self.assertIsNone(feed_entry._search_in_description(
            r'Description (?P<custom_attribute>.+)$'))

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
