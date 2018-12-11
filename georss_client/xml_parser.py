"""
RSS XML Parser with GeoRSS support.
"""
import dateparser as dateparser
import datetime
import logging
import xmltodict
from typing import Optional

from georss_client.consts import XML_TAG_GEORSS_POLYGON, XML_TAG_GEO_LONG, \
    XML_TAG_GEO_LAT, XML_TAG_GEO_POINT, XML_TAG_GML_POS, XML_TAG_GML_POINT, \
    XML_TAG_GEORSS_WHERE, XML_TAG_GEORSS_POINT, XML_ATTR_TERM, \
    XML_TAG_CATEGORY, XML_TAG_SOURCE, XML_ATTR_TEXT, XML_TAG_ID, \
    XML_TAG_GUID, XML_TAG_ENTRY, XML_TAG_ITEM, XML_TAG_NAME, XML_TAG_AUTHOR, \
    XML_TAG_LAST_BUILD_DATE, XML_TAG_TTL, XML_TAG_LANGUAGE, \
    XML_TAG_GENERATOR, XML_TAG_COPYRIGHT, XML_TAG_DC_DATE, XML_TAG_PUB_DATE, \
    XML_TAG_PUBLISHED, XML_TAG_UPDATED, XML_TAG_LINK, XML_TAG_CONTENT, \
    XML_TAG_SUMMARY, XML_TAG_DESCRIPTION, XML_TAG_TITLE, XML_TAG_FEED, \
    XML_TAG_CHANNEL, XML_TAG_RSS, XML_TAG_GML_POLYGON, XML_TAG_GML_EXTERIOR, \
    XML_TAG_GML_LINEAR_RING, XML_TAG_GML_POS_LIST, XML_TAG_MANAGING_EDITOR, \
    XML_TAG_CONTRIBUTOR, XML_TAG_RIGHTS

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAMESPACES = {
    'http://www.w3.org/2005/Atom': None,
    'http://purl.org/dc/elements/1.1/': 'dc',
    'http://www.georss.org/georss': 'georss',
    'http://www.w3.org/2003/01/geo/wgs84_pos#': 'geo',
    'http://www.opengis.net/gml': 'gml',
    'http://www.gdacs.org/': 'gdacs',
}

KEYS_DATE = [XML_TAG_DC_DATE, XML_TAG_LAST_BUILD_DATE, XML_TAG_PUB_DATE,
             XML_TAG_PUBLISHED, XML_TAG_UPDATED]
KEYS_INT = [XML_TAG_TTL]


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
                    if key in KEYS_DATE and value:
                        return key, dateparser.parse(value)
                    if key in KEYS_INT and value:
                        return key, int(value)
                except (ValueError, TypeError) as error:
                    _LOGGER.warning("Unable to process (%s/%s): %s",
                                    key, value, error)
                return key, value

            parsed_dict = xmltodict.parse(
                xml, process_namespaces=True, namespaces=self._namespaces,
                postprocessor=postprocessor)

            if XML_TAG_RSS in parsed_dict:
                rss = parsed_dict.get(XML_TAG_RSS)
                if XML_TAG_CHANNEL in rss:
                    channel = rss.get(XML_TAG_CHANNEL)
                    return Feed(channel)
            if XML_TAG_FEED in parsed_dict:
                feed = parsed_dict.get(XML_TAG_FEED)
                return Feed(feed)

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
        return '<{}(latitude={}, longitude={})>'.format(
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

    def __repr__(self):
        """Return string representation of this polygon."""
        return '<{}(centroid={})>'.format(
            self.__class__.__name__, self.centroid)

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

    @staticmethod
    def _key_exists(obj, keys):
        key = keys.pop(0)
        if key in obj:
            return FeedDictSource._key_exists(obj[key], keys) if keys \
                else obj[key]

    @property
    def title(self) -> Optional[str]:
        """Return the title of this feed or feed item."""
        return self._attribute([XML_TAG_TITLE])

    @property
    def description(self) -> Optional[str]:
        """Return the description of this feed or feed item."""
        return self._attribute([XML_TAG_DESCRIPTION,
                                XML_TAG_SUMMARY,
                                XML_TAG_CONTENT])

    @property
    def summary(self) -> Optional[str]:
        """Return the summary of this feed or feed item."""
        return self.description

    @property
    def content(self) -> Optional[str]:
        """Return the content of this feed or feed item."""
        return self.description

    @property
    def link(self) -> Optional[str]:
        """Return the link of this feed or feed item."""
        return self._attribute([XML_TAG_LINK])

    @property
    def published_date(self) -> Optional[datetime.datetime]:
        """Return the published date of this feed or feed item."""
        return self._attribute([XML_TAG_PUB_DATE,
                                XML_TAG_PUBLISHED,
                                XML_TAG_DC_DATE])

    @property
    def pub_date(self) -> Optional[datetime.datetime]:
        """Return the published date of this feed or feed item."""
        return self.published_date

    @property
    def updated_date(self) -> Optional[datetime.datetime]:
        """Return the updated date of this feed or feed item."""
        return self._attribute([XML_TAG_LAST_BUILD_DATE, XML_TAG_UPDATED])

    @property
    def last_build_date(self) -> Optional[datetime.datetime]:
        """Return the last build date of this feed."""
        return self.updated_date

    @property
    def author(self) -> Optional[str]:
        """Return the author of this feed."""
        # <managingEditor>jrc-ems@ec.europa.eu</managingEditor>
        managing_editor = self._attribute([XML_TAG_MANAGING_EDITOR])
        if managing_editor:
            return managing_editor
        # <author>
        #   <name>Istituto Nazionale di Geofisica e Vulcanologia</name>
        #   <uri>http://www.ingv.it</uri>
        # </author>
        author = self._attribute([XML_TAG_AUTHOR, XML_TAG_CONTRIBUTOR])
        if author:
            name = author.get(XML_TAG_NAME, None)
            return name
        return None

    @property
    def contributor(self) -> Optional[str]:
        """Return the contributor of this feed."""
        return self.author

    @property
    def managing_editor(self) -> Optional[str]:
        """Return the managing editor of this feed."""
        return self.author

    def get_additional_attribute(self, name):
        """Get an additional attribute not provided as property."""
        return self._attribute([name])


class Feed(FeedDictSource):
    """Represents a feed."""

    @property
    def copyright(self) -> Optional[str]:
        """Return the copyright of this feed."""
        return self._attribute([XML_TAG_COPYRIGHT, XML_TAG_RIGHTS])

    @property
    def rights(self) -> Optional[str]:
        """Return the rights of this feed."""
        return self.copyright

    @property
    def generator(self) -> Optional[str]:
        """Return the generator of this feed."""
        return self._attribute([XML_TAG_GENERATOR])

    @property
    def language(self) -> Optional[str]:
        """Return the language of this feed."""
        return self._attribute([XML_TAG_LANGUAGE])

    @property
    def ttl(self) -> Optional[int]:
        """Return the ttl of this feed."""
        return self._attribute([XML_TAG_TTL])

    @property
    def entries(self):
        """Return the entries of this feed."""
        items = self._attribute([XML_TAG_ITEM, XML_TAG_ENTRY])
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
        guid = self._attribute([XML_TAG_GUID, XML_TAG_ID])
        if guid and isinstance(guid, dict) and XML_ATTR_TEXT in guid:
            # <guid isPermaLink="false">
            #   1234
            # </guid>
            guid = guid.get(XML_ATTR_TEXT)
        return guid

    @property
    def id(self) -> Optional[str]:
        """Return the id of this feed item."""
        return self.guid

    @property
    def source(self) -> Optional[str]:
        """Return the source of this feed item."""
        return self._attribute([XML_TAG_SOURCE])

    @property
    def category(self) -> Optional[str]:
        """Return the category of this feed item."""
        category = self._attribute([XML_TAG_CATEGORY])
        if category and XML_ATTR_TERM in category:
            # <category term="Category 1"/>
            category = category.get(XML_ATTR_TERM)
        return category

    @property
    def geometry(self) -> Optional[Geometry]:
        """Return the geometry of this feed item."""
        # <georss:point>-0.5 119.8</georss:point>
        point = self._attribute([XML_TAG_GEORSS_POINT])
        if point:
            latitude = float(point.split(' ')[0])
            longitude = float(point.split(' ')[1])
            return Point(latitude, longitude)
        # GML
        where = self._attribute([XML_TAG_GEORSS_WHERE])
        if where:
            # Point:
            # <georss:where>
            #   <gml:Point>
            #     <gml:pos>44.11 -66.23</gml:pos>
            #   </gml:Point>
            # </georss:where>
            pos = self._key_exists(where, [XML_TAG_GML_POINT, XML_TAG_GML_POS])
            if pos:
                latitude = float(pos.split(' ')[0])
                longitude = float(pos.split(' ')[1])
                return Point(latitude, longitude)
            # Polygon:
            # <georss:where>
            #   <gml:Polygon>
            #     <gml:exterior>
            #       <gml:LinearRing>
            #         <gml:posList>
            #           -71.106216 42.366661
            #           -71.105576 42.367104
            #           -71.104378 42.367134
            #           -71.103729 42.366249
            #           -71.098793 42.363331
            #           -71.101028 42.362541
            #           -71.106865 42.366123
            #           -71.106216 42.366661
            #         </gml:posList>
            #       </gml:LinearRing>
            #     </gml:exterior>
            #   </gml:Polygon>
            # </georss:where>
            pos_list = self._key_exists(where, [XML_TAG_GML_POLYGON,
                                                XML_TAG_GML_EXTERIOR,
                                                XML_TAG_GML_LINEAR_RING,
                                                XML_TAG_GML_POS_LIST])
            if pos_list:
                return self._create_polygon(pos_list)
        # <geo:Point xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
        #   <geo:lat>38.3728</geo:lat>
        #   <geo:long>15.7213</geo:long>
        # </geo:Point>
        point = self._attribute([XML_TAG_GEO_POINT])
        if point:
            lat = point.get(XML_TAG_GEO_LAT)
            long = point.get(XML_TAG_GEO_LONG)
            if long and lat:
                longitude = float(long)
                latitude = float(lat)
                return Point(latitude, longitude)
        # <geo:long>119.948006</geo:long>
        # <geo:lat>-23.126413</geo:lat>
        lat = self._attribute([XML_TAG_GEO_LAT])
        long = self._attribute([XML_TAG_GEO_LONG])
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
        polygon = self._attribute([XML_TAG_GEORSS_POLYGON])
        if polygon:
            # For now, only supporting the first polygon.
            if isinstance(polygon, list):
                polygon = polygon[0]
            return self._create_polygon(polygon)
        # None of the above
        return None

    @staticmethod
    def _create_polygon(coordinates):
        """Create a polygon from the provided coordinates."""
        if coordinates:
            # The coordinates must be in latitude-longitude order and
            # whitespace separated.
            coordinate_values = coordinates.split()
            points = []
            for i in range(0, len(coordinate_values), 2):
                latitude = float(coordinate_values[i])
                longitude = float(coordinate_values[i + 1])
                points.append(Point(latitude, longitude))
            return Polygon(points)
        return None
