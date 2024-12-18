# Changes

## 0.18 (02/11/2024)
* Removed Python 3.8 support.
* Removed dateparser and replaced with python-dateutil.
* Bumped xmltodict to 0.14.2.
* Bumped ruff to 0.7.1.
* Code quality improvements.

## 0.17 (31/01/2024)
* Provide backwards compatibility with v0.15 by exposing constants.

## 0.16 (31/01/2024)
* Removed Python 3.7 support.
* Added Python 3.11 support.
* Added Python 3.12 support.
* Bumped requests to 2.31.0.
* Bumped dateparser to 1.2.0.
* Bumped haversine to 2.8.1.
* Bumped xmltodict to 0.13.0.
* Bumped library versions: black, flake8, isort.
* Migrated to pytest.
* Code quality improvements.

## 0.15 (16/02/2022)
* No functional changes.
* Migrated to github actions.
* Added Python 3.10 support.
* Removed Python 3.6 support.
* Bumped library versions: black, flake8, isort.

## 0.14 (08/06/2021)
* Add license tag (thanks @fabaff).
* General code improvements.

## 0.13 (20/04/2021)
* Python 3.9 support.

## 0.12 (30/12/2020)
* Add non-standard namespace used by [EMSC feed](https://www.emsc-csem.org/service/rss/rss.php).

## 0.11 (18/10/2020)
* Excluded tests from package (thanks @scop).
* Python 3.8 support.

## 0.10 (05/12/2019)
* Fix handling feeds starting with byte order mark.

## 0.9 (01/04/2019)
* Migrated Instituto Geográfico Nacional Sismología feed integration to [python-georss-ign-sismologia-client](https://github.com/exxamalte/python-georss-ign-sismologia-client)
* Migrated generic GeoRSS feed integration to [python-georss-generic-client](https://github.com/exxamalte/python-georss-generic-client)
* Migrated Western Australia Department of Fire and Emergency Services feed integration to [python-georss-wa-dfes-client](https://github.com/exxamalte/python-georss-wa-dfes-client)
* Migrated Queensland Fire and Emergency Services (QFES) Bushfire Alert feed integration to [python-georss-qfes-bushfire-alert-client](https://github.com/exxamalte/python-georss-qfes-bushfire-alert-client)
* Migrated Tasmania Fire Service Incidents feed to [python-georss-tfs-incidents-client](https://github.com/exxamalte/python-georss-tfs-incidents-client).
* Migrated INGV Centro Nazionale Terremoti (Earthquakes) feed to [python-georss-ingv-centro-nazionale-terremoti-client](https://github.com/exxamalte/python-georss-ingv-centro-nazionale-terremoti-client)
* Migrated Natural Resources Canada Earthquakes feed [python-georss-nrcan-earthquakes-client](https://github.com/exxamalte/python-georss-nrcan-earthquakes-client)
* Dropped Python 3.5 support.

## 0.8 (24/03/2019)
* Fixed issue where the feed entries do not have any suitable timestamps.

## 0.7 (24/03/2019)
* Simple Feed Manager for all feeds added.

## 0.6 (20/03/2019)
* Support for Instituto Geográfico Nacional Sismología (Earthquakes) feed.

## 0.5 (14/12/2018)
* Built-in XML parser.
* Python 3.7 support.

## 0.4 (01/11/2018)
* Third-party library updates.

## 0.3 (08/10/2018)
* Filter out entries without any geo location data.
* Support for Natural Resources Canada Earthquakes feed.
* Support for INGV Centro Nazionale Terremoti (Earthquakes) feed.

## 0.2 (05/10/2018)
* Support for Tasmania Fire Service Incidents feed.
* Support for Western Australia Department of Fire and Emergency Services feed.

## 0.1 (27/09/2018)
* Initial release with support for generic GeoRSS feeds and the QFES Bushfire Alert feed.
* Calculating distance to home coordinates.
* Support for filtering by distance and category for all feeds.
