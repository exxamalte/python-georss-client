"""Tests for feed."""
import datetime
import unittest
from unittest import mock

import pytest
import requests

from georss_client.consts import UPDATE_ERROR, UPDATE_OK
from georss_client.feed import GeoRssFeed
from tests import MockGeoRssFeed
from tests.utils import load_fixture

HOME_COORDINATES_1 = (-31.0, 151.0)
HOME_COORDINATES_2 = (-37.0, 150.0)


class TestGeoRssFeed(unittest.TestCase):
    """Test cases for GeoRSS feed."""

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send.return_value.ok = True
        mock_session.return_value.__enter__.return_value.send.return_value.text = (
            load_fixture("generic_feed_1.xml")
        )

        feed = MockGeoRssFeed(HOME_COORDINATES_1, None)
        assert (
            repr(feed) == "<MockGeoRssFeed(home=(-31.0, 151.0), "
            "url=None, radius=None, categories=None)>"
        )
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
        assert feed_entry.external_id == hash(feed_entry.coordinates)

        feed_entry = entries[4]
        assert feed_entry.title == "Title 5"
        assert feed_entry.external_id == "5678"

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_feed_2(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send.return_value.ok = True
        mock_session.return_value.__enter__.return_value.send.return_value.text = (
            load_fixture("generic_feed_2.xml")
        )

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
        mock_session.return_value.__enter__.return_value.send.return_value.ok = True
        mock_session.return_value.__enter__.return_value.send.return_value.text = (
            load_fixture("generic_feed_3.xml")
        )

        feed = MockGeoRssFeed(HOME_COORDINATES_1, None)
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 3

        feed_entry = entries[0]
        assert feed_entry.external_id == "1234"
        assert feed_entry.coordinates == (
            pytest.approx(-34.93728111547821),
            pytest.approx(148.59710883878262),
        )
        self.assertAlmostEqual(feed_entry.distance_to_home, 491.7, 1)

        feed_entry = entries[1]
        assert feed_entry.external_id == "2345"
        assert feed_entry.coordinates == (-34.937170989, 148.597182317)
        self.assertAlmostEqual(feed_entry.distance_to_home, 491.8, 1)

        feed_entry = entries[2]
        assert feed_entry.external_id == "3456"
        assert feed_entry.coordinates == (
            pytest.approx(-29.962746645660683),
            pytest.approx(152.43090880416074),
        )
        self.assertAlmostEqual(feed_entry.distance_to_home, 176.5, 1)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_feed_6(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send.return_value.ok = True
        mock_session.return_value.__enter__.return_value.send.return_value.text = (
            load_fixture("generic_feed_6.xml")
        )

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
    def test_update_ok_with_radius_filtering(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send.return_value.ok = True
        mock_session.return_value.__enter__.return_value.send.return_value.text = (
            load_fixture("generic_feed_1.xml")
        )

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
    def test_update_ok_with_radius_and_category_filtering(
        self, mock_session, mock_request
    ):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send.return_value.ok = True
        mock_session.return_value.__enter__.return_value.send.return_value.text = (
            load_fixture("generic_feed_1.xml")
        )

        feed = MockGeoRssFeed(
            HOME_COORDINATES_2,
            None,
            filter_radius=90.0,
            filter_categories=["Category 2"],
        )
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 1
        self.assertAlmostEqual(entries[0].distance_to_home, 77.0, 1)

        feed = MockGeoRssFeed(
            HOME_COORDINATES_2,
            None,
            filter_radius=90.0,
            filter_categories=["Category 4"],
        )
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 0

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_error(self, mock_session, mock_request):
        """Test updating feed results in error."""
        mock_session.return_value.__enter__.return_value.send.return_value.ok = False

        feed = MockGeoRssFeed(HOME_COORDINATES_1, None)
        status, entries = feed.update()
        assert status == UPDATE_ERROR

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_with_request_exception(self, mock_session, mock_request):
        """Test updating feed raises exception."""
        mock_session.return_value.__enter__.return_value.send.side_effect = (
            requests.exceptions.RequestException
        )

        feed = GeoRssFeed(HOME_COORDINATES_1, None)
        status, entries = feed.update()
        assert status == UPDATE_ERROR
        self.assertIsNone(entries)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_bom(self, mock_session, mock_request):
        """Test updating feed with BOM (byte order mark) is ok."""
        mock_session.return_value.__enter__.return_value.send.return_value.ok = True
        mock_session.return_value.__enter__.return_value.send.return_value.text = (
            load_fixture("xml_parser_bom_1.xml")
        )

        feed = MockGeoRssFeed(HOME_COORDINATES_1, None)
        assert (
            repr(feed) == "<MockGeoRssFeed(home=(-31.0, 151.0), "
            "url=None, radius=None, categories=None)>"
        )
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 0
