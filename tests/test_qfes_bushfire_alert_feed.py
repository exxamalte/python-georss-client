"""Test for the QFES Bushfire Alert feed."""
import datetime
import unittest
from unittest import mock

from georss_client import UPDATE_OK
from georss_client.qfes_bushfire_alert_feed import \
    QfesBushfireAlertFeed
from tests.utils import load_fixture


class TestQfesBushfireAlertFeed(unittest.TestCase):
    """Test the QFES Bushfire Alert feed."""

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok(self, mock_session, mock_request):
        """Test updating feed is ok."""
        home_coordinates = (-31.0, 151.0)
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('qfes_bushfire_alert_feed.xml')

        feed = QfesBushfireAlertFeed(home_coordinates)
        assert repr(feed) == "<QfesBushfireAlertFeed(home=(-31.0, 151.0), " \
                             "url=https://www.qfes.qld.gov.au/data/alerts/" \
                             "bushfireAlert.xml, radius=None, categories=" \
                             "None)>"
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 2

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.coordinates == (-32.2345, 149.1234)
        self.assertAlmostEqual(feed_entry.distance_to_home, 224.5, 1)
        assert feed_entry.published == datetime.datetime(2018, 9, 27, 8, 0)
        assert feed_entry.updated == datetime.datetime(2018, 9, 27, 8, 30)
        assert feed_entry.status == "Status 1"
        assert feed_entry.attribution == "Author 1"
        assert repr(feed_entry) == "<QfesBushfireAlertFeedEntry(id=1234)>"

        feed_entry = entries[1]
        assert feed_entry.title == "Title 2"
        self.assertIsNone(feed_entry.published)
        self.assertIsNone(feed_entry.updated)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_with_category(self, mock_session, mock_request):
        """Test updating feed is ok."""
        home_coordinates = (-31.0, 151.0)
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('qfes_bushfire_alert_feed.xml')

        feed = QfesBushfireAlertFeed(
            home_coordinates,
            filter_categories=['Category 1'])
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 1

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
