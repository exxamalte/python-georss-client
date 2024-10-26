"""GeoRSS feed models."""

from __future__ import annotations

import logging

from georss_client.consts import (
    XML_TAG_COPYRIGHT,
    XML_TAG_DOCS,
    XML_TAG_ENTRY,
    XML_TAG_GENERATOR,
    XML_TAG_IMAGE,
    XML_TAG_ITEM,
    XML_TAG_LANGUAGE,
    XML_TAG_RIGHTS,
    XML_TAG_SUBTITLE,
    XML_TAG_TTL,
)
from georss_client.xml_parser.feed_image import FeedImage
from georss_client.xml_parser.feed_item import FeedItem
from georss_client.xml_parser.feed_or_feed_item import FeedOrFeedItem

_LOGGER = logging.getLogger(__name__)


class Feed(FeedOrFeedItem):
    """Represents a feed."""

    @property
    def subtitle(self) -> str | None:
        """Return the subtitle of this feed."""
        return self._attribute_with_text([XML_TAG_SUBTITLE])

    @property
    def copyright(self) -> str | None:
        """Return the copyright of this feed."""
        return self._attribute_with_text([XML_TAG_COPYRIGHT, XML_TAG_RIGHTS])

    @property
    def rights(self) -> str | None:
        """Return the rights of this feed."""
        return self.copyright

    @property
    def generator(self) -> str | None:
        """Return the generator of this feed."""
        return self._attribute_with_text([XML_TAG_GENERATOR])

    @property
    def language(self) -> str | None:
        """Return the language of this feed."""
        return self._attribute([XML_TAG_LANGUAGE])

    @property
    def docs(self) -> str | None:
        """Return the docs URL of this feed."""
        return self._attribute_with_text([XML_TAG_DOCS])

    @property
    def ttl(self) -> int | None:
        """Return the ttl of this feed."""
        return self._attribute([XML_TAG_TTL])

    @property
    def image(self) -> FeedImage | None:
        """Return the image of this feed."""
        image = self._attribute([XML_TAG_IMAGE])
        if image:
            return FeedImage(image)
        return None

    @property
    def entries(self) -> list[FeedItem]:
        """Return the entries of this feed."""
        items = self._attribute([XML_TAG_ITEM, XML_TAG_ENTRY])
        entries = []
        if items and isinstance(items, list):
            entries = [FeedItem(item) for item in items]
        else:
            # A single item in the feed is not represented as an array.
            entries.append(FeedItem(items))
        return entries
