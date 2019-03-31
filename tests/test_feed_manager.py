"""Test for the Feed Manager."""
import datetime
import unittest
from unittest import mock

from georss_client.feed_manager import FeedManagerBase
from tests import MockGeoRssFeed
from tests.utils import load_fixture

HOME_COORDINATES_1 = (-31.0, 151.0)
HOME_COORDINATES_2 = (-37.0, 150.0)


class TestFeedManager(unittest.TestCase):

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_feed_manager(self, mock_session, mock_request):
        """Test the feed manager."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_1.xml')

        feed = MockGeoRssFeed(HOME_COORDINATES_1, None)

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

        feed_manager = FeedManagerBase(
            feed,
            _generate_entity,
            _update_entity,
            _remove_entity)
        assert repr(feed_manager) == "<FeedManagerBase(" \
                                     "feed=<MockGeoRssFeed(home=" \
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
        assert repr(feed_entry) == "<FeedEntry(id=1234)>"

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

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_feed_manager_no_timestamp(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture('generic_feed_5.xml')

        feed = MockGeoRssFeed(HOME_COORDINATES_1, None)

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

        feed_manager = FeedManagerBase(
            feed,
            _generate_entity,
            _update_entity,
            _remove_entity)
        assert repr(feed_manager) == "<FeedManagerBase(" \
                                     "feed=<MockGeoRssFeed(home=" \
                                     "(-31.0, 151.0), url=None, " \
                                     "radius=None, categories=None)>)>"
        feed_manager.update()
        entries = feed_manager.feed_entries
        self.assertIsNotNone(entries)
        assert len(entries) == 1
        self.assertIsNone(feed_manager.last_timestamp)
