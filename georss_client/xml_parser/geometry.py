"""Geometry models."""

from __future__ import annotations


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
        return f"<{self.__class__.__name__}(latitude={self.latitude}, longitude={self.longitude})>"

    @property
    def latitude(self) -> float | None:
        """Return the latitude of this point."""
        return self._latitude

    @property
    def longitude(self) -> float | None:
        """Return the longitude of this point."""
        return self._longitude


class Polygon(Geometry):
    """Represents a polygon."""

    def __init__(self, points):
        """Initialise polygon."""
        self._points = points

    def __repr__(self):
        """Return string representation of this polygon."""
        return f"<{self.__class__.__name__}(centroid={self.centroid})>"

    @property
    def points(self) -> list | None:
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
