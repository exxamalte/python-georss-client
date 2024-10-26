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

    def __hash__(self) -> int:
        """Return unique hash of this geometry."""
        return hash((self.latitude, self.longitude))

    def __eq__(self, other: object) -> bool:
        """Return if this object is equal to other object."""
        return (
            self.__class__ == other.__class__
            and self.latitude == other.latitude
            and self.longitude == other.longitude
        )

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

    def __init__(self, points: list[Point]):
        """Initialise polygon."""
        self._points: list[Point] = points

    def __repr__(self):
        """Return string representation of this polygon."""
        return f"<{self.__class__.__name__}(centroid={self.centroid})>"

    def __hash__(self) -> int:
        """Return unique hash of this geometry."""
        return hash(self.points)

    def __eq__(self, other: object) -> bool:
        """Return if this object is equal to other object."""
        return self.__class__ == other.__class__ and self.points == other.points

    @property
    def points(self) -> list[Point] | None:
        """Return the points of this polygon."""
        return self._points

    @property
    def centroid(self) -> Point:
        """Find the polygon's centroid as a best approximation."""
        longitudes_list: list[float] = [point.longitude for point in self.points]
        latitudes_list: list[float] = [point.latitude for point in self.points]
        number_of_points: int = len(self.points)
        longitude: float = sum(longitudes_list) / number_of_points
        latitude: float = sum(latitudes_list) / number_of_points
        return Point(latitude, longitude)
