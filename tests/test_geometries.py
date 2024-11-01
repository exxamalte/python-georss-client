"""Test geometries."""

from georss_client.xml_parser.geometry import Point, Polygon


def test_point():
    """Test point."""
    point = Point(-37.1234, 149.2345)
    assert point.latitude == -37.1234
    assert point.longitude == 149.2345
    assert repr(point) == "<Point(latitude=-37.1234, longitude=149.2345)>"


def test_point_equality():
    """Test points."""
    point1 = Point(10.0, 15.0)
    point2 = Point(10.0, 15.0)
    assert point1 == point2


def test_polygon():
    """Test polygon."""
    polygon = Polygon(
        [
            Point(-30.1, 150.1),
            Point(-30.2, 150.2),
            Point(-30.4, 150.4),
            Point(-30.8, 150.8),
            Point(-30.1, 150.1),
        ]
    )
    assert len(polygon.points) == 5
    assert polygon.centroid.latitude == -30.32
    assert polygon.centroid.longitude == 150.32
    assert (
        repr(polygon) == "<Polygon(centroid="
        "<Point(latitude=-30.32, longitude=150.32)>)>"
    )


def test_polygon_equality():
    """Test points."""
    polygon1 = Polygon(
        [
            Point(30.0, 30.0),
            Point(30.0, 35.0),
            Point(35.0, 35.0),
            Point(35.0, 30.0),
            Point(30.0, 30.0),
        ]
    )
    polygon2 = Polygon(
        [
            Point(30.0, 30.0),
            Point(30.0, 35.0),
            Point(35.0, 35.0),
            Point(35.0, 30.0),
            Point(30.0, 30.0),
        ]
    )
    assert polygon1 == polygon2
