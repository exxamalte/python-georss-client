"""
INGV Centro Nazionale Terremoti (Earthquakes) Feed.

Fetches GeoRSS feed from INGV Centro Nazionale Terremoti.
"""
import calendar
import pytz
from datetime import datetime

from typing import Optional

from georss_client import GeoRssFeed, FeedEntry
from georss_client.consts import CUSTOM_ATTRIBUTE, ATTR_ATTRIBUTION

REGEXP_ATTR_MAGNITUDE = 'Magnitude\(M.{{0,3}}\) (?P<{}>[^ ]+) '\
    .format(CUSTOM_ATTRIBUTE)
REGEXP_ATTR_REGION = 'Magnitude\(M.{{0,3}}\) [^ ]+[ ]+-[ ]+(?P<{}>.+)$'\
    .format(CUSTOM_ATTRIBUTE)

URL = "http://cnt.rm.ingv.it/feed/atom/all_week"


class IngvCentroNazionaleTerremotiFeed(GeoRssFeed):
    """INGV Centro Nazionale Terremoti feed."""

    def __init__(self, home_coordinates, filter_radius=None,
                 filter_minimum_magnitude=None):
        """Initialise this service."""
        super().__init__(home_coordinates, URL, filter_radius=filter_radius)
        self._filter_minimum_magnitude = filter_minimum_magnitude

    def __repr__(self):
        """Return string representation of this feed."""
        return '<{}(home={}, url={}, radius={}, magnitude={})>'.format(
            self.__class__.__name__, self._home_coordinates, self._url,
            self._filter_radius, self._filter_minimum_magnitude)

    def _new_entry(self, home_coordinates, rss_entry, global_data):
        """Generate a new entry."""
        attribution = None if not global_data and ATTR_ATTRIBUTION not in \
            global_data else global_data[ATTR_ATTRIBUTION]
        return IngvCentroNazionaleTerremotiFeedEntry(home_coordinates,
                                                     rss_entry, attribution)

    def _filter_entries(self, entries):
        """Filter the provided entries."""
        entries = super()._filter_entries(entries)
        if self._filter_minimum_magnitude:
            # Return only entries that have an actual magnitude value, and
            # the value is equal or above the defined threshold.
            return list(filter(lambda entry:
                               entry.magnitude and entry.magnitude >= self.
                               _filter_minimum_magnitude, entries))
        return entries


class IngvCentroNazionaleTerremotiFeedEntry(FeedEntry):
    """INGV Centro Nazionale Terremoti feed entry."""

    def __init__(self, home_coordinates, rss_entry, attribution):
        """Initialise this service."""
        super().__init__(home_coordinates, rss_entry)
        self._attribution = attribution

    @property
    def attribution(self) -> str:
        """Return the attribution of this entry."""
        return self._attribution

    @property
    def magnitude(self) -> Optional[float]:
        """Return the magnitude of this entry."""
        magnitude = self._search_in_title(REGEXP_ATTR_MAGNITUDE)
        if magnitude:
            magnitude = float(magnitude)
        return magnitude

    @property
    def region(self) -> Optional[float]:
        """Return the region of this entry."""
        return self._search_in_title(REGEXP_ATTR_REGION)

    @property
    def published(self) -> Optional[datetime]:
        """Return the published date of this entry."""
        # The feed actually contains the original date of the event in a
        # "dc:date" tag, and the update in an "updated" tag. However, the
        # feedparser library reads the "dc:date" as updated and ignores the
        # "updated" tag.
        return self.updated

    @property
    def updated(self) -> Optional[datetime]:
        """Return the updated date of this entry."""
        if self._rss_entry:
            published_date = self._rss_entry.get('updated_parsed', None)
            if published_date:
                return datetime.fromtimestamp(calendar.timegm(
                    published_date), tz=pytz.utc)
        return None