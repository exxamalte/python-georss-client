"""Test for the generic georss feed."""
import datetime
import requests
import unittest
from unittest import mock

from georss_client import UPDATE_ERROR, UPDATE_OK
from georss_client.generic_feed import GenericFeed
from tests.utils import load_fixture


class TestGenericFeed(unittest.TestCase):
    """Test the generic feed."""

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok(self, mock_session, mock_request):
        """Test updating feed is ok."""
        home_coordinates = (-31.0, 151.0)
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_1.xml')

        feed = GenericFeed(home_coordinates, None)
        assert repr(feed) == "<GenericFeed(home=(-31.0, 151.0), url=None, " \
                             "radius=None, categories=None)>"
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
        assert feed_entry.attribution == "Attribution 1"
        assert repr(feed_entry) == "<GenericFeedEntry(id=2345)>"

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
        home_coordinates = (-31.0, 151.0)
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_2.xml')

        feed = GenericFeed(home_coordinates, None)
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
        home_coordinates = (-31.0, 151.0)
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_3.xml')

        feed = GenericFeed(home_coordinates, None)
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
        home_coordinates = (-37.0, 150.0)
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_1.xml')

        feed = GenericFeed(home_coordinates, None, filter_radius=90.0)
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
        home_coordinates = (-37.0, 150.0)
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_1.xml')

        feed = GenericFeed(home_coordinates, None, filter_radius=90.0,
                           filter_categories=['Category 2'])
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 1
        self.assertAlmostEqual(entries[0].distance_to_home, 77.0, 1)

        feed = GenericFeed(home_coordinates, None, filter_radius=90.0,
                           filter_categories=['Category 4'])
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 0

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_error(self, mock_session, mock_request):
        """Test updating feed results in error."""
        home_coordinates = (-31.0, 151.0)
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = False

        feed = GenericFeed(home_coordinates, None)
        status, entries = feed.update()
        assert status == UPDATE_ERROR

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_with_request_exception(self, mock_session, mock_request):
        """Test updating feed raises exception."""
        home_coordinates = (-31.0, 151.0)
        mock_session.return_value.__enter__.return_value.send\
            .side_effect = requests.exceptions.RequestException

        feed = GenericFeed(home_coordinates, None)
        status, entries = feed.update()
        assert status == UPDATE_ERROR
        self.assertIsNone(entries)
