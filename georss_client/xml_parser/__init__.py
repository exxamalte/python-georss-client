"""
XML Parser.
"""
import dateparser as dateparser
import logging
import xmltodict

from georss_client.consts import XML_TAG_DC_DATE, XML_TAG_LAST_BUILD_DATE, \
    XML_TAG_PUB_DATE, XML_TAG_PUBLISHED, XML_TAG_UPDATED, XML_TAG_GEO_LAT, \
    XML_TAG_GEO_LONG, XML_TAG_GEORSS_POLYGON, XML_TAG_GML_POS_LIST, \
    XML_TAG_GML_POS, XML_TAG_GEORSS_POINT, XML_TAG_HEIGHT, XML_TAG_TTL, \
    XML_TAG_WIDTH, XML_TAG_RSS, XML_TAG_CHANNEL, XML_TAG_FEED
from georss_client.xml_parser.feed import Feed

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAMESPACES = {
    'http://www.w3.org/2005/Atom': None,
    'http://purl.org/dc/elements/1.1/': 'dc',
    'http://www.georss.org/georss': 'georss',
    'http://www.w3.org/2003/01/geo/wgs84_pos#': 'geo',
    'http://www.opengis.net/gml': 'gml',
    'http://www.gdacs.org/': 'gdacs',
}
KEYS_DATE = [XML_TAG_DC_DATE, XML_TAG_LAST_BUILD_DATE, XML_TAG_PUB_DATE,
             XML_TAG_PUBLISHED, XML_TAG_UPDATED]
KEYS_FLOAT = [XML_TAG_GEO_LAT, XML_TAG_GEO_LONG]
KEYS_FLOAT_LIST = [XML_TAG_GEORSS_POLYGON, XML_TAG_GML_POS_LIST,
                   XML_TAG_GML_POS, XML_TAG_GEORSS_POINT]
KEYS_INT = [XML_TAG_HEIGHT, XML_TAG_TTL, XML_TAG_WIDTH]


class XmlParser:
    """Built-in XML parser."""

    def __init__(self, additional_namespaces=None):
        """Initialise the XML parser."""
        self._namespaces = DEFAULT_NAMESPACES
        if additional_namespaces:
            self._namespaces.update(additional_namespaces)

    def parse(self, xml):
        """Parse the provided xml."""
        if xml:

            def postprocessor(path, key, value):
                """Conduct type conversion for selected keys."""
                try:
                    if key in KEYS_DATE and value:
                        return key, dateparser.parse(value)
                    if key in KEYS_FLOAT and value:
                        return key, float(value)
                    if key in KEYS_FLOAT_LIST and value:
                        # Turn white-space separated list of numbers into
                        # list of floats.
                        coordinate_values = value.split()
                        point_coordinates = []
                        for i in range(0, len(coordinate_values)):
                            point_coordinates.append(
                                float(coordinate_values[i]))
                        return key, point_coordinates
                    if key in KEYS_INT and value:
                        return key, int(value)
                except (ValueError, TypeError) as error:
                    _LOGGER.warning("Unable to process (%s/%s): %s",
                                    key, value, error)
                return key, value

            parsed_dict = xmltodict.parse(
                xml, process_namespaces=True, namespaces=self._namespaces,
                postprocessor=postprocessor)

            if XML_TAG_RSS in parsed_dict:
                rss = parsed_dict.get(XML_TAG_RSS)
                if XML_TAG_CHANNEL in rss:
                    channel = rss.get(XML_TAG_CHANNEL)
                    return Feed(channel)
            if XML_TAG_FEED in parsed_dict:
                feed = parsed_dict.get(XML_TAG_FEED)
                return Feed(feed)

        return None
