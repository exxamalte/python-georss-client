"""Test for the generic georss feed."""
import datetime
import requests
import unittest
from unittest import mock

from georss_client import UPDATE_ERROR, UPDATE_OK
from georss_client.generic_feed import GenericFeed, GenericFeedManager
from tests.utils import load_fixture

HOME_COORDINATES_1 = (-31.0, 151.0)
HOME_COORDINATES_2 = (-37.0, 150.0)


class TestGenericFeed(unittest.TestCase):
    """Test the generic feed."""

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_1.xml')

        feed = GenericFeed(HOME_COORDINATES_1, None)
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
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_2.xml')

        feed = GenericFeed(HOME_COORDINATES_1, None)
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

        feed = GenericFeed(HOME_COORDINATES_1, None)
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

        feed = GenericFeed(HOME_COORDINATES_2, None, filter_radius=90.0)
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

        feed = GenericFeed(HOME_COORDINATES_2, None, filter_radius=90.0,
                           filter_categories=['Category 2'])
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 1
        self.assertAlmostEqual(entries[0].distance_to_home, 77.0, 1)

        feed = GenericFeed(HOME_COORDINATES_2, None, filter_radius=90.0,
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

        feed = GenericFeed(HOME_COORDINATES_1, None)
        status, entries = feed.update()
        assert status == UPDATE_ERROR

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_with_request_exception(self, mock_session, mock_request):
        """Test updating feed raises exception."""
        mock_session.return_value.__enter__.return_value.send\
            .side_effect = requests.exceptions.RequestException

        feed = GenericFeed(HOME_COORDINATES_1, None)
        status, entries = feed.update()
        assert status == UPDATE_ERROR
        self.assertIsNone(entries)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_feed_manager(self, mock_session, mock_request):
        """Test the feed manager."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture(
                'generic_feed_1.xml')

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

        feed_manager = GenericFeedManager(
            _generate_entity,
            _update_entity,
            _remove_entity,
            HOME_COORDINATES_1,
            None)
        assert repr(feed_manager) == "<GenericFeedManager(" \
                                     "feed=<GenericFeed(home=" \
                                     "(-31.0, 151.0), url=None, " \
                                     "radius=None, categories=None)>)>"
        feed_manager.update()
        entries = feed_manager.feed_entries
        self.assertIsNotNone(entries)
        assert len(entries) == 5
        self.assertIsNotNone(feed_manager.last_update)
        assert feed_manager.last_timestamp \
            == datetime.datetime(2018, 9, 23, 9, 10)
        assert len(generated_entity_external_ids) == 5
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0

        feed_entry = entries.get("1234")
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.coordinates == (-37.2345, 149.1234)
        self.assertAlmostEqual(feed_entry.distance_to_home, 714.4, 1)
        assert repr(feed_entry) == "<GenericFeedEntry(id=1234)>"

        feed_entry = entries.get("2345")
        assert feed_entry.title == "Title 2"
        assert feed_entry.external_id == "2345"

        feed_entry = entries.get("Title 3")
        assert feed_entry.title == "Title 3"
        assert feed_entry.external_id == "Title 3"

        feed_entry = entries.get(-7266545992534134585)
        self.assertIsNone(feed_entry.title)
        assert feed_entry.external_id == -7266545992534134585

        feed_entry = entries.get("5678")
        assert feed_entry.title == "Title 5"
        assert feed_entry.external_id == "5678"

        # Simulate an update with several changes.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()

        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_4.xml')

        feed_manager.update()
        entries = feed_manager.feed_entries
        self.assertIsNotNone(entries)
        assert len(entries) == 3
        assert len(generated_entity_external_ids) == 1
        assert len(updated_entity_external_ids) == 2
        assert len(removed_entity_external_ids) == 3

        feed_entry = entries.get("1234")
        assert feed_entry.title == "Title 1 UPDATED"

        feed_entry = entries.get("2345")
        assert feed_entry.title == "Title 2"

        feed_entry = entries.get("6789")
        assert feed_entry.title == "Title 6"

        # Simulate an update with no data.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()

        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = False

        feed_manager.update()
        entries = feed_manager.feed_entries

        assert len(entries) == 0
        assert len(generated_entity_external_ids) == 0
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 3
