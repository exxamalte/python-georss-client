"""
GeoRSS Distance Helper.
"""
import logging

from haversine import haversine

from georss_client.xml_parser.geometry import Point, Polygon

_LOGGER = logging.getLogger(__name__)


class GeoRssDistanceHelper:
    """Helper to calculate distances between GeoRSS geometries."""

    @staticmethod
    def extract_coordinates(geometry):
        """Extract the best coordinates from the feature for display."""
        latitude = longitude = None
        if isinstance(geometry, Point):
            # Just extract latitude and longitude directly.
            latitude, longitude = geometry.latitude, geometry.longitude
        elif isinstance(geometry, Polygon):
            centroid = geometry.centroid
            latitude, longitude = centroid.latitude, centroid.longitude
            _LOGGER.debug("Centroid of %s is %s", geometry, (latitude, longitude))
        else:
            _LOGGER.debug("Not implemented: %s", type(geometry))
        return latitude, longitude

    @staticmethod
    def distance_to_geometry(home_coordinates, geometry):
        """Calculate the distance between home coordinates and geometry."""
        distance = float("inf")
        if isinstance(geometry, Point):
            distance = GeoRssDistanceHelper._distance_to_point(
                home_coordinates, geometry
            )
        elif isinstance(geometry, Polygon):
            distance = GeoRssDistanceHelper._distance_to_polygon(
                home_coordinates, geometry
            )
        else:
            _LOGGER.debug("Not implemented: %s", type(geometry))
        return distance

    @staticmethod
    def _distance_to_point(home_coordinates, point):
        """Calculate the distance between home coordinates and the point."""
        # Swap coordinates to match: (latitude, longitude).
        return GeoRssDistanceHelper._distance_to_coordinates(
            home_coordinates, (point.latitude, point.longitude)
        )

    @staticmethod
    def _distance_to_polygon(home_coordinates, polygon):
        """Calculate the distance between home coordinates and the polygon."""
        distance = float("inf")
        # Calculate distance from polygon by calculating the distance
        # to each point of the polygon but not to each edge of the
        # polygon; should be good enough
        for point in polygon.points:
            distance = min(
                distance,
                GeoRssDistanceHelper._distance_to_coordinates(
                    home_coordinates, (point.latitude, point.longitude)
                ),
            )
        return distance

    @staticmethod
    def _distance_to_coordinates(home_coordinates, coordinates):
        """Calculate the distance between home coordinates and the
        coordinates."""
        # Expecting coordinates in format: (latitude, longitude).
        return haversine(coordinates, home_coordinates)
