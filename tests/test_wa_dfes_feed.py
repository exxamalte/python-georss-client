"""Test for the Department of Fire and Emergency Services (DFES) feed."""
import datetime
import unittest
from unittest import mock

from georss_client import UPDATE_OK
from georss_client.exceptions import GeoRssException
from georss_client.wa_dfes_feed import WaDfesFeed, WaDfesFeedManager
from tests.utils import load_fixture

HOME_COORDINATES = (-31.0, 121.0)


class TestWaDfesFeed(unittest.TestCase):
    """Test the Department of Fire and Emergency Services (DFES) feed."""

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_warnings(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('wa_dfes_warnings_feed.xml')

        feed = WaDfesFeed(HOME_COORDINATES, 'warnings')
        assert repr(feed) == "<WaDfesFeed(home=(-31.0, 121.0), " \
                             "url=https://www.emergency.wa.gov.au/data/" \
                             "message.rss, radius=None, " \
                             "categories=None)>"
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 2

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.coordinates == (-30.97304, 121.30196)
        self.assertAlmostEqual(feed_entry.distance_to_home, 28.9, 1)
        assert feed_entry.published \
            == datetime.datetime(2018, 9, 30, 8, 30,
                                 tzinfo=datetime.timezone.utc)
        assert feed_entry.category == "Category 1"
        assert feed_entry.region == "Region 1"
        assert feed_entry.attribution == "Department of Fire and Emergency " \
                                         "Services"
        assert repr(feed_entry) == "<WaDfesWarningsFeedEntry(id=1234)>"

        feed_entry = entries[1]
        assert feed_entry.title == "Title 2"
        self.assertIsNone(feed_entry.published)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_warnings_with_category(self, mock_session,
                                              mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('wa_dfes_warnings_feed.xml')

        feed = WaDfesFeed(HOME_COORDINATES, 'warnings',
                          filter_categories=['Category 1'])
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 1

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_all_incidents(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('wa_dfes_all_incidents_feed.xml')

        feed = WaDfesFeed(HOME_COORDINATES, 'all_incidents')
        assert repr(feed) == "<WaDfesFeed(home=(-31.0, 121.0), " \
                             "url=https://www.emergency.wa.gov.au/data/" \
                             "incident_FCAD.rss, radius=None, " \
                             "categories=None)>"
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 2

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.coordinates == (-23.12641, 119.94800)
        self.assertAlmostEqual(feed_entry.distance_to_home, 881.7, 1)
        assert feed_entry.published \
            == datetime.datetime(2018, 9, 30, 8, 30)
        assert feed_entry.category == "Category 1"
        assert feed_entry.region == "Region 1"
        assert feed_entry.attribution == "Department of Fire and Emergency " \
                                         "Services"
        assert repr(feed_entry) == "<WaDfesAllIncidentsFeedEntry(id=1234)>"

        feed_entry = entries[1]
        assert feed_entry.title == "Title 2"
        self.assertIsNone(feed_entry.published)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_all_incidents_with_category(self, mock_session,
                                                   mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('wa_dfes_all_incidents_feed.xml')

        feed = WaDfesFeed(HOME_COORDINATES, 'all_incidents',
                          filter_categories=['Category 1'])
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 1

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"

    def test_update_wrong_feed(self):
        """Test invalid feed name."""
        with self.assertRaises(GeoRssException):
            WaDfesFeed(HOME_COORDINATES, 'DOES NOT EXIST')

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_feed_manager(self, mock_session, mock_request):
        """Test the feed manager."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture(
                'wa_dfes_warnings_feed.xml')

        # This will just record calls and keep track of external ids.
        generated_entity_external_ids = []
        updated_entity_external_ids = []
        removed_entity_external_ids = []

        def _generate_entity(external_id):
            """Generate new entity."""
            generated_entity_external_ids.append(external_id)

        def _update_entity(external_id):
            """Update entity."""
            updated_entity_external_ids.append(external_id)

        def _remove_entity(external_id):
            """Remove entity."""
            removed_entity_external_ids.append(external_id)

        feed_manager = WaDfesFeedManager(
            _generate_entity,
            _update_entity,
            _remove_entity,
            HOME_COORDINATES,
            'warnings')
        assert repr(feed_manager) == "<WaDfesFeedManager(" \
                                     "feed=<WaDfesFeed(home=" \
                                     "(-31.0, 121.0), " \
                                     "url=https://www.emergency.wa.gov.au/" \
                                     "data/message.rss, " \
                                     "radius=None, categories=None)>)>"
        feed_manager.update()
        entries = feed_manager.feed_entries
        self.assertIsNotNone(entries)
        assert len(entries) == 2
        assert feed_manager.last_timestamp \
            == datetime.datetime(2018, 9, 30, 8, 30,
                                 tzinfo=datetime.timezone.utc)
        assert len(generated_entity_external_ids) == 2
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0
