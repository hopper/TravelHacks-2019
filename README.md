# TravelHacks 2019

* [List of schemas](#List-of-schemas)
     * [flight_airports](#flight_airports)
     * [flight_schedules](#flight_schedules)
     * [hotel_geo_metadata](#hotel_geo_metadata)
     * [flight_trips](#flight_trips)
     * [flight_segments](#flight_segments)
* [Resources](#resources)
    * [Google Cloud tutorials and documentation](#Google-Cloud-tutorials-and-documentation)

## Glossary

IATA: International Air Transport Association. Source of many standards associated with air travel.

## List of schemas

### flight_airports

| Columns | Data Type | Description |
|-|-|-|
| `name` | `string` | Name of the airport |
| `latitude` | `double` | Latitude of the airport |
| `longitude` | `double` | Longitude of the airport |
| `iata_code` | `string` | Three-letter IATA code for the airport, e.g. BOS. Usable as a primary key. |
| `mac_iata_code` | `string` | Three-letter IATA metropolitan area code for the airport, e.g. JFK is part of NYC. |
| `country_code` | `string` | Two letter ISO-3166 country code for this airport, e.g. US. |
| `continent_code` | `string` | Two letter ISO-3166 continent code for this airport, e.g. NA. |
| `currency_code` | `string` | Three letter ISO-4217 currency code, e.g. USD. |
| `timezone` | `string` | The timezone prevailing at the airport, e.g. America/New_York |
| `score` | `double` | An ad hoc measure of airport volume or importance, from 0-1. Provided for convenience, but you can probably do better than this without too much effort. |

### flight_schedules

 A table of past and future flight schedules, including their seat capacities and codes in a long table format. From Innovata.

Usage caveats:

If a flight has codeshares, it will have a row for every flight number. E.g. if there is one codeshare, there will be two rows, one for the operating carrier number and another for the codeshare. Set codeshareIndicator = 0 to filter out codeshares to avoid duplicates

If a flight has a hidden stop, it will have a row for all consecutive combinations of segment combinations. E.g. CX888 appears 3 times as HKG-JFK, HKG-YVR, and YVR-JFK as there is a hidden stop in YVR. Set stops = 0 to filter out flights with hidden stops to avoid duplicates

Flight schedules are subject to change. Innovata sends schedules on an approximately 4 week basis. Each schedule only contains flights for the future, so there may be schedule changes that happened in the previous 4 weeks that are unaccounted for. Moreover, flights scheduled for the future may change in future schedules. received_date is the date that we received the final innovata schedule for the flight; if received_date is in the future, it means that future innovata schedules may change the current information. 

**Partitioned By** : `date`

| Columns | Data Type | Description |
|-|-|-|
| `origin` | `string` | Origin airport code. |
| `destination` | `string` | Destination airport code. |
| `carrier` | `string` | Carrier code. |
| `flightnumber` | `string` | Flight number of flight. |
| `departure_time` | `string` | Departure Time Local |
| `arrival_time` | `string` | Arrival Time Local |
| `equipment_subtype` | `string` | Type of plane used, subtype |
| `equipment_group` | `string` | Type of plane used, equipment group |
| `date` | `date` | Date of flight |
| `date_weekday` | `integer` | Day of week, Monday = 1, ... Sunday = 7 |
| `seats_total` | `double` | Total number of seats |
| `seats_economy` | `double` | Economy seats |
| `seats_premium_economy` | `double` | Premium economy seats |
| `seats_business` | `double` | Business seats |
| `seats_first` | `double` | First class seats |

### hotel_geo_metadata

Basic metadata for hotels

| Columns | Data Type | Description |
|-|-|-|
| `ID` | `long` | unique ID of the hotel in Giata database |
| `name` | `string` | Name of the hotel |
| `category_name` | `string` | Category of the lodging (e.g. 'resort', 'aparthotel') |
| `Address` | `string` | Address of the hotel |
| `latitude` | `double` | latitude of the lodging|
| `longitude` | `double` | longitude of the lodging |
| `Accuracy` | `string` | Accuracy of the coordinates (usually 'address', 'street', 'city') |

### internal_flight_trips

Itineraries received in response to requests by Hopper on the behalf of our users.

`event.id` and `trip_index` together form a primary key that can be joined with `internal_flight_segments`.

**Partitioned By** : `received_date`, `trip_type`

| Columns | Data Type | Description |
|-|-|-|
| `event_id` | `string` | A source-specific unique ID for this shop (list of trips). |
| `trip_index` | `integer` | Trip index (row number) within the original shop (list of trips) |
| `origin` | `string` |  |
| `destination` | `string` |  |
| `major_carrier_id` | `string` | Main carrier involved in the trip, based on some logic for marketing carriers and segment length |
| `total_stops` | `integer` | Total number of stops in the trip |
| `advance` | `integer` | Days before trip, in origin timezone |
| `los` | `integer` | Length of stay: number of nights stay involved in the trip. Same day return is 0. |
| `includes_saturday_night_stay` | `boolean` | Does the trip include a Saturday night stay? Certain airlines use this as a rule of thumb for business travel: round trips not including a Saturday night are believed to be business travel, and prices are often higher on the assumption that corporate travelers are less price-sensitive than leisure travellers. |
| `available_seats` | `integer` | How many seats are nominally available for sale in this fare class? Typically 0-9, not directly related to number of physical seats left on the plane(s). Once this number hits zero, another fare class is reached, and price may increase. |
| `lowest_cabin_class` | `string` | Lowest class of service amongst the segments in this trip |
| `highest_cabin_class` | `string` | Highest class of service amongst the segments in this trip |
| `received_odate` | `string` | The date this trip was received. Based on origin timezone, i.e. the date the user at that origin would say it was. |
| `timestamp_ms` | `long` | Timestamp the search occurred in epoch millis |
| `received_date` | `date` | Date the trip was received, in the ET time zone |
| `trip_type` | `string` | Type of trip; one of `one_way`, `round_trip`, `open_jaw` |
| `event_source` | `string` | The shopping provider system that generated these search results |
| `fare.total_usd` | `double` | Total ticket price in USD, including all taxes and fees |
| `fare.tax_usd` | `double` | Tax component of the ticket price |
| `fare.surcharge_usd` | `double` | Surcharge component (identically zero?) |
| `fare.currency` | `string` | Currency the trip was originally priced in |
| `fare.total` | `double` | Total ticket price in original `currency` units |
| `fare.tax` | `double` | Tax amount in original currency |
| `fare.surcharge` | `double` | Surcharge in original currency |
| `fare.exchange_rate` | `double` | Exchange rate used for conversion to USD |
| `fare.pax_type` | `string` | Code for passenger type used for quote, typically ADT for adult |
| `fare.refundable` | `boolean` | Whether this ticket is refundable |
| `fare.point_of_sale_country_code` | `string` | Country code for point of sale where ticket was priced |
| `fare.validating_carrier` | `string` | Carrier code for the airline selling the ticket (not necessarily flying it) |
| `fare.conversation_id` | `string` | Unique identifier for the search in the source system |
| `outgoing.origin` | `string` | Three letter airport code like BOS for slice origination |
| `outgoing.destination` | `string` | Three letter code like YUL for slice destination |
| `outgoing.departure_odate` | `string` | Departure date in origin timezone in yyyy-mm-dd format |
| `outgoing.departure_ms` | `long` | Departure time in epoch millis |
| `outgoing.departure_day_of_week_mon1` | `integer` | Departing day of week in origin timezone, within Monday=1, Sunday=7 |
| `outgoing.departure_tz_offset_ms` | `long` | Timezone offset in millis for origin |
| `outgoing.departure_country_code` | `string` | Two letter ISO country code for origin |
| `outgoing.departure_subdivision_code` | `string` | Three letter ISO 3166-2 code for subdivision (e.g. province or state) |
| `outgoing.departure_currency_code` | `string` | Three letter ISO currency code for origin |
| `outgoing.arrival_ddate` | `string` | Arrival date in destination timezone in yyyy-mm-dd format |
| `outgoing.arrival_ms` | `long` | Arrival time in epoch millis |
| `outgoing.arrival_day_of_week_mon1` | `integer` | Arrival day of week at destination |
| `outgoing.arrival_tz_offset_ms` | `long` | Timezone offset in millis at destination |
| `outgoing.arrival_country_code` | `string` |  |
| `outgoing.arrival_subdivision_code` | `string` |  |
| `outgoing.arrival_currency_code` | `string` |  |
| `outgoing.layovers` | `array` | List of layover airport codes |
| `outgoing.marketing_carriers` | `array` | List of marketing carriers, the airlines advertised to the customer, e.g. via codeshare |
| `outgoing.operating_carriers` | `array` | List of operating carriers, the airlines that actually fly the plane |
| `outgoing.duration_minutes` | `integer` | Total length of travel (including layovers?) in minutes |
| `outgoing.stops` | `integer` | Number of stops for the slice |
| `returning.origin` | `string` | Three letter airport code like BOS for slice origination |
| `returning.destination` | `string` | Three letter code like YUL for slice destination |
| `returning.departure_odate` | `string` | Departure date in origin timezone in yyyy-mm-dd format |
| `returning.departure_ms` | `long` | Departure time in epoch millis |
| `returning.departure_day_of_week_mon1` | `integer` | Departing day of week in origin timezone, within Monday=1, Sunday=7 |
| `returning.departure_tz_offset_ms` | `long` | Timezone offset in millis for origin |
| `returning.departure_country_code` | `string` | Two letter ISO country code for origin |
| `returning.departure_subdivision_code` | `string` |  |
| `returning.departure_currency_code` | `string` | Three letter ISO currency code for origin |
| `returning.arrival_ddate` | `string` | Arrival date in destination timezone in yyyy-mm-dd format |
| `returning.arrival_ms` | `long` | Arrival time in epoch millis |
| `returning.arrival_day_of_week_mon1` | `integer` | Arrival day of week at destination |
| `returning.arrival_tz_offset_ms` | `long` | Timezone offset in millis at destination |
| `returning.arrival_country_code` | `string` |  |
| `returning.arrival_subdivision_code` | `string` |  |
| `returning.arrival_currency_code` | `string` |  |
| `returning.layovers` | `array` | List of layover airport codes |
| `returning.marketing_carriers` | `array` | List of marketing carriers, the airlines advertised to the customer, e.g. via codeshare |
| `returning.operating_carriers` | `array` | List of operating carriers, the airlines that actually fly the plane |
| `returning.duration_minutes` | `integer` | Total length of travel (including layovers) in minutes |
| `returning.stops` | `integer` | Number of stops for the slice |
| `query.origin_type` | `string` | Type for origin, either `airport` or `city` |
| `query.origin` | `string` | Origin code, e.g. BOS or YMQ |
| `query.destination_type` | `string` |  |
| `query.destination` | `string` |  |
| `query.departure_date` | `string` | Departure date |
| `query.return_date` | `string` |  |
| `cities.origin` | `string` | Origin for outbound |
| `cities.destination` | `string` | Destination for outbound |
| `cities.return_origin` | `string` | Origin for returning (typically same as `destination`) |
| `cities.return_destination` | `string` | Destination for returning (typically same as `origin`) |
| `cities.same_origin` | `boolean` | Whether slices coincide at origin |
| `cities.same_destination` | `boolean` | Whether slices coincide at destination |
| `cities.is_roundtrip` | `boolean` |  |

### internal_flight_segments

All segments (legs) within each trip of a shop, joinable with `internal_flight_trips` using the combination of `trip_index` and `event.id` as a foreign key.

**Partitioned By** : `received_date`, `trip_type`

| Columns | Data Type | Description |
|-|-|-|
| `event.id` | `string` | A source-specific unique ID for this shop (list of trips). |
| `trip_index` | `integer` | Index of this trip within the shop event |
| `segment_index` | `integer` | Index of this slice within the trip |
| `origin` | `string` | Origin airport for this slice |
| `destination` | `string` | Destination airport for this slice |
| `departure_ms` | `long` | Departure time in epoch millis |
| `arrival_ms` | `long` | Arrival time in epoch millis |
| `duration` | `integer` | Flight duration in minutes |
| `flight_number` | `string` | Flight number |
| `equipment_code` | `string` | Aircraft type |
| `marketing_carrier` | `string` | Carrier marketing this flight, e.g. via a codeshare |
| `operating_carrier` | `string` | Carrier flying the plane |
| `code_shared_carrier` | `string` | ? |
| `fare_code` | `string` | Fare basis code for this segment |
| `carrier_cabin_class` | `string` | Cabin class according to the carrier |
| `hopper_cabin_class` | `string` | Standardized cabin class according to Hopper, one of E - Economy, EP - Premium Economy, B - Business, F - First, U - Unknown |
| `stops` | `integer` | Number of stops within this segment, sometimes not requiring deplaning(?) |
| `available_seats` | `integer` | Nominally availability (0-9) for this segment in this fare class |
| `booking_code` | `string` | Fare bucket (A-Z) typically the first letter of the fare basis code |
| `received_date` | `date` | Received date in Hopper TZ (partition) |
| `trip_type` | `string` | Trip type (partition) |
| `event.source` | `string` | The shopping provider system that generated these search results |
| `cities.origin` | `string` |  |
| `cities.destination` | `string` |  |

# Resources

## Google Cloud tutorials and documentation

* [Qwiklabs: Google Developer Essentials](https://google.qwiklabs.com/quests/86?qlcampaign=5l-hack-23)
