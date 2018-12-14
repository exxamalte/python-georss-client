"""
GeoRSS feed models.
"""
import datetime
import logging
from typing import Optional

from georss_client.consts import XML_TAG_GEORSS_POLYGON, XML_TAG_GEO_LONG, \
    XML_TAG_GEO_LAT, XML_TAG_GEO_POINT, XML_TAG_GML_POS, XML_TAG_GML_POINT, \
    XML_TAG_GEORSS_WHERE, XML_TAG_GEORSS_POINT, XML_ATTR_TERM, \
    XML_TAG_CATEGORY, XML_TAG_SOURCE, XML_CDATA, XML_TAG_ID, \
    XML_TAG_GUID, XML_TAG_ENTRY, XML_TAG_ITEM, XML_TAG_NAME, XML_TAG_AUTHOR, \
    XML_TAG_LAST_BUILD_DATE, XML_TAG_TTL, XML_TAG_LANGUAGE, \
    XML_TAG_GENERATOR, XML_TAG_COPYRIGHT, XML_TAG_DC_DATE, XML_TAG_PUB_DATE, \
    XML_TAG_PUBLISHED, XML_TAG_UPDATED, XML_TAG_LINK, XML_TAG_CONTENT, \
    XML_TAG_SUMMARY, XML_TAG_DESCRIPTION, XML_TAG_TITLE, XML_TAG_GML_POLYGON, XML_TAG_GML_EXTERIOR, \
    XML_TAG_GML_LINEAR_RING, XML_TAG_GML_POS_LIST, XML_TAG_MANAGING_EDITOR, \
    XML_TAG_CONTRIBUTOR, XML_TAG_RIGHTS, XML_ATTR_HREF, XML_TAG_IMAGE, \
    XML_TAG_URL, XML_TAG_HEIGHT, XML_TAG_WIDTH, XML_TAG_DOCS, XML_TAG_SUBTITLE
from georss_client.xml_parser.geometry import Geometry, Point, Polygon

_LOGGER = logging.getLogger(__name__)


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

    def _attribute_with_text(self, names):
        """Get an attribute with text from this feed or feed item."""
        value = self._attribute(names)
        if value and isinstance(value, dict) and XML_CDATA in value:
            # <tag attr="/some.uri">Value</tag>
            value = value.get(XML_CDATA)
        return value

    @staticmethod
    def _attribute_in_structure(obj, keys):
        """Return the attribute found under the chain of keys."""
        key = keys.pop(0)
        if key in obj:
            return FeedDictSource._attribute_in_structure(
                obj[key], keys) if keys else obj[key]

    @property
    def title(self) -> Optional[str]:
        """Return the title of this feed or feed item."""
        return self._attribute_with_text([XML_TAG_TITLE])

    @property
    def description(self) -> Optional[str]:
        """Return the description of this feed or feed item."""
        return self._attribute_with_text([XML_TAG_DESCRIPTION,
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
        link = self._attribute([XML_TAG_LINK])
        if link and XML_ATTR_HREF in link:
            link = link.get(XML_ATTR_HREF)
        return link

    def get_additional_attribute(self, name):
        """Get an additional attribute not provided as property."""
        return self._attribute([name])


class FeedOrFeedItem(FeedDictSource):
    """Represents the common base of feed and its items."""

    @property
    def category(self) -> Optional[list]:
        """Return the categories of this feed item."""
        category = self._attribute([XML_TAG_CATEGORY])
        if category:
            if isinstance(category, str) or isinstance(category, dict):
                # If it's a string or a dict, wrap in list.
                category = [category]
            result = []
            for item in category:
                if XML_ATTR_TERM in item:
                    # <category term="Category 1"/>
                    item = item.get(XML_ATTR_TERM)
                result.append(item)
            return result
        return None

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


class Feed(FeedOrFeedItem):
    """Represents a feed."""

    @property
    def subtitle(self) -> Optional[str]:
        """Return the subtitle of this feed."""
        return self._attribute_with_text([XML_TAG_SUBTITLE])

    @property
    def copyright(self) -> Optional[str]:
        """Return the copyright of this feed."""
        return self._attribute_with_text([XML_TAG_COPYRIGHT, XML_TAG_RIGHTS])

    @property
    def rights(self) -> Optional[str]:
        """Return the rights of this feed."""
        return self.copyright

    @property
    def generator(self) -> Optional[str]:
        """Return the generator of this feed."""
        return self._attribute_with_text([XML_TAG_GENERATOR])

    @property
    def language(self) -> Optional[str]:
        """Return the language of this feed."""
        return self._attribute([XML_TAG_LANGUAGE])

    @property
    def docs(self) -> Optional[str]:
        """Return the docs URL of this feed."""
        return self._attribute_with_text([XML_TAG_DOCS])

    @property
    def ttl(self) -> Optional[int]:
        """Return the ttl of this feed."""
        return self._attribute([XML_TAG_TTL])

    @property
    def image(self):
        """Return the image of this feed."""
        image = self._attribute([XML_TAG_IMAGE])
        if image:
            return FeedImage(image)
        return None

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


class FeedImage(FeedDictSource):
    """Represents a feed image."""

    @property
    def url(self) -> Optional[str]:
        """Return the url of this feed image."""
        return self._attribute([XML_TAG_URL])

    @property
    def height(self) -> Optional[int]:
        """Return the height of this feed image."""
        return self._attribute([XML_TAG_HEIGHT])

    @property
    def width(self) -> Optional[int]:
        """Return the width of this feed image."""
        return self._attribute([XML_TAG_WIDTH])


class FeedItem(FeedOrFeedItem):
    """Represents a feed item."""

    def __repr__(self):
        """Return string representation of this feed item."""
        return '<{}({})>'.format(
            self.__class__.__name__, self.guid)

    @property
    def guid(self) -> Optional[str]:
        """Return the guid of this feed item."""
        return self._attribute_with_text([XML_TAG_GUID, XML_TAG_ID])

    @property
    def id(self) -> Optional[str]:
        """Return the id of this feed item."""
        return self.guid

    @property
    def source(self) -> Optional[str]:
        """Return the source of this feed item."""
        return self._attribute([XML_TAG_SOURCE])

    @property
    def geometry(self) -> Optional[Geometry]:
        """Return the geometry of this feed item."""
        # <georss:point>-0.5 119.8</georss:point>
        point = self._attribute([XML_TAG_GEORSS_POINT])
        if point:
            return Point(point[0], point[1])
        # GML
        where = self._attribute([XML_TAG_GEORSS_WHERE])
        if where:
            # Point:
            # <georss:where>
            #   <gml:Point>
            #     <gml:pos>44.11 -66.23</gml:pos>
            #   </gml:Point>
            # </georss:where>
            pos = self._attribute_in_structure(
                where, [XML_TAG_GML_POINT, XML_TAG_GML_POS])
            if pos:
                return Point(pos[0], pos[1])
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
            pos_list = self._attribute_in_structure(
                where, [XML_TAG_GML_POLYGON, XML_TAG_GML_EXTERIOR,
                        XML_TAG_GML_LINEAR_RING, XML_TAG_GML_POS_LIST])
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
                return Point(lat, long)
        # <geo:long>119.948006</geo:long>
        # <geo:lat>-23.126413</geo:lat>
        lat = self._attribute([XML_TAG_GEO_LAT])
        long = self._attribute([XML_TAG_GEO_LONG])
        if long and lat:
            return Point(lat, long)
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
            if isinstance(polygon, list) and isinstance(polygon[0], list):
                polygon = polygon[0]
            return self._create_polygon(polygon)
        # None of the above
        return None

    @staticmethod
    def _create_polygon(coordinates):
        """Create a polygon from the provided coordinates."""
        if coordinates:
            if len(coordinates) % 2 != 0:
                # Not even number of coordinates - chop last entry.
                coordinates = coordinates[0:len(coordinates)-1]
            points = []
            for i in range(0, len(coordinates), 2):
                points.append(Point(coordinates[i], coordinates[i + 1]))
            return Polygon(points)
        return None
