"""
RSS XML Parser with GeoRSS support.
"""
import dateparser as dateparser
import datetime
import logging
import xmltodict
from typing import Optional

_LOGGER = logging.getLogger(__name__)

KEYS_DATES = ['lastBuildDate', 'pubDate']
KEYS_INT = ['ttl']

NAMESPACES = {
    'http://www.w3.org/2005/Atom': None,
    'http://purl.org/dc/elements/1.1/': 'dc',
    'http://www.georss.org/georss': 'georss',
    'http://www.w3.org/2003/01/geo/wgs84_pos#': 'geo',
    'http://www.opengis.net/gml': 'gml',
    'http://www.gdacs.org/': 'gdacs',
}


class XmlParser:
    """Built-in XML parser."""

    def __init__(self, encoding):
        """Initialise the XML parser."""
        self._encoding = encoding
        self.parsed_xmltodict = None
        self.feed = None

    def parse(self, xml):
        """Parse the provided xml."""
        if xml:
            # Retain full control over namespaces.

            def postprocessor(path, key, value):
                """Conduct type conversion for selected keys."""
                try:
                    if key in KEYS_DATES:
                        return key, dateparser.parse(value)
                    if key in KEYS_INT:
                        return key, int(value)
                except (ValueError, TypeError):
                    # TODO: handle error
                    _LOGGER.warning("error")
                return key, value

            self.parsed_xmltodict = xmltodict.parse(
                xml, process_namespaces=True, namespaces=NAMESPACES,
                postprocessor=postprocessor)

            data = self.parsed_xmltodict
            if 'rss' in self.parsed_xmltodict:
                rss = self.parsed_xmltodict.get('rss')
                if 'channel' in rss:
                    channel = rss.get('channel')
                    data = channel

            self.feed = Feed(data)
            return self.feed
        return None


class Point:
    """Represents a point."""

    def __init__(self, latitude, longitude):
        """Initialise point."""
        self._latitude = latitude
        self._longitude = longitude

    def __repr__(self):
        """Return string representation of this point."""
        return '<{}(latitude={},longitude={})>'.format(
            self.__class__.__name__, self.latitude, self.longitude)

    @property
    def latitude(self) -> Optional[float]:
        return self._latitude

    @property
    def longitude(self) -> Optional[float]:
        return self._longitude

class FeedDictSource:
    """Represents a subset of a feed based on a dict."""

    def __init__(self, source):
        """Initialise feed."""
        self._source = source

    def __repr__(self):
        """Return string representation of this feed item."""
        return '<{}({})>'.format(
            self.__class__.__name__, self.link)

    def _attribute(self, names):
        if self._source and names:
            # Try each name, and return the first value that is not None.
            for name in names:
                value = self._source.get(name, None)
                if value:
                    return value
        return None

    @property
    def title(self) -> Optional[str]:
        return self._attribute(['title'])

    @property
    def description(self) -> Optional[str]:
        return self._attribute(['description', 'summary'])

    @property
    def link(self) -> Optional[str]:
        return self._attribute(['link'])

    @property
    def category(self) -> Optional[str]:
        # TODO: handle lists
        return self._attribute(['category'])

    @property
    def pub_date(self) -> Optional[datetime.datetime]:
        return self._attribute(['pubDate'])


class Feed(FeedDictSource):
    """Represents a feed."""
    # 'publisher'

    @property
    def author(self) -> Optional[str]:
        # <author>
        #   <name>Istituto Nazionale di Geofisica e Vulcanologia</name>
        #   <uri>http://www.ingv.it</uri>
        # </author>
        author = self._attribute(['author'])
        if author:
            name = author.get('name', None)
            return name
        return None

    @property
    def copyright(self) -> Optional[str]:
        return self._attribute(['copyright'])

    @property
    def generator(self) -> Optional[str]:
        return self._attribute(['generator'])

    @property
    def language(self) -> Optional[str]:
        return self._attribute(['language'])

    @property
    def last_build_date(self) -> Optional[datetime.datetime]:
        return self._attribute(['lastBuildDate'])

    @property
    def ttl(self) -> Optional[int]:
        return self._attribute(['ttl'])

    @property
    def entries(self):
        items = self._attribute(['item'])
        entries = []
        if items:
            for item in items:
                entries.append(FeedItem(item))
        return entries


class FeedItem(FeedDictSource):
    """Represents a feed item."""

    # 'dc:date' - <dc:date xmlns:dc="http://purl.org/dc/elements/1.1/">
    #               2018-10-01T13:19:56+00:00
    #             </dc:date>

    def __repr__(self):
        """Return string representation of this feed item."""
        return '<{}({})>'.format(
            self.__class__.__name__, self.guid)

    @property
    def guid(self) -> Optional[str]:
        return self._attribute(['guid'])

    @property
    def source(self) -> Optional[str]:
        return self._attribute(['source'])

    @property
    def geometry(self) -> Optional[Point]:
        # <georss:point>-0.5 119.8</georss:point>
        point = self._attribute(['georss:point'])
        if point:
            longitude = float(point.split(' ')[0])
            latitude = float(point.split(' ')[1])
            return Point(latitude, longitude)
        # <georss:where>
        #   <gml:Point>
        #     <gml:pos>44.11 -66.23</gml:pos>
        #   </gml:Point>
        # </georss:where>
        where = self._attribute(['georss:where'])
        if where:
            point = where.get('gml:Point')
            if point:
                pos = where.get('gml:pos')
                if pos:
                    longitude = float(pos.split(' ')[0])
                    latitude = float(pos.split(' ')[1])
                    return Point(latitude, longitude)
        # <geo:Point xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
        #   <geo:lat>38.3728</geo:lat>
        #   <geo:long>15.7213</geo:long>
        # </geo:Point>
        point = self._attribute(['geo:Point'])
        if point:
            latitude = float(point.get('geo:lat'))
            longitude = float(point.get('geo:lon'))
            return Point(latitude, longitude)
        # <geo:long>119.948006</geo:long>
        # <geo:lat>-23.126413</geo:lat>
        long = self._attribute(['geo:long'])
        lat = self._attribute(['geo:lat'])
        if long and lat:
            longitude = float(long)
            latitude = float(lat)
            return Point(latitude, longitude)
        # None of the above
        return None
