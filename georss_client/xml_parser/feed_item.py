"""GeoRSS feed item."""

from __future__ import annotations

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
        return f"<{self.__class__.__name__}({self.guid})>"

    @property
    def guid(self) -> str | None:
        """Return the guid of this feed item."""
        return self._attribute_with_text([XML_TAG_GUID, XML_TAG_ID])

    @property
    def id(self) -> str | None:
        """Return the id of this feed item."""
        return self.guid

    @property
    def source(self) -> str | None:
        """Return the source of this feed item."""
        return self._attribute([XML_TAG_SOURCE])

    @property
    def geometries(self) -> list[Geometry] | None:
        """Return all geometries of this feed item."""
        geometries = []
        for entry in [
            self._geometry_georss_point(),
            self._geometry_georss_where(),
            self._geometry_geo_point(),
            self._geometry_geo_long_lat(),
            self._geometry_georss_polygon(),
        ]:
            if entry:
                geometries.extend(entry)
        # Filter out any duplicates.
        unique_geometries = []
        for i in geometries:
            if i not in unique_geometries:
                unique_geometries.append(i)
        return unique_geometries

    def _geometry_georss_point(self) -> list[Point] | None:
        """Check for georss:point tag."""
        # <georss:point>-0.5 119.8</georss:point>
        point = self._attribute([XML_TAG_GEORSS_POINT])
        if point:
            if isinstance(point, tuple):
                return FeedItem._create_georss_point_single(point)
            return FeedItem._create_georss_point_multiple(point)
        return None

    @staticmethod
    def _create_georss_point_single(point: tuple) -> list[Point]:
        """Create single point from provided coordinates."""
        return [Point(point[0], point[1])]

    @staticmethod
    def _create_georss_point_multiple(point: list) -> list[Point]:
        """Create multiple points from provided coordinates."""
        return [Point(entry[0], entry[1]) for entry in point]

    def _geometry_georss_where(self) -> list[Geometry] | None:
        """Check for georss:where tag."""
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
                return [Point(pos[0], pos[1])]
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
        return None

    def _geometry_geo_point(self) -> list[Point] | None:
        """Check for geo:Point tag."""
        # <geo:Point xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
        #   <geo:lat>38.3728</geo:lat>
        #   <geo:long>15.7213</geo:long>
        # </geo:Point>
        point = self._attribute([XML_TAG_GEO_POINT])
        if point:
            lat = point.get(XML_TAG_GEO_LAT)
            long = point.get(XML_TAG_GEO_LONG)
            if long and lat:
                return [Point(lat, long)]
        return None

    def _geometry_geo_long_lat(self) -> list[Point] | None:
        """Check for geo:long and geo:lat tags."""
        # <geo:long>119.948006</geo:long>
        # <geo:lat>-23.126413</geo:lat>
        lat = self._attribute([XML_TAG_GEO_LAT])
        long = self._attribute([XML_TAG_GEO_LONG])
        if long and lat:
            return [Point(lat, long)]
        return None

    def _geometry_georss_polygon(self) -> list[Polygon] | None:
        """Check for georss:polygon tag."""
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
            return self._create_polygon(polygon)
        return None

    @staticmethod
    def _create_polygon(polygon_data) -> list[Polygon] | None:
        """Create a polygon from the provided coordinates."""
        if polygon_data:
            # Either tuple or an array of tuples.
            if isinstance(polygon_data, tuple):
                return FeedItem._create_polygon_single(polygon_data)
            return FeedItem._create_polygon_multiple(polygon_data)
        return None

    @staticmethod
    def _create_polygon_single(polygon_data: tuple) -> list[Polygon]:
        """Create polygon from provided tuple of coordinates."""
        if len(polygon_data) % 2 != 0:
            # Not even number of coordinates - chop last entry.
            polygon_data = polygon_data[0 : len(polygon_data) - 1]
        return [
            Polygon(
                [
                    Point(polygon_data[i], polygon_data[i + 1])
                    for i in range(0, len(polygon_data), 2)
                ]
            )
        ]

    @staticmethod
    def _create_polygon_multiple(polygon_data: list) -> list[Polygon]:
        """Create polygon from provided list of coordinates."""
        polygons = []
        for entry in polygon_data:
            polygons.extend(FeedItem._create_polygon(entry))
        return polygons

    @property
    def geometry(self) -> Geometry | None:
        """Return the first geometry of this feed item for backwards compatibility reasons."""
        return self.geometries[0] if self.geometries else None
