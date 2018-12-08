"""Test for the INGV Centro Nazionale Terremoti feed."""
import datetime
import unittest
from unittest import mock

from georss_client import UPDATE_OK
from georss_client.ingv_centro_nazionale_terremoti_feed import \
    IngvCentroNazionaleTerremotiFeed
from tests.utils import load_fixture


class TestIngvCentroNazionaleTerremotiFeed(unittest.TestCase):
    """Test the INGV Centro Nazionale Terremoti feed."""

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok(self, mock_session, mock_request):
        """Test updating feed is ok."""
        home_coordinates = (40.84, 14.25)
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('ingv_centro_nazionale_terremoti_feed.xml')

        feed = IngvCentroNazionaleTerremotiFeed(home_coordinates)
        assert repr(feed) == "<IngvCentroNazionaleTerremotiFeed(home=" \
                             "(40.84, 14.25), url=http://cnt.rm.ingv.it/" \
                             "feed/atom/all_week, radius=None, " \
                             "magnitude=None)>"
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 2

        feed_entry = entries[0]
        assert feed_entry.title == "2018-10-06 10:21:33 UTC - Magnitude(ML)" \
                                   " 2.3 - 1 km NE Biancavilla (CT)"
        assert feed_entry.external_id == "smi:webservices.ingv.it/fdsnws/" \
                                         "event/1/query?eventId=1234"
        assert feed_entry.coordinates == (37.654, 14.878)
        self.assertAlmostEqual(feed_entry.distance_to_home, 358.4, 1)
        assert feed_entry.published \
            == datetime.datetime(2018, 10, 6, 8, 0,
                                 tzinfo=datetime.timezone.utc)
        assert feed_entry.updated \
            == datetime.datetime(2018, 10, 6, 8, 30,
                                 tzinfo=datetime.timezone.utc)
        assert feed_entry.region == "1 km NE Biancavilla (CT)"
        assert feed_entry.magnitude == 2.3
        assert feed_entry.attribution == "Istituto Nazionale di Geofisica " \
                                         "e Vulcanologia"
        assert repr(feed_entry) == "<IngvCentroNazionaleTerremotiFeedEntry" \
                                   "(id=smi:webservices.ingv.it/fdsnws/" \
                                   "event/1/query?eventId=1234)>"

        feed_entry = entries[1]
        assert feed_entry.title == "2018-10-06 09:14:11 UTC - Magnitude(ML)" \
                                   " 0.7 - 1 km NE Norcia (PG)"
        self.assertIsNone(feed_entry.published)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_with_category(self, mock_session, mock_request):
        """Test updating feed is ok."""
        home_coordinates = (40.84, 14.25)
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('ingv_centro_nazionale_terremoti_feed.xml')

        feed = IngvCentroNazionaleTerremotiFeed(home_coordinates,
                                                filter_minimum_magnitude=2.0)
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 1

        feed_entry = entries[0]
        assert feed_entry.title == "2018-10-06 10:21:33 UTC - Magnitude(ML)" \
                                   " 2.3 - 1 km NE Biancavilla (CT)"
        assert feed_entry.external_id == "smi:webservices.ingv.it/fdsnws/" \
                                         "event/1/query?eventId=1234"
