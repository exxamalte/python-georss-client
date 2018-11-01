"""

"""
import logging
import xmltodict
import atoma

_LOGGER = logging.getLogger(__name__)


class XmlParser:
    """Built-in XML parser."""

    def __init__(self, encoding):
        """Initialise the XML parser."""
        self._encoding = encoding

    def parse(self, xml):
        """Parse the provided xml."""
        if xml:
            # Retain full control over namespaces.
            # namespaces = {
            #     'http://www.w3.org/2005/Atom': None,
            #     'http://purl.org/dc/elements/1.1/': 'dc',
            #     'http://www.georss.org/georss': 'georss',
            #     'http://www.w3.org/2003/01/geo/wgs84_pos#': 'geo',
            #     'http://www.opengis.net/gml': 'gml',
            # }
            # parsed_xml = xmltodict.parse(xml, process_namespaces=True,
            #                              namespaces=namespaces)

            # parsed_xml = atoma.parse_atom_bytes(bytes(xml, self._encoding))
            parsed_xml = atoma.parse_rss_bytes(bytes(xml, self._encoding))
            return parsed_xml
            # self.parsed_xml = parsed_xml
            # _LOGGER.debug("XML parsed: %s", parsed_xml)
            # if parsed_xml and 'feed' in parsed_xml:
            #     # Read global feed attributes
            #     global_attributes = {}
            #     for key in parsed_xml['feed'].keys():
            #         if key != 'entry':
            #             global_attributes[key] = parsed_xml['feed'][key]
            #     # Read entries
            #     entries = []
            #     if 'entry' in parsed_xml['feed'].keys():
            #         entries.extend(parsed_xml['feed']['entry'])
            #     feed = {}
            #     feed['feed'] = global_attributes
            #     feed['entries'] = entries
            #     return feed
        return None


# class Feed:
#
#     def id(self) -> Optional[str]:
