"""Tests for georss distance helper."""

import unittest
from unittest.mock import MagicMock

import pytest

from georss_client.geo_rss_distance_helper import GeoRssDistanceHelper
from georss_client.xml_parser.geometry import Point, Polygon


class TestGeoRssDistanceHelper(unittest.TestCase):
    """Tests for the GeoJSON distance helper."""

    def test_extract_coordinates_from_point(self):
        """Test extracting coordinates from point."""
        mock_point = Point(-30.0, 151.0)
        latitude, longitude = GeoRssDistanceHelper.extract_coordinates(mock_point)
        assert latitude == -30.0
        assert longitude == 151.0

    def test_extract_coordinates_from_polygon(self):
        """Test extracting coordinates from polygon."""
        mock_polygon = Polygon(
            [
                Point(-30.0, 151.0),
                Point(-30.0, 151.5),
                Point(-30.5, 151.5),
                Point(-30.5, 151.0),
                Point(-30.0, 151.0),
            ]
        )
        latitude, longitude = GeoRssDistanceHelper.extract_coordinates(mock_polygon)
        assert latitude == pytest.approx(-30.2, 0.1)
        assert longitude == pytest.approx(151.2, 0.1)

    def test_extract_coordinates_from_unsupported_geometry(self):
        """Test extracting coordinates from unsupported geometry."""
        mock_unsupported_geometry = MagicMock()
        latitude, longitude = GeoRssDistanceHelper.extract_coordinates(
            mock_unsupported_geometry
        )
        assert latitude is None
        assert longitude is None

    def test_distance_to_point(self):
        """Test calculating distance to point."""
        home_coordinates = [-31.0, 150.0]
        mock_point = Point(-30.0, 151.0)
        distance = GeoRssDistanceHelper.distance_to_geometry(
            home_coordinates, mock_point
        )
        assert distance == pytest.approx(146.8, 0.1)

    def test_distance_to_polygon(self):
        """Test calculating distance to point."""
        home_coordinates = [-31.0, 150.0]
        mock_polygon = Polygon(
            [
                Point(-30.0, 151.0),
                Point(-30.0, 151.5),
                Point(-30.5, 151.5),
                Point(-30.5, 151.0),
                Point(-30.0, 151.0),
            ]
        )
        distance = GeoRssDistanceHelper.distance_to_geometry(
            home_coordinates, mock_polygon
        )
        assert distance == pytest.approx(110.6, 0.1)

    def test_distance_to_unsupported_geometry(self):
        """Test calculating distance to unsupported geometry."""
        home_coordinates = [-31.0, 150.0]
        mock_unsupported_geometry = MagicMock()
        distance = GeoRssDistanceHelper.distance_to_geometry(
            home_coordinates, mock_unsupported_geometry
        )
        assert distance == float("inf")
