# python-georss-client

[![Build Status](https://github.com/exxamalte/python-georss-client/workflows/CI/badge.svg?branch=master)](https://github.com/exxamalte/python-georss-client/actions?workflow=CI)
[![codecov](https://codecov.io/gh/exxamalte/python-georss-client/branch/master/graph/badge.svg?token=8L93XZYRJK)](https://codecov.io/gh/exxamalte/python-georss-client)
[![PyPi](https://img.shields.io/pypi/v/georss-client.svg)](https://pypi.python.org/pypi/georss-client)
[![Version](https://img.shields.io/pypi/pyversions/georss-client.svg)](https://pypi.python.org/pypi/georss-client)
[![Maintainability](https://api.codeclimate.com/v1/badges/ed2a70f3af0c2324dcce/maintainability)](https://codeclimate.com/github/exxamalte/python-georss-client/maintainability)

This library is a framework to build concrete libraries for convenient access 
to [GeoRSS](http://www.georss.org/) Feeds.


## Installation
`pip install georss-client`


## Known Implementations

| Library | Source | Topic |
|---------|--------|-------|
| [python-georss-generic-client](https://github.com/exxamalte/python-georss-generic-client) | Generic GeoRSS Feeds | misc |
| [python-georss-ign-sismologia-client](https://github.com/exxamalte/python-georss-ign-sismologia-client) | Instituto Geográfico Nacional Sismología | Earthquakes |
| [python-georss-ingv-centro-nazionale-terremoti-client](https://github.com/exxamalte/python-georss-ingv-centro-nazionale-terremoti-client) | INGV Centro Nazionale Terremoti | Earthquakes |
| [python-georss-nrcan-earthquakes-client](https://github.com/exxamalte/python-georss-nrcan-earthquakes-client) | Natural Resources Canada | Earthquakes |
| [python-georss-qld-bushfire-alert-client](https://github.com/exxamalte/python-georss-qld-bushfire-alert-client) | Queensland Bushfire Alert | Fires |
| [python-georss-tfs-incidents-client](https://github.com/exxamalte/python-georss-tfs-incidents-client) | Tasmania Fire Service Incidents | Fires |
| [python-georss-wa-dfes-client](https://github.com/exxamalte/python-georss-wa-dfes-client) | Western Australia Department of Fire and Emergency Services | Fires |


## Usage
Each implementation extracts relevant information from the GeoRSS feed. Not all
feeds contain the same level of information, or present their information in
different ways.

After instantiating a particular class and supply the required 
parameters, you can call `update` to retrieve the feed data. The return 
value will be a tuple of a status code and the actual data in the form of a 
list of feed entries specific to the selected feed.

Status Codes
* _UPDATE_OK_: Update went fine and data was retrieved. The library may still return empty data, for example because no entries fulfilled the filter criteria.
* _UPDATE_OK_NO_DATA_: Update went fine but no data was retrieved, for example because the server indicated that there was not update since the last request.
* _UPDATE_ERROR_: Something went wrong during the update

## Feed Managers

The Feed Managers help managing feed updates over time, by notifying the 
consumer of the feed about new feed entries, updates and removed entries 
compared to the last feed update.

* If the current feed update is the first one, then all feed entries will be 
  reported as new. The feed manager will keep track of all feed entries' 
  external IDs that it has successfully processed.
* If the current feed update is not the first one, then the feed manager will 
  produce three sets:
  * Feed entries that were not in the previous feed update but are in the 
    current feed update will be reported as new.
  * Feed entries that were in the previous feed update and are still in the 
    current feed update will be reported as to be updated.
  * Feed entries that were in the previous feed update but are not in the 
    current feed update will be reported to be removed.
* If the current update fails, then all feed entries processed in the previous
  feed update will be reported to be removed.

After a successful update from the feed, the feed manager will provide two
different dates:

* `last_update` will be the timestamp of the last successful update from the
  feed. This date may be useful if the consumer of this library wants to
  treat intermittent errors from feed updates differently.
* `last_timestamp` will be the latest timestamp extracted from the feed data. 
  This requires that the underlying feed data actually contains a suitable 
  date. This date may be useful if the consumer of this library wants to 
  process feed entries differently if they haven't actually been updated.
