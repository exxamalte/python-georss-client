"""Tests for XML parser."""
import datetime
import unittest

from georss_client.xml_parser import XmlParser
from georss_client.xml_parser.geometry import Point, Polygon
from tests.utils import load_fixture


class TestXmlParser(unittest.TestCase):
    """Test the XML parser."""

    def test_simple_1(self):
        """Test parsing various actual XML files."""
        xml_parser = XmlParser()
        xml = load_fixture('xml_parser_simple_1.xml')
        feed = xml_parser.parse(xml)
        self.assertIsNotNone(feed)
        self.assertIsNotNone(feed.entries)
        assert len(feed.entries) == 1

    def test_simple_2(self):
        """Test parsing various actual XML files."""
        xml_parser = XmlParser()
        xml = load_fixture('xml_parser_simple_2.xml')
        feed = xml_parser.parse(xml)
        self.assertIsNotNone(feed)
        self.assertIsNotNone(feed.entries)
        assert len(feed.entries) == 1

    def test_simple_3(self):
        """Test parsing various actual XML files."""
        xml_parser = XmlParser()
        xml = load_fixture('xml_parser_simple_3.xml')
        feed = xml_parser.parse(xml)
        self.assertIsNone(feed)

    def test_complex_1(self):
        """Test parsing various actual XML files."""
        xml_parser = XmlParser()
        xml = load_fixture('xml_parser_complex_1.xml')
        feed = xml_parser.parse(xml)
        self.assertIsNotNone(feed)

        assert feed.title == "Feed Title 1"
        assert feed.subtitle == "Feed Subtitle 1"
        assert feed.description == "Feed Description 1"
        assert feed.summary == "Feed Description 1"
        assert feed.content == "Feed Description 1"
        assert feed.link == "Feed Link 1"
        assert feed.published_date \
            == datetime.datetime(2018, 12, 9, 8, 30,
                                 tzinfo=datetime.timezone.utc)
        assert feed.pub_date \
            == datetime.datetime(2018, 12, 9, 8, 30,
                                 tzinfo=datetime.timezone.utc)
        assert feed.updated_date \
            == datetime.datetime(2018, 12, 9, 8, 45,
                                 tzinfo=datetime.timezone.utc)
        assert feed.last_build_date \
            == datetime.datetime(2018, 12, 9, 8, 45,
                                 tzinfo=datetime.timezone.utc)
        assert feed.copyright == "Feed Copyright 1"
        assert feed.rights == "Feed Copyright 1"
        assert feed.generator == "Feed Generator 1"
        assert feed.language == "Feed Language 1"
        assert feed.docs == "http://docs.url/documentation.html"
        assert feed.ttl == 42
        assert feed.author == "Feed Author 1"
        assert feed.contributor == "Feed Author 1"
        assert feed.managing_editor == "Feed Author 1"
        assert feed.category == ["Feed Category 1"]
        self.assertIsNotNone(feed.image)
        assert feed.image.title == "Image Title 1"
        assert feed.image.url == "http://image.url/image.png"
        assert feed.image.link == "http://feed.link/feed.rss"
        assert feed.image.description == "Image Description 1"
        assert feed.image.width == 123
        assert feed.image.height == 234
        assert feed.get_additional_attribute('random') == "Feed Random 1"
        assert repr(feed) == "<Feed(Feed Link 1)>"

        self.assertIsNotNone(feed.entries)
        assert len(feed.entries) == 6

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
        assert feed_entry.id == "GUID 1"
        assert feed_entry.source == "Source 1"
        assert feed_entry.category == ["Category 1"]
        self.assertIsInstance(feed_entry.geometry, Point)
        assert feed_entry.geometry.latitude == -37.4567
        assert feed_entry.geometry.longitude == 149.3456
        assert feed_entry.get_additional_attribute('random') == "Random 1"
        assert repr(feed_entry) == "<FeedItem(GUID 1)>"

        feed_entry = feed.entries[1]
        assert feed_entry.title == "Title 2"
        assert feed_entry.description == "Description 2"
        assert feed_entry.link == "Link 2"
        assert feed_entry.published_date \
            == datetime.datetime(2018, 12, 9, 7, 35,
                                 tzinfo=datetime.timezone.utc)
        assert feed_entry.updated_date \
            == datetime.datetime(2018, 12, 9, 7, 50,
                                 tzinfo=datetime.timezone.utc)
        assert feed_entry.guid == "GUID 2"
        assert feed_entry.category == ["Category 2"]
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
        assert feed_entry.category == ["Category 3A",
                                       "Category 3B",
                                       "Category 3C"]
        self.assertIsInstance(feed_entry.geometry, Point)
        assert feed_entry.geometry.latitude == -37.6789
        assert feed_entry.geometry.longitude == 149.5678

        feed_entry = feed.entries[3]
        assert feed_entry.title == "Title 4"
        assert feed_entry.description == "Description 4"
        assert feed_entry.author == "Author 4"
        assert feed_entry.contributor == "Author 4"
        assert feed_entry.category == ["Category 4A",
                                       "Category 4B"]
        assert feed_entry.published_date == datetime.datetime(
            2018, 9, 30, 21, 36, 48,
            tzinfo=datetime.timezone(datetime.timedelta(hours=10), 'AEST'))
        self.assertIsInstance(feed_entry.geometry, Point)
        assert feed_entry.geometry.latitude == -37.789
        assert feed_entry.geometry.longitude == 149.6789

        feed_entry = feed.entries[4]
        assert feed_entry.title == "Title 5"
        assert feed_entry.description == "Description 5"
        assert feed_entry.published_date == datetime.datetime(
            2018, 9, 20, 18, 1, 55,
            tzinfo=datetime.timezone(datetime.timedelta(hours=2), 'CEST'))
        self.assertIsInstance(feed_entry.geometry, Polygon)
        assert feed_entry.geometry.centroid.latitude == -30.32
        assert feed_entry.geometry.centroid.longitude == 150.32

        feed_entry = feed.entries[5]
        assert feed_entry.title == "Title 6"
        assert feed_entry.description == "Description 6"
        assert feed_entry.published_date == datetime.datetime(
            2018, 10, 7, 19,52,
            tzinfo=datetime.timezone(datetime.timedelta(hours=-7), 'PDT'))
        self.assertIsInstance(feed_entry.geometry, Polygon)
        assert feed_entry.geometry.centroid.latitude == -30.32
        assert feed_entry.geometry.centroid.longitude == 150.32

    def test_complex_2(self):
        """Test parsing various actual XML files."""
        xml_parser = XmlParser()
        xml = load_fixture('xml_parser_complex_2.xml')
        feed = xml_parser.parse(xml)
        self.assertIsNotNone(feed)

        assert feed.title == "Feed Title 1"
        assert feed.subtitle == "Feed Subtitle 1"
        assert feed.ttl == "INVALID"
        assert feed.author == "Author 1"
        assert feed.last_build_date \
            == datetime.datetime(2018, 12, 9, 9, 0,
                                 tzinfo=datetime.timezone.utc)
        assert feed.updated_date \
            == datetime.datetime(2018, 12, 9, 9, 0,
                                 tzinfo=datetime.timezone.utc)
        assert feed.copyright == "Feed Rights 1"
        assert feed.rights == "Feed Rights 1"
        assert feed.generator == "Feed Generator 1"
        self.assertIsNotNone(feed.image)
        assert feed.image.title == "Image Title 1"
        assert feed.image.url == "http://image.url/image.png"
        assert feed.image.link == "http://feed.link/feed.rss"
        self.assertIsNone(feed.image.description)
        self.assertIsNone(feed.image.width)
        self.assertIsNone(feed.image.height)
        self.assertIsNone(feed.docs)

        self.assertIsNotNone(feed.entries)
        assert len(feed.entries) == 1

        feed_entry = feed.entries[0]
        assert feed_entry.title == "Title 6"
        self.assertIsNone(feed_entry.published_date)

    def test_complex_3(self):
        """Test parsing various actual XML files."""
        xml_parser = XmlParser()
        xml = load_fixture('xml_parser_complex_3.xml')
        feed = xml_parser.parse(xml)
        self.assertIsNotNone(feed)

        self.assertIsNone(feed.title)
        self.assertIsNone(feed.subtitle)
        self.assertIsNone(feed.description)
        self.assertIsNone(feed.language)
        self.assertIsNone(feed.published_date)
        self.assertIsNone(feed.last_build_date)
        self.assertIsNone(feed.ttl)
        assert feed.rights == "Feed Rights 1"
        self.assertIsNone(feed.image)

        self.assertIsNotNone(feed.entries)
        assert len(feed.entries) == 2

        feed_entry = feed.entries[0]
        self.assertIsNone(feed_entry.title)
        self.assertIsNone(feed_entry.published_date)
        self.assertIsNone(feed_entry.geometry)

        feed_entry = feed.entries[1]
        self.assertIsNone(feed_entry.title)
        self.assertIsNone(feed_entry.geometry)


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
