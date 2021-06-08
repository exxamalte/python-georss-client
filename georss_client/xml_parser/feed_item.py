"""
GeoRSS feed item.
"""
from typing import Optional

from georss_client.consts import (
    XML_TAG_GEO_LAT,
    XML_TAG_GEO_LONG,
    XML_TAG_GEO_POINT,
    XML_TAG_GEORSS_POINT,
    XML_TAG_GEORSS_POLYGON,
    XML_TAG_GEORSS_WHERE,
    XML_TAG_GML_EXTERIOR,
    XML_TAG_GML_LINEAR_RING,
    XML_TAG_GML_POINT,
    XML_TAG_GML_POLYGON,
    XML_TAG_GML_POS,
    XML_TAG_GML_POS_LIST,
    XML_TAG_GUID,
    XML_TAG_ID,
    XML_TAG_SOURCE,
)
from georss_client.xml_parser.feed_or_feed_item import FeedOrFeedItem
from georss_client.xml_parser.geometry import Geometry, Point, Polygon


class FeedItem(FeedOrFeedItem):
    """Represents a feed item."""

    def __repr__(self):
        """Return string representation of this feed item."""
        return "<{}({})>".format(self.__class__.__name__, self.guid)

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
                where, [XML_TAG_GML_POINT, XML_TAG_GML_POS]
            )
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
                where,
                [
                    XML_TAG_GML_POLYGON,
                    XML_TAG_GML_EXTERIOR,
                    XML_TAG_GML_LINEAR_RING,
                    XML_TAG_GML_POS_LIST,
                ],
            )
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
                coordinates = coordinates[0 : len(coordinates) - 1]
            points = []
            for i in range(0, len(coordinates), 2):
                points.append(Point(coordinates[i], coordinates[i + 1]))
            return Polygon(points)
        return None
