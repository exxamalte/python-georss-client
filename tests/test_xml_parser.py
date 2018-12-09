"""Tests for XML parser."""
import datetime
import unittest

from georss_client.xml_parser import XmlParser, Point, Polygon
from tests.utils import load_fixture


class TestXmlParser(unittest.TestCase):
    """Test the XML parser."""

    def test_simple_1(self):
        xml_parser = XmlParser()
        xml = load_fixture('xml_parser_simple_1.xml')
        feed = xml_parser.parse(xml)
        self.assertIsNotNone(feed)
        self.assertIsNotNone(feed.entries)
        assert len(feed.entries) == 1

    def test_simple_2(self):
        xml_parser = XmlParser()
        xml = load_fixture('xml_parser_simple_2.xml')
        feed = xml_parser.parse(xml)
        self.assertIsNotNone(feed)
        self.assertIsNotNone(feed.entries)
        assert len(feed.entries) == 1

    def test_simple_3(self):
        xml_parser = XmlParser()
        xml = load_fixture('xml_parser_simple_3.xml')
        feed = xml_parser.parse(xml)
        self.assertIsNone(feed)

    def test_complex_1(self):
        xml_parser = XmlParser()
        xml = load_fixture('xml_parser_complex_1.xml')
        feed = xml_parser.parse(xml)
        self.assertIsNotNone(feed)

        assert feed.title == "Feed Title 1"
        assert feed.description == "Feed Description 1"
        assert feed.link == "Feed Link 1"
        assert feed.published_date \
            == datetime.datetime(2018, 12, 9, 8, 30,
                                 tzinfo=datetime.timezone.utc)
        assert feed.updated_date \
            == datetime.datetime(2018, 12, 9, 8, 45,
                                 tzinfo=datetime.timezone.utc)
        assert feed.copyright == "Feed Copyright 1"
        assert feed.generator == "Feed Generator 1"
        assert feed.language == "Feed Language 1"
        assert feed.last_build_date \
            == datetime.datetime(2018, 12, 9, 9, 0,
                                 tzinfo=datetime.timezone.utc)
        assert feed.ttl == 42
        assert feed.author == "Feed Author 1"
        assert feed.get_additional_attribute('random') == "Feed Random 1"
        assert repr(feed) == "<Feed(Feed Link 1)>"

        self.assertIsNotNone(feed.entries)
        assert len(feed.entries) == 5

        feed_entry = feed.entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.description == "Description 1"
        assert feed_entry.link == "Link 1"
        assert feed_entry.published_date \
            == datetime.datetime(2018, 12, 9, 7, 30,
                                 tzinfo=datetime.timezone.utc)
        assert feed_entry.updated_date \
            == datetime.datetime(2018, 12, 9, 7, 45,
                                 tzinfo=datetime.timezone.utc)
        assert feed_entry.guid == "GUID 1"
        assert feed_entry.source == "Source 1"
        assert feed_entry.category == "Category 1"
        self.assertIsInstance(feed_entry.geometry, Point)
        assert feed_entry.geometry.latitude == -37.4567
        assert feed_entry.geometry.longitude == 149.3456
        assert feed_entry.get_additional_attribute('random') == "Random 1"
        assert repr(feed_entry) == "<FeedItem(GUID 1)>"

        feed_entry = feed.entries[1]
        assert feed_entry.title == "Title 2"
        assert feed_entry.description == "Description 2"
        assert feed_entry.published_date \
            == datetime.datetime(2018, 12, 9, 7, 35,
                                 tzinfo=datetime.timezone.utc)
        assert feed_entry.updated_date \
            == datetime.datetime(2018, 12, 9, 7, 50,
                                 tzinfo=datetime.timezone.utc)
        assert feed_entry.guid == "GUID 2"
        assert feed_entry.category == "Category 2"
        self.assertIsInstance(feed_entry.geometry, Point)
        assert feed_entry.geometry.latitude == -37.5678
        assert feed_entry.geometry.longitude == 149.4567

        feed_entry = feed.entries[2]
        assert feed_entry.title == "Title 3"
        assert feed_entry.description == "Description 3"
        assert feed_entry.published_date \
            == datetime.datetime(2018, 12, 9, 7, 40,
                                 tzinfo=datetime.timezone.utc)
        assert feed_entry.updated_date \
            == datetime.datetime(2018, 12, 9, 7, 55,
                                 tzinfo=datetime.timezone.utc)
        assert feed_entry.guid == "GUID 3"
        self.assertIsInstance(feed_entry.geometry, Point)
        assert feed_entry.geometry.latitude == -37.6789
        assert feed_entry.geometry.longitude == 149.5678

        feed_entry = feed.entries[3]
        assert feed_entry.title == "Title 4"
        self.assertIsInstance(feed_entry.geometry, Point)
        assert feed_entry.geometry.latitude == -37.789
        assert feed_entry.geometry.longitude == 149.6789

        feed_entry = feed.entries[4]
        assert feed_entry.title == "Title 5"
        self.assertIsInstance(feed_entry.geometry, Polygon)
        assert feed_entry.geometry.centroid.latitude == -30.32
        assert feed_entry.geometry.centroid.longitude == 150.32

    def test_complex_2(self):
        xml_parser = XmlParser()
        xml = load_fixture('xml_parser_complex_2.xml')
        feed = xml_parser.parse(xml)
        self.assertIsNotNone(feed)

        assert feed.title == "Feed Title 1"
        assert feed.ttl == "INVALID"

        self.assertIsNotNone(feed.entries)
        assert len(feed.entries) == 1

        feed_entry = feed.entries[0]
        assert feed_entry.title == "Title 6"
        self.assertIsNone(feed_entry.published_date)


class TestGeometries(unittest.TestCase):
    """Test geometries."""

    def test_point(self):
        """Test point."""
        point = Point(-37.1234, 149.2345)
        assert point.latitude == -37.1234
        assert point.longitude == 149.2345
        assert repr(point) == "<Point(latitude=-37.1234, longitude=149.2345)>"

    def test_polygon(self):
        """Test polygon."""
        polygon = Polygon([
            Point(-30.1, 150.1),
            Point(-30.2, 150.2),
            Point(-30.4, 150.4),
            Point(-30.8, 150.8),
            Point(-30.1, 150.1)
        ])
        assert len(polygon.points) == 5
        assert polygon.centroid.latitude == -30.32
        assert polygon.centroid.longitude == 150.32
        assert repr(polygon) == "<Polygon(centroid=" \
                                "<Point(latitude=-30.32, longitude=150.32)>)>"
