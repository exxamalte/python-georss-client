"""Test for the IGN Instituto Geográfico Nacional Sismología feed."""
import datetime
import unittest
from unittest import mock

from georss_client import UPDATE_OK
from georss_client.ign_sismologia_feed import IgnSismologiaFeed, ATTRIBUTION, \
    IgnSismologiaFeedManager
from tests.utils import load_fixture

HOME_COORDINATES = (40.38, -3.72)


class TestIgnSismologiaFeed(unittest.TestCase):
    """Test the IGN Instituto Geográfico Nacional Sismología feed."""

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('ign_sismologia_feed.xml')

        feed = IgnSismologiaFeed(HOME_COORDINATES)
        assert repr(feed) == "<IgnSismologiaFeed(home=" \
                             "(40.38, -3.72), url=http://www.ign.es/ign/" \
                             "RssTools/sismologia.xml, radius=None, " \
                             "magnitude=None)>"
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 3

        feed_entry = entries[0]
        assert feed_entry.title == "-Info.terremoto: 18/03/2019 19:34:55"
        assert feed_entry.external_id == "http://www.ign.es/web/ign/portal/" \
                                         "sis-catalogo-terremotos/-/" \
                                         "catalogo-terremotos/" \
                                         "detailTerremoto?evid=es2019dfcfp"
        assert feed_entry.coordinates == (27.62, -18.0859)
        self.assertAlmostEqual(feed_entry.distance_to_home, 1935.7, 1)
        assert feed_entry.published \
            == datetime.datetime(2019, 3, 18, 19, 34, 55)
        assert feed_entry.region == "SW EL PINAR DE EL HIERRO.IHI"
        assert feed_entry.magnitude == 3.1
        assert feed_entry.attribution == ATTRIBUTION
        assert feed_entry.image_url == "http://www.ign.es/web/resources/" \
                                       "sismologia/www/" \
                                       "dir_images_terremotos/detalle/" \
                                       "es2019dfcfp.gif"
        assert repr(feed_entry) == "<IgnSismologiaFeedEntry" \
                                   "(id=http://www.ign.es/web/ign/portal/" \
                                   "sis-catalogo-terremotos/-/" \
                                   "catalogo-terremotos/detailTerremoto?" \
                                   "evid=es2019dfcfp)>"

        feed_entry = entries[1]
        assert feed_entry.title == "-Info.terremoto: NO DATE"
        assert feed_entry.external_id == "ITEM_ID"
        self.assertIsNone(feed_entry.image_url)
        self.assertIsNone(feed_entry.region)
        self.assertIsNone(feed_entry.magnitude)
        self.assertIsNone(feed_entry.published)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_with_category(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('ign_sismologia_feed.xml')

        feed = IgnSismologiaFeed(HOME_COORDINATES,
                                 filter_minimum_magnitude=3.0)
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 2

        feed_entry = entries[0]
        assert feed_entry.title == "-Info.terremoto: 18/03/2019 19:34:55"
        assert feed_entry.external_id == "http://www.ign.es/web/ign/portal/" \
                                         "sis-catalogo-terremotos/-/" \
                                         "catalogo-terremotos/" \
                                         "detailTerremoto?evid=es2019dfcfp"

        feed_entry = entries[1]
        assert feed_entry.title == "-Info.terremoto: 18/03/2019 1:11:35"
        assert feed_entry.external_id == "http://www.ign.es/web/ign/portal/" \
                                         "sis-catalogo-terremotos/-/" \
                                         "catalogo-terremotos/" \
                                         "detailTerremoto?evid=es2019dejoe"

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_feed_manager(self, mock_session, mock_request):
        """Test the feed manager."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture(
                'ign_sismologia_feed.xml')

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

        feed_manager = IgnSismologiaFeedManager(_generate_entity,
                                                _update_entity,
                                                _remove_entity,
                                                HOME_COORDINATES)
        assert repr(feed_manager) == "<IgnSismologiaFeedManager(" \
                                     "feed=<IgnSismologiaFeed(home=" \
                                     "(40.38, -3.72), " \
                                     "url=http://www.ign.es/ign/" \
                                     "RssTools/sismologia.xml, " \
                                     "radius=None, magnitude=None)>)>"
        feed_manager.update()
        entries = feed_manager.feed_entries
        self.assertIsNotNone(entries)
        assert len(entries) == 3
        assert feed_manager.last_timestamp \
            == datetime.datetime(2019, 3, 18, 19, 34, 55)
        assert len(generated_entity_external_ids) == 3
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0
