# python-georss-client

[![Build Status](https://travis-ci.org/exxamalte/python-georss-client.svg)](https://travis-ci.org/exxamalte/python-georss-client)
[![Coverage Status](https://coveralls.io/repos/github/exxamalte/python-georss-client/badge.svg?branch=master)](https://coveralls.io/github/exxamalte/python-georss-client?branch=master)

This library provides convenient access to [GeoRSS](http://www.georss.org/) Feeds.


## Installation
`pip install georss-client`

## Usage
See below for examples of how this library can be used for particular GeoRSS feeds. After instantiating a particular class and supply the required parameters, you can call `update` to retrieve the feed data. The return value will be a tuple of a status code and the actual data in the form of a list of feed entries specific to the selected feed.

Status Codes
* _UPDATE_OK_: Update went fine and data was retrieved. The library may still return empty data, for example because no entries fulfilled the filter criteria.
* _UPDATE_OK_NO_DATA_: Update went fine but no data was retrieved, for example because the server indicated that there was not update since the last request.
* _UPDATE_ERROR_: Something went wrong during the update

## Supported GeoRSS Feeds

### Generic Feed

**Supported Filters**

| Filter |                 | Description |
|--------|-----------------|-------------|
| Radius | `filter_radius` | Radius in kilometers around the home coordinates in which events from feed are included. |

**Example**
```python
from georss_client.generic_feed import GenericFeed
# Home Coordinates: Latitude: -27.5, Longitude: 153.0
# Filter radius: 1000 km
feed = GenericFeed((-27.5, 153.0), filter_radius=200, 
                   url="https://www.qfes.qld.gov.au/data/alerts/bushfireAlert.xml")
status, entries = feed.update()
```

### [Queensland Fire and Emergency Services (QFES) Bushfire Alert Feed](https://www.ruralfire.qld.gov.au/map/Pages/default.aspx)

**Supported Filters**

| Filter     |                     | Description |
|------------|---------------------|-------------|
| Radius     | `filter_radius`     | Radius in kilometers around the home coordinates in which events from feed are included. |
| Categories | `filter_categories` | Array of category names. Only events with a category matching any of these is included. |

**Example**
```python
from georss_client.qfes_bushfire_alert_feed import QfesBushfireAlertFeed
# Home Coordinates: Latitude: -27.5, Longitude: 153.0
# Filter radius: 50 km
# Filter categories: 'Advice'
feed = QfesBushfireAlertFeed((-27.5, 153.0), filter_radius=50, filter_categories=['Advice'])
status, entries = feed.update()
```
