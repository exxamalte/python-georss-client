"""GeoRSS Feed."""
from __future__ import annotations

import codecs
import logging
from datetime import datetime

import requests

from .consts import ATTR_ATTRIBUTION, UPDATE_ERROR, UPDATE_OK, UPDATE_OK_NO_DATA
from .xml_parser import XmlParser

_LOGGER = logging.getLogger(__name__)


class GeoRssFeed:
    """GeoRSS feed base class."""

    def __init__(
        self, home_coordinates, url, filter_radius=None, filter_categories=None
    ):
        """Initialise this service."""
        self._home_coordinates = home_coordinates
        self._filter_radius = filter_radius
        self._filter_categories = filter_categories
        self._url = url
        self._request = requests.Request(method="GET", url=url).prepare()
        self._last_timestamp = None

    def __repr__(self):
        """Return string representation of this feed."""
        return "<{}(home={}, url={}, radius={}, categories={})>".format(
            self.__class__.__name__,
            self._home_coordinates,
            self._url,
            self._filter_radius,
            self._filter_categories,
        )

    def _new_entry(self, home_coordinates, rss_entry, global_data):
        """Generate a new entry."""
        pass

    def _additional_namespaces(self):
        """Provide additional namespaces, relevant for this feed."""
        pass

    def update(self):
        """Update from external source and return filtered entries."""
        status, data = self._fetch()
        if status == UPDATE_OK:
            if data:
                entries = []
                global_data = self._extract_from_feed(data)
                # Extract data from feed entries.
                for rss_entry in data.entries:
                    entries.append(
                        self._new_entry(self._home_coordinates, rss_entry, global_data)
                    )
                filtered_entries = self._filter_entries(entries)
                self._last_timestamp = self._extract_last_timestamp(filtered_entries)
                return UPDATE_OK, filtered_entries
            else:
                # Should not happen.
                return UPDATE_OK, None
        elif status == UPDATE_OK_NO_DATA:
            # Happens for example if the server returns 304
            return UPDATE_OK_NO_DATA, None
        else:
            # Error happened while fetching the feed.
            return UPDATE_ERROR, None

    def _fetch(self):
        """Fetch GeoRSS data from external source."""
        try:
            with requests.Session() as session:
                response = session.send(self._request, timeout=10)
            if response.ok:
                self._pre_process_response(response)
                parser = XmlParser(self._additional_namespaces())
                feed_data = parser.parse(response.text)
                self.parser = parser
                self.feed_data = feed_data
                return UPDATE_OK, feed_data
            else:
                _LOGGER.warning(
                    "Fetching data from %s failed with status %s",
                    self._request.url,
                    response.status_code,
                )
                return UPDATE_ERROR, None
        except requests.exceptions.RequestException as request_ex:
            _LOGGER.warning(
                "Fetching data from %s failed with %s", self._request.url, request_ex
            )
            return UPDATE_ERROR, None

    def _pre_process_response(self, response):
        """Pre-process the response."""
        if response:
            _LOGGER.debug("Response encoding %s", response.encoding)
            if response.content.startswith(codecs.BOM_UTF8):
                _LOGGER.debug(
                    "UTF8 byte order mark detected, " "setting encoding to 'utf-8-sig'"
                )
                response.encoding = "utf-8-sig"

    def _filter_entries(self, entries):
        """Filter the provided entries."""
        filtered_entries = entries
        _LOGGER.debug("Entries before filtering %s", filtered_entries)
        # Always remove entries without geometry
        filtered_entries = list(
            filter(lambda entry: entry.geometry is not None, filtered_entries)
        )
        # Filter by distance.
        if self._filter_radius:
            filtered_entries = list(
                filter(
                    lambda entry: entry.distance_to_home <= self._filter_radius,
                    filtered_entries,
                )
            )
        # Filter by category.
        if self._filter_categories:
            filtered_entries = list(
                filter(
                    lambda entry: len(
                        {entry.category}.intersection(self._filter_categories)
                    )
                    > 0,
                    filtered_entries,
                )
            )
        _LOGGER.debug("Entries after filtering %s", filtered_entries)
        return filtered_entries

    def _extract_from_feed(self, feed):
        """Extract global metadata from feed."""
        global_data = {}
        author = feed.author
        if author:
            global_data[ATTR_ATTRIBUTION] = author
        return global_data

    def _extract_last_timestamp(self, feed_entries):
        """Determine latest (newest) entry from the filtered feed."""
        if feed_entries:
            dates = sorted(
                [entry.published for entry in feed_entries if entry.published],
                reverse=True,
            )
            if dates:
                last_timestamp = dates[0]
                _LOGGER.debug("Last timestamp: %s", last_timestamp)
                return last_timestamp
        return None

    @property
    def last_timestamp(self) -> datetime | None:
        """Return the last timestamp extracted from this feed."""
        return self._last_timestamp
