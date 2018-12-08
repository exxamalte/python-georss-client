"""
RSS XML Parser with GeoRSS support.
"""
import dateparser as dateparser
import datetime
import logging
import xmltodict
from typing import Optional

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAMESPACES = {
    'http://www.w3.org/2005/Atom': None,
    'http://purl.org/dc/elements/1.1/': 'dc',
    'http://www.georss.org/georss': 'georss',
    'http://www.w3.org/2003/01/geo/wgs84_pos#': 'geo',
    'http://www.opengis.net/gml': 'gml',
    'http://www.gdacs.org/': 'gdacs',
}

KEYS_DATE = ['dc:date', 'lastBuildDate', 'pubDate', 'published', 'updated']
KEYS_INT = ['ttl']


class XmlParser:
    """Built-in XML parser."""

    def __init__(self, additional_namespaces=None):
        """Initialise the XML parser."""
        self._namespaces = DEFAULT_NAMESPACES
        if additional_namespaces:
            self._namespaces.update(additional_namespaces)

    def parse(self, xml):
        """Parse the provided xml."""
        if xml:

            def postprocessor(path, key, value):
                """Conduct type conversion for selected keys."""
                try:
                    if key in KEYS_DATE:
                        return key, dateparser.parse(value)
                    if key in KEYS_INT:
                        return key, int(value)
                except (ValueError, TypeError) as error:
                    _LOGGER.warning("Unable to process (%s/%s): %s",
                                    key, value, error)
                return key, value

            parsed_dict = xmltodict.parse(
                xml, process_namespaces=True, namespaces=self._namespaces,
                postprocessor=postprocessor)

            data = parsed_dict
            if 'rss' in parsed_dict:
                rss = parsed_dict.get('rss')
                if 'channel' in rss:
                    channel = rss.get('channel')
                    data = channel
            if 'feed' in parsed_dict:
                feed = parsed_dict.get('feed')
                data = feed

            return Feed(data)
        return None


class Geometry:
    """Represents a geometry."""


class Point(Geometry):
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
        """Return the latitude of this point."""
        return self._latitude

    @property
    def longitude(self) -> Optional[float]:
        """Return the longitude of this point."""
        return self._longitude


class Polygon(Geometry):
    """Represents a polygon."""

    def __init__(self, points):
        """Initialise polygon."""
        self._points = points

    @property
    def points(self) -> Optional[list]:
        """Return the points of this polygon."""
        return self._points

    @property
    def centroid(self) -> Point:
        """Find the polygon's centroid as a best approximation."""
        longitudes_list = [point.longitude for point in self.points]
        latitudes_list = [point.latitude for point in self.points]
        number_of_points = len(self.points)
        longitude = sum(longitudes_list) / number_of_points
        latitude = sum(latitudes_list) / number_of_points
        return Point(latitude, longitude)


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
        """Get an attribute from this feed or feed item."""
        if self._source and names:
            # Try each name, and return the first value that is not None.
            for name in names:
                value = self._source.get(name, None)
                if value:
                    return value
        return None

    @property
    def title(self) -> Optional[str]:
        """Return the title of this feed or feed item."""
        return self._attribute(['title'])

    @property
    def description(self) -> Optional[str]:
        """Return the description of this feed or feed item."""
        return self._attribute(['description', 'summary', 'content'])

    @property
    def link(self) -> Optional[str]:
        """Return the link of this feed or feed item."""
        return self._attribute(['link'])

    @property
    def published_date(self) -> Optional[datetime.datetime]:
        """Return the published date of this feed or feed item."""
        return self._attribute(['pubDate', 'published', 'dc:date'])

    @property
    def updated_date(self) -> Optional[datetime.datetime]:
        """Return the updated date of this feed or feed item."""
        return self._attribute(['updated'])

    def get_additional_attribute(self, name):
        """Get an additional attribute not provided as property."""
        return self._attribute([name])


class Feed(FeedDictSource):
    """Represents a feed."""

    @property
    def author(self) -> Optional[str]:
        """Return the author of this feed."""
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
        """Return the copyright of this feed."""
        return self._attribute(['copyright'])

    @property
    def generator(self) -> Optional[str]:
        """Return the generator of this feed."""
        return self._attribute(['generator'])

    @property
    def language(self) -> Optional[str]:
        """Return the language of this feed."""
        return self._attribute(['language'])

    @property
    def last_build_date(self) -> Optional[datetime.datetime]:
        """Return the last build date of this feed."""
        return self._attribute(['lastBuildDate'])

    @property
    def ttl(self) -> Optional[int]:
        """Return the ttl of this feed."""
        return self._attribute(['ttl'])

    @property
    def entries(self):
        """Return the entries of this feed."""
        items = self._attribute(['item', 'entry'])
        entries = []
        if items and isinstance(items, list):
            for item in items:
                entries.append(FeedItem(item))
        else:
            # A single item in the feed is not represented as an array.
            entries.append(FeedItem(items))
        return entries


class FeedItem(FeedDictSource):
    """Represents a feed item."""

    def __repr__(self):
        """Return string representation of this feed item."""
        return '<{}({})>'.format(
            self.__class__.__name__, self.guid)

    @property
    def guid(self) -> Optional[str]:
        """Return the guid of this feed item."""
        guid = self._attribute(['guid', 'id'])
        if guid and isinstance(guid, dict) and '#text' in guid:
            # <guid isPermaLink="false">
            #   1234
            # </guid>
            guid = guid.get('#text')
        return guid

    @property
    def source(self) -> Optional[str]:
        """Return the source of this feed item."""
        return self._attribute(['source'])

    @property
    def category(self) -> Optional[str]:
        """Return the category of this feed item."""
        category = self._attribute(['category'])
        if category and '@term' in category:
            # <category term="Category 1"/>
            category = category.get('@term')
        return category

    @property
    def geometry(self) -> Optional[Geometry]:
        """Return the geometry of this feed item."""
        # <georss:point>-0.5 119.8</georss:point>
        point = self._attribute(['georss:point'])
        if point:
            latitude = float(point.split(' ')[0])
            longitude = float(point.split(' ')[1])
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
                pos = point.get('gml:pos')
                if pos:
                    latitude = float(pos.split(' ')[0])
                    longitude = float(pos.split(' ')[1])
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
        # <georss:polygon>
        #   -34.937663524 148.597260613
        #   -34.9377026399999 148.597169138
        #   -34.9377002169999 148.59708737
        #   -34.9376945989999 148.59705595
        #   -34.9376863529999 148.596955098
        #   -34.937663524 148.597260613
        # </georss:polygon>
        polygon = self._attribute(['georss:polygon'])
        if polygon:
            # For now, only supporting the first polygon.
            if isinstance(polygon, list):
                polygon = polygon[0]
            # Extract coordinate pairs.
            coordinate_values = polygon.split(' ')
            points = []
            for i in range(0, len(coordinate_values), 2):
                latitude = float(coordinate_values[i])
                longitude = float(coordinate_values[i+1])
                points.append(Point(latitude, longitude))
            return Polygon(points)
        # None of the above
        return None
