"""
Tasmania Fire Service Incidents Feed.

Fetches GeoRSS feed from Tasmania Fire Service Incidents Feed.
"""
from georss_client import GeoRssFeed, FeedEntry
from georss_client.consts import CUSTOM_ATTRIBUTE
from georss_client.feed_manager import FeedManagerBase

ATTRIBUTION = "Tasmania Fire Service"

REGEXP_ATTR_LOCATION = 'LOCATION: (?P<{}>[^<]+)<br />'\
    .format(CUSTOM_ATTRIBUTE)
REGEXP_ATTR_REGION = 'Region: (?P<{}>[^<]+)<br />'\
    .format(CUSTOM_ATTRIBUTE)
REGEXP_ATTR_RESPONSIBLE_AGENCY = 'RESPONSIBLE AGENCY: (?P<{}>[^<]+)<br />'\
    .format(CUSTOM_ATTRIBUTE)
REGEXP_ATTR_SIZE = 'SIZE: (?P<{}>[^<]+)<br />'\
    .format(CUSTOM_ATTRIBUTE)
REGEXP_ATTR_STATUS = 'STATUS: (?P<{}>[^<]+)<br />'\
    .format(CUSTOM_ATTRIBUTE)
REGEXP_ATTR_TYPE = 'TYPE: (?P<{}>[^<]+)<br />'\
    .format(CUSTOM_ATTRIBUTE)

URL = "http://www.fire.tas.gov.au/Show?pageId=colBushfireSummariesRss"

VALID_CATEGORIES = ['Emergency Warning', 'Watch and Act', 'Advice',
                    'No Alert Level']


class TfsIncidentsFeedManager(FeedManagerBase):
    """Feed Manager for Tasmania Fire Service Incidents feed."""

    def __init__(self, generate_callback, update_callback, remove_callback,
                 coordinates, filter_radius=None,
                 filter_categories=None):
        """Initialize the Tasmania Fire Service Incidents Feed Manager."""
        feed = TfsIncidentsFeed(
            coordinates,
            filter_radius=filter_radius,
            filter_categories=filter_categories)
        super().__init__(feed, generate_callback, update_callback,
                         remove_callback)


class TfsIncidentsFeed(GeoRssFeed):
    """Tasmania Fire Service Incidents feed."""

    def __init__(self, home_coordinates, filter_radius=None,
                 filter_categories=None):
        """Initialise this service."""
        super().__init__(home_coordinates, URL, filter_radius=filter_radius)
        self._filter_categories = filter_categories

    def _new_entry(self, home_coordinates, rss_entry, global_data):
        """Generate a new entry."""
        return TfsIncidentsFeedEntry(home_coordinates, rss_entry)

    def _filter_entries(self, entries):
        """Filter the provided entries."""
        entries = super()._filter_entries(entries)
        if self._filter_categories:
            return list(filter(lambda entry:
                               entry.category in self._filter_categories,
                               entries))
        return entries


class TfsIncidentsFeedEntry(FeedEntry):
    """Tasmania Fire Service Incidents feed entry."""

    def __init__(self, home_coordinates, rss_entry):
        """Initialise this service."""
        super().__init__(home_coordinates, rss_entry)

    @property
    def attribution(self) -> str:
        """Return the attribution of this entry."""
        return ATTRIBUTION

    @property
    def location(self) -> str:
        """Return the location of this entry."""
        return self._search_in_description(REGEXP_ATTR_LOCATION)

    @property
    def region(self) -> str:
        """Return the region of this entry."""
        return self._search_in_description(REGEXP_ATTR_REGION)

    @property
    def responsible_agency(self) -> str:
        """Return the responsible agency of this entry."""
        return self._search_in_description(REGEXP_ATTR_RESPONSIBLE_AGENCY)

    @property
    def status(self) -> str:
        """Return the status of this entry."""
        return self._search_in_description(REGEXP_ATTR_STATUS)

    @property
    def size(self) -> str:
        """Return the size of this entry."""
        return self._search_in_description(REGEXP_ATTR_SIZE)

    @property
    def type(self) -> str:
        """Return the type of this entry."""
        return self._search_in_description(REGEXP_ATTR_TYPE)
