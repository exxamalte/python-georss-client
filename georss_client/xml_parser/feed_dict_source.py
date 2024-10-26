"""GeoRSS feed dict source."""

from __future__ import annotations

from typing import Optional

from georss_client.consts import (
    XML_ATTR_HREF,
    XML_CDATA,
    XML_TAG_CONTENT,
    XML_TAG_DESCRIPTION,
    XML_TAG_LINK,
    XML_TAG_SUMMARY,
    XML_TAG_TITLE,
)


class FeedDictSource:
    """Represents a subset of a feed based on a dict."""

    def __init__(self, source: dict):
        """Initialise feed."""
        self._source: dict = source

    def __repr__(self):
        """Return string representation of this feed item."""
        return f"<{self.__class__.__name__}({self.link})>"

    def _attribute(self, names: list[str]) -> Optional:
        """Get an attribute from this feed or feed item."""
        if self._source and names:
            # Try each name, and return the first value that is not None.
            for name in names:
                value = self._source.get(name, None)
                if value:
                    return value
        return None

    def _attribute_with_text(self, names: list[str]) -> Optional:
        """Get an attribute with text from this feed or feed item."""
        value = self._attribute(names)
        if value and isinstance(value, dict) and XML_CDATA in value:
            # <tag attr="/some.uri">Value</tag>
            value = value.get(XML_CDATA)
        return value

    @staticmethod
    def _attribute_in_structure(obj, keys: list[str]) -> Optional:
        """Return the attribute found under the chain of keys."""
        key = keys.pop(0)
        if key in obj:
            return (
                FeedDictSource._attribute_in_structure(obj[key], keys)
                if keys
                else obj[key]
            )
        return None

    @property
    def title(self) -> str | None:
        """Return the title of this feed or feed item."""
        return self._attribute_with_text([XML_TAG_TITLE])

    @property
    def description(self) -> str | None:
        """Return the description of this feed or feed item."""
        return self._attribute_with_text(
            [XML_TAG_DESCRIPTION, XML_TAG_SUMMARY, XML_TAG_CONTENT]
        )

    @property
    def summary(self) -> str | None:
        """Return the summary of this feed or feed item."""
        return self.description

    @property
    def content(self) -> str | None:
        """Return the content of this feed or feed item."""
        return self.description

    @property
    def link(self) -> str | None:
        """Return the link of this feed or feed item."""
        link = self._attribute([XML_TAG_LINK])
        if link and XML_ATTR_HREF in link:
            link = link.get(XML_ATTR_HREF)
        return link

    def get_additional_attribute(self, name: str) -> Optional:
        """Get an additional attribute not provided as property."""
        return self._attribute([name])
