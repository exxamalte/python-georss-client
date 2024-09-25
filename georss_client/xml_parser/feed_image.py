"""GeoRSS feed image."""

from __future__ import annotations

from georss_client.consts import XML_TAG_HEIGHT, XML_TAG_URL, XML_TAG_WIDTH
from georss_client.xml_parser.feed_dict_source import FeedDictSource


class FeedImage(FeedDictSource):
    """Represents a feed image."""

    @property
    def url(self) -> str | None:
        """Return the url of this feed image."""
        return self._attribute([XML_TAG_URL])

    @property
    def height(self) -> int | None:
        """Return the height of this feed image."""
        return self._attribute([XML_TAG_HEIGHT])

    @property
    def width(self) -> int | None:
        """Return the width of this feed image."""
        return self._attribute([XML_TAG_WIDTH])
