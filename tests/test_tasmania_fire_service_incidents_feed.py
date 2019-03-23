"""Test for the Tasmania Fire Service Incidents feed."""
import datetime
import unittest
from unittest import mock

from georss_client import UPDATE_OK
from georss_client.tasmania_fire_service_incidents_feed import \
    TfsIncidentsFeed, TfsIncidentsFeedManager
from tests.utils import load_fixture

HOME_COORDINATES = (-42.0, 147.0)


class TestTfsIncidentsFeed(unittest.TestCase):
    """Test the Tasmania Fire Service Incidents feed."""

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('tasmania_fire_service_incidents_feed.xml')

        feed = TfsIncidentsFeed(HOME_COORDINATES)
        assert repr(feed) == "<TfsIncidentsFeed(home=(-42.0, 147.0), " \
                             "url=http://www.fire.tas.gov.au/Show?pageId=" \
                             "colBushfireSummariesRss, radius=None, " \
                             "categories=None)>"
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 2

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.coordinates == (-42.123456, 147.234567)
        self.assertAlmostEqual(feed_entry.distance_to_home, 23.7, 1)
        assert feed_entry.published \
            == datetime.datetime(2018, 9, 29, 15, 30,
                                 tzinfo=datetime.timezone.utc)
        assert feed_entry.location == "Location 1"
        assert feed_entry.region == "Region 1"
        assert feed_entry.responsible_agency == "Agency 1"
        assert feed_entry.status == "Status 1"
        assert feed_entry.size == "Size 1"
        assert feed_entry.type == "Type 1"
        assert feed_entry.attribution == "Tasmania Fire Service"
        assert repr(feed_entry) == "<TfsIncidentsFeedEntry(id=1234)>"

        feed_entry = entries[1]
        assert feed_entry.title == "Title 2"
        self.assertIsNone(feed_entry.published)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_with_category(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('tasmania_fire_service_incidents_feed.xml')

        feed = TfsIncidentsFeed(HOME_COORDINATES,
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
    def test_feed_manager(self, mock_session, mock_request):
        """Test the feed manager."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture(
                'tasmania_fire_service_incidents_feed.xml')

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

        feed_manager = TfsIncidentsFeedManager(
            _generate_entity,
            _update_entity,
            _remove_entity,
            HOME_COORDINATES)
        assert repr(feed_manager) == "<TfsIncidentsFeedManager(" \
                                     "feed=<TfsIncidentsFeed(home=" \
                                     "(-42.0, 147.0), url=http://www.fire." \
                                     "tas.gov.au/Show?pageId=" \
                                     "colBushfireSummariesRss, " \
                                     "radius=None, categories=None)>)>"
        feed_manager.update()
        entries = feed_manager.feed_entries
        self.assertIsNotNone(entries)
        assert len(entries) == 2
        assert feed_manager.last_timestamp \
            == datetime.datetime(2018, 9, 29, 15, 30,
                                 tzinfo=datetime.timezone.utc)
        assert len(generated_entity_external_ids) == 2
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0
