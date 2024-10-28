"""Feed Entry."""

from __future__ import annotations

from datetime import datetime
import re

from .consts import CUSTOM_ATTRIBUTE
from .geo_rss_distance_helper import GeoRssDistanceHelper
from .xml_parser.feed_item import FeedItem
from .xml_parser.geometry import Geometry


class FeedEntry:
    """Feed entry base class."""

    def __init__(self, home_coordinates: tuple[float, float], rss_entry: FeedItem):
        """Initialise this feed entry."""
        self._home_coordinates: tuple[float, float] = home_coordinates
        self._rss_entry: FeedItem = rss_entry

    def __repr__(self):
        """Return string representation of this entry."""
        return f"<{self.__class__.__name__}(id={self.external_id})>"

    @property
    def geometry(self) -> Geometry | None:
        """Return all geometry details of this entry."""
        if self._rss_entry:
            return self._rss_entry.geometry
        return None

    @property
    def coordinates(self) -> tuple[float, float] | None:
        """Return the best coordinates (latitude, longitude) of this entry."""
        if self.geometry:
            return GeoRssDistanceHelper.extract_coordinates(self.geometry)
        return None

    @property
    def external_id(self) -> str | None:
        """Return the external id of this entry."""
        if self._rss_entry:
            external_id = self._rss_entry.guid
            if not external_id:
                external_id = self.title
            if not external_id:
                # Use geometry as ID as a fallback.
                external_id = hash(self.coordinates)
            return external_id
        return None

    def _search_in_external_id(self, regexp) -> str | None:
        """Find a sub-string in the entry's external id."""
        if self.external_id:
            match = re.search(regexp, self.external_id)
            if match:
                return match.group(CUSTOM_ATTRIBUTE)
        return None

    @property
    def title(self) -> str | None:
        """Return the title of this entry."""
        if self._rss_entry:
            return self._rss_entry.title
        return None

    def _search_in_title(self, regexp):
        """Find a sub-string in the entry's title."""
        if self.title:
            match = re.search(regexp, self.title)
            if match:
                return match.group(CUSTOM_ATTRIBUTE)
        return None

    @property
    def category(self) -> str | None:
        """Return the category of this entry."""
        if (
            self._rss_entry
            and self._rss_entry.category
            and isinstance(self._rss_entry.category, list)
        ):
            # To keep this simple, just return the first category.
            return self._rss_entry.category[0]
        return None

    @property
    def attribution(self) -> str | None:
        """Return the attribution of this entry."""
        return None

    @property
    def distance_to_home(self) -> float:
        """Return the distance in km of this entry to the home coordinates."""
        return GeoRssDistanceHelper.distance_to_geometry(
            self._home_coordinates, self.geometry
        )

    @property
    def description(self) -> str | None:
        """Return the description of this entry."""
        if self._rss_entry and self._rss_entry.description:
            return self._rss_entry.description
        return None

    @property
    def published(self) -> datetime | None:
        """Return the published date of this entry."""
        if self._rss_entry:
            return self._rss_entry.published_date
        return None

    @property
    def updated(self) -> datetime | None:
        """Return the updated date of this entry."""
        if self._rss_entry:
            return self._rss_entry.updated_date
        return None

    def _search_in_description(self, regexp):
        """Find a sub-string in the entry's description."""
        if self.description:
            match = re.search(regexp, self.description)
            if match:
                return match.group(CUSTOM_ATTRIBUTE)
        return None
