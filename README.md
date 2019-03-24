# python-georss-client

[![Build Status](https://travis-ci.org/exxamalte/python-georss-client.svg)](https://travis-ci.org/exxamalte/python-georss-client)
[![Coverage Status](https://coveralls.io/repos/github/exxamalte/python-georss-client/badge.svg?branch=master)](https://coveralls.io/github/exxamalte/python-georss-client?branch=master)
[![PyPi](https://img.shields.io/pypi/v/georss-client.svg)](https://pypi.python.org/pypi/georss-client)
[![Version](https://img.shields.io/pypi/pyversions/georss-client.svg)](https://pypi.python.org/pypi/georss-client)
[![Maintainability](https://api.codeclimate.com/v1/badges/ed2a70f3af0c2324dcce/maintainability)](https://codeclimate.com/github/exxamalte/python-georss-client/maintainability)

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

| Filter |                         | Description |
|--------|-------------------------|-------------|
| Radius | `filter_radius`         | Radius in kilometers around the home coordinates in which events from feed are included. |
| Categories | `filter_categories` | Array of category names. Only events with a category matching any of these is included. |

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
feed = QfesBushfireAlertFeed((-27.5, 153.0), filter_radius=50, 
                             filter_categories=['Advice'])
status, entries = feed.update()
```

### [Tasmania Fire Service Incidents Feed](http://www.fire.tas.gov.au/Show?pageId=colCurrentBushfires)

**Supported Filters**

| Filter     |                     | Description |
|------------|---------------------|-------------|
| Radius     | `filter_radius`     | Radius in kilometers around the home coordinates in which events from feed are included. |
| Categories | `filter_categories` | Array of category names. Only events with a category matching any of these is included. |

**Example**
```python
from georss_client.tasmania_fire_service_incidents_feed import TfsIncidentsFeed
# Home Coordinates: Latitude: -41.5, Longitude: 148.0
# Filter radius: 50 km
feed = TfsIncidentsFeed((-41.5, 148.0), filter_radius=50)
status, entries = feed.update()
```

### [Western Australia Department of Fire and Emergency Services Feed](https://www.emergency.wa.gov.au/)

**Supported Feeds**

| Category  | Feed            |
|-----------|-----------------|
| Warnings  | `warnings`      |
| Incidents | `all_incidents` |

**Supported Filters**

| Filter     |                     | Description |
|------------|---------------------|-------------|
| Radius     | `filter_radius`     | Radius in kilometers around the home coordinates in which events from feed are included. |
| Categories | `filter_categories` | Array of category names. Only events with a category matching any of these is included. |

**Example**
```python
from georss_client.wa_dfes_feed import WaDfesFeed
# Home Coordinates: Latitude: -31.0, Longitude: 121.0
# Feed: Warnings
# Filter radius: 50 km
feed = WaDfesFeed((-31.0, 121.0), 'warnings', filter_radius=50)
status, entries = feed.update()
```

### [Natural Resources Canada Earthquakes Feed](http://www.earthquakescanada.nrcan.gc.ca/index-en.php)

**Supported Languages**

| Language | Feed |
|----------|------|
| English  | `en` |
| Français | `fr` |

**Supported Filters**

| Filter            |                            | Description |
|-------------------|----------------------------|-------------|
| Radius            | `filter_radius`            | Radius in kilometers around the home coordinates in which events from feed are included. |
| Minimum Magnitude | `filter_minimum_magnitude` | Minimum magnitude as float value. Only events with a magnitude equal or above this value are included. |

**Example**
```python
from georss_client.natural_resources_canada_earthquakes_feed import \
    NaturalResourcesCanadaEarthquakesFeed
# Home Coordinates: Latitude: 49.25, Longitude: -123.1
# Language: English
# Filter radius: 200 km
# Filter minimum magnitude: 4.0
feed = NaturalResourcesCanadaEarthquakesFeed((49.25, -123.1), 'en', 
                                             filter_radius=200,
                                             filter_minimum_magnitude=4.0)
status, entries = feed.update()
```

### [INGV Centro Nazionale Terremoti (Earthquakes) Feed](http://cnt.rm.ingv.it/)

**Supported Filters**

| Filter            |                            | Description |
|-------------------|----------------------------|-------------|
| Radius            | `filter_radius`            | Radius in kilometers around the home coordinates in which events from feed are included. |
| Minimum Magnitude | `filter_minimum_magnitude` | Minimum magnitude as float value. Only events with a magnitude equal or above this value are included. |

**Example**
```python
from georss_client.ingv_centro_nazionale_terremoti_feed import \
    IngvCentroNazionaleTerremotiFeed
# Home Coordinates: Latitude: 40.84, Longitude: 14.25
# Filter radius: 200 km
# Filter minimum magnitude: 4.0
feed = IngvCentroNazionaleTerremotiFeed((40.84, 14.25), filter_radius=200, 
                                        filter_minimum_magnitude=4.0)
status, entries = feed.update()
```

### [Instituto Geográfico Nacional Sismología (Earthquakes) Feed](http://www.ign.es/)

**Supported Filters**

| Filter            |                            | Description |
|-------------------|----------------------------|-------------|
| Radius            | `filter_radius`            | Radius in kilometers around the home coordinates in which events from feed are included. |
| Minimum Magnitude | `filter_minimum_magnitude` | Minimum magnitude as float value. Only events with a magnitude equal or above this value are included. |

**Example**
```python
from georss_client.ign_sismologia_feed import IgnSismologiaFeed
# Home Coordinates: Latitude: 40.38, Longitude: -3.72
# Filter radius: 200 km
# Filter minimum magnitude: 3.0
feed = IgnSismologiaFeed((40.38, -3.72), 
                         filter_radius=200,
                         filter_minimum_magnitude=3.0)
status, entries = feed.update()
```

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
