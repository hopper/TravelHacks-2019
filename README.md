# TravelHacks 2019

* [Getting Started](#Getting-Started)
* [Glossary](#Glossary)
* [List of schemas](#List-of-schemas)
     * [flight_airports](#flight_airports)
     * [flight_schedules](#flight_schedules)
     * [hotel_geo_metadata](#hotel_geo_metadata)
     * [flight_trips](#flight_trips)
     * [flight_segments](#flight_segments)
     * [flight_shops](#flight_shops)
* [GCP bucket structure](#GCP_bucket_structure)
* [List of data slices](#List-of-data-slices)
* [Resources](#resources)
    * [Google Cloud tutorials and documentation](#Google-Cloud-tutorials-and-documentation)

## Getting Started

* The captain of the team should receive an invite e-mail, which will provide access to the TravelHacks GCP organization
* The captain should then create a project for the team, following instructions [here](https://cloud.google.com/resource-manager/docs/creating-managing-projects)
* From that point there are several possible options to the team. You should decide if you want to use BigQuery, use a Jupyter notebook, create a Dataproc cluster, etc.
Don't hesitate to call for help in case of [overchoice paralysis](https://en.wikipedia.org/wiki/Overchoice) 
* It is likely that you will want to run code locally using the GCP API, which will require valid credentials. In that case, see next section

### Using GCP Credentials locally

* Create a service account for your project, and give it the correct permissions [give it the correct permissions](https://cloud.google.com/iam/docs/creating-managing-service-accounts)
* Download the service account's credential json (this should be an available option when creating the service account)
* Export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials/json
* You should now be able to use the GCP API with any of their available clients

## Glossary

Here are some terms and acronyms used in the air travel industry. This will help you get a better grasp of the terms used in the data schemas.

See also [ATPCO's glossary](https://www.atpco.net/glossary).

 * Airline types
    * Disclosure - "For airline companies that have a code sharing agreement, the airline that operates the flight." (from Sabre)
    * Marketing - The carrier that sells a flight.
    * Operating - "The airline company or carrier that operates a flight. When a consumer requests an itinerary, the DOT requires the disclosure of the identity of the operating carrier by corporate name in any schedule that is displayed in a response." (abbreviated from Sabre)
    * Plating - a synonym for validating, used by Travelport in particular.
    * Validating - The carrier that collects payment, issues tickets, and distributes payment to any other carriers in the reservation. A Hopper user doesn't know this carrier unless they are issued travel credit for a cancellation. If the carriers in a reservation don't have an interline agreement, there are multiple validating carriers.
    * Primary - defined and used only internally at Hopper. For a slice, a primary carrier is the marketing carrier of the longest segment. For a trip, a primary carrier is the primary carrier of the first slice. We have multiple primary carriers for a trip only if a booking is multi tickets (a.k.a. hacker fares).
 * Codeshare - An agreement between two airlines in which the marketing airline puts its own airline identification code on flights that the other participating airline actually operates.
    * Online - An itinerary with a single marketing carrier on all segments
    * Interline - An itinerary with more than one marketing carrier, but the marketing carriers have agreements to work together for things like baggage transfer.
 * GDS - Global distribution system, such as Sabre or Travelport.
 * LCC - Low Cost Carrier. An airline focused on providing cheap tickets with as few comforts as possible
 * Segment - A segment, with some exception (hidden stops), corresponds to a single flight. One or more segments form a leg in a trip (A --> B), with one or more legs forming a complete trip
 * Shop - A shop corresponds to a request sent to a GDS for information about flights. Shops are an important signal of demand/offer for each trip.
 * Stops
    * Connection - A stop that requires a passenger to change planes before continuing to the ultimate destination.
    * Direct - A flight that makes one or more stops at an intermediate airport between the departure and destination airports, but keeps the same flight number and is unlikely to change planes. (adapted from Sabre)
    * Hidden - see Tech / Technical Stop
    * Leg - The flight segments comprising the journey from the passenger's starting point to their destination. May contain intermediate stops.
    * Marriage group - "Segments that must be processed as one unit, and are therefore moved, cancelled, and/or priced together" (from Sabre)
    * Nonstop - A flight that does not make any stops between the departure and destination airports.
    * Segment - A flight from an origin airport to a destination airport. Can refer to a single takeoff/landing or multiple ones. The grouping is usually determined by airline operational, marketing, or partnership reasons.
    * Slice - A Hopper term for "leg".
    * Tech / Technical - a stop (flight landing and subsequent takeoff) in a segment's flight for refuelling or other technical reasons. Planned technical stops usually don't involve changing planes.
 * Trip - A trip corresponds to the sum of flights linked to a single ticket. A trip can be round-trip (with two legs A --> B, B--> A), one-way (A --> B) or open-jaw (A-->B, C-->A) 

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

 A table of past and future flight schedules, including their seat capacities and codes in a long table format.

Usage caveats:

If a flight has codeshares, it will have a row for every flight number. E.g. if there is one codeshare, there will be two rows, one for the operating carrier number and another for the codeshare. Set codeshareIndicator = 0 to filter out codeshares to avoid duplicates

If a flight has a hidden stop, it will have a row for all consecutive combinations of segment combinations. E.g. CX888 appears 3 times as HKG-JFK, HKG-YVR, and YVR-JFK as there is a hidden stop in YVR. Set stops = 0 to filter out flights with hidden stops to avoid duplicates

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

### flight_trips

Itineraries received in response to requests by Hopper on the behalf of our users. A trip consist of 1 (if one-way), 2 (if round-trip or open-jaw) or more legs.
Each leg is formed by 1 or more segments, each usually corresponding to a flight.

`event.id` and `trip_index` together form a primary key that can be joined with `flight_segments`.

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
| `fare_total_usd` | `double` | Total ticket price in USD, including all taxes and fees |
| `fare_tax_usd` | `double` | Tax component of the ticket price |
| `fare_surcharge_usd` | `double` | Surcharge component (identically zero) |
| `fare_currency` | `string` | Currency the trip was originally priced in |
| `fare_total` | `double` | Total ticket price in original `currency` units |
| `fare_tax` | `double` | Tax amount in original currency |
| `fare_surcharge` | `double` | Surcharge in original currency |
| `fare_exchange_rate` | `double` | Exchange rate used for conversion to USD |
| `fare_pax_type` | `string` | Code for passenger type used for quote, typically ADT for adult |
| `fare_refundable` | `boolean` | Whether this ticket is refundable |
| `fare_point_of_sale_country_code` | `string` | Country code for point of sale where ticket was priced |
| `fare_validating_carrier` | `string` | Carrier code for the airline selling the ticket (not necessarily flying it) |
| `fare_conversation_id` | `string` | Unique identifier for the search in the source system |
| `outgoing_origin` | `string` | Three letter airport code like BOS for slice origination |
| `outgoing_destination` | `string` | Three letter code like YUL for slice destination |
| `outgoing_departure_odate` | `string` | Departure date in origin timezone in yyyy-mm-dd format |
| `outgoing_departure_ms` | `long` | Departure time in epoch millis |
| `outgoing_departure_day_of_week_mon1` | `integer` | Departing day of week in origin timezone, within Monday=1, Sunday=7 |
| `outgoing_departure_tz_offset_ms` | `long` | Timezone offset in millis for origin |
| `outgoing_departure_country_code` | `string` | Two letter ISO country code for origin |
| `outgoing_departure_subdivision_code` | `string` | Three letter ISO 3166-2 code for subdivision (e_g_ province or state) |
| `outgoing_departure_currency_code` | `string` | Three letter ISO currency code for origin |
| `outgoing_arrival_ddate` | `string` | Arrival date in destination timezone in yyyy-mm-dd format |
| `outgoing_arrival_ms` | `long` | Arrival time in epoch millis |
| `outgoing_arrival_day_of_week_mon1` | `integer` | Arrival day of week at destination |
| `outgoing_arrival_tz_offset_ms` | `long` | Timezone offset in millis at destination |
| `outgoing_arrival_country_code` | `string` |  |
| `outgoing_arrival_subdivision_code` | `string` |  |
| `outgoing_arrival_currency_code` | `string` |  |
| `outgoing_layovers` | `array` | List of layover airport codes |
| `outgoing_marketing_carriers` | `array` | List of marketing carriers, the airlines advertised to the customer, e_g_ via codeshare |
| `outgoing_operating_carriers` | `array` | List of operating carriers, the airlines that actually fly the plane |
| `outgoing_duration_minutes` | `integer` | Total length of travel (including layovers) in minutes |
| `outgoing_stops` | `integer` | Number of stops for the slice |
| `returning_origin` | `string` | Three letter airport code like BOS for slice origination |
| `returning_destination` | `string` | Three letter code like YUL for slice destination |
| `returning_departure_odate` | `string` | Departure date in origin timezone in yyyy-mm-dd format |
| `returning_departure_ms` | `long` | Departure time in epoch millis |
| `returning_departure_day_of_week_mon1` | `integer` | Departing day of week in origin timezone, within Monday=1, Sunday=7 |
| `returning_departure_tz_offset_ms` | `long` | Timezone offset in millis for origin |
| `returning_departure_country_code` | `string` | Two letter ISO country code for origin |
| `returning_departure_subdivision_code` | `string` |  |
| `returning_departure_currency_code` | `string` | Three letter ISO currency code for origin |
| `returning_arrival_ddate` | `string` | Arrival date in destination timezone in yyyy-mm-dd format |
| `returning_arrival_ms` | `long` | Arrival time in epoch millis |
| `returning_arrival_day_of_week_mon1` | `integer` | Arrival day of week at destination |
| `returning_arrival_tz_offset_ms` | `long` | Timezone offset in millis at destination |
| `returning_arrival_country_code` | `string` |  |
| `returning_arrival_subdivision_code` | `string` |  |
| `returning_arrival_currency_code` | `string` |  |
| `returning_layovers` | `array` | List of layover airport codes |
| `returning_marketing_carriers` | `array` | List of marketing carriers, the airlines advertised to the customer, e_g_ via codeshare |
| `returning_operating_carriers` | `array` | List of operating carriers, the airlines that actually fly the plane |
| `returning_duration_minutes` | `integer` | Total length of travel (including layovers) in minutes |
| `returning_stops` | `integer` | Number of stops for the slice |
| `query_origin_type` | `string` | Type for origin, either `airport` or `city` |
| `query_origin` | `string` | Origin code, e_g_ BOS or YMQ |
| `query_destination_type` | `string` |  |
| `query_destination` | `string` |  |
| `query_departure_date` | `string` | Departure date |
| `query_return_date` | `string` |  |
| `cities_origin` | `string` | Origin for outbound |
| `cities_destination` | `string` | Destination for outbound |
| `cities_return_origin` | `string` | Origin for returning (typically same as `destination`) |
| `cities_return_destination` | `string` | Destination for returning (typically same as `origin`) |
| `cities_same_origin` | `boolean` | Whether slices coincide at origin |
| `cities_same_destination` | `boolean` | Whether slices coincide at destination |
| `cities_is_roundtrip` | `boolean` |  |

### flight_segments

All segments within each trip of a shop, joinable with `flight_trips` using the combination of `trip_index` and `event.id` as a foreign key.
A segment corresponds, with some technical exceptions, to a single flight. One or more segments form the leg of a trip (e.g Montreal-Quito). One or more legs form a full trip.

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
| `code_shared_carrier` | `string` | Carrier code sharing the plane  |
| `fare_code` | `string` | Fare basis code for this segment |
| `carrier_cabin_class` | `string` | Cabin class according to the carrier |
| `hopper_cabin_class` | `string` | Standardized cabin class according to Hopper, one of E - Economy, EP - Premium Economy, B - Business, F - First, U - Unknown |
| `stops` | `integer` | Number of stops within this segment, sometimes not requiring deplaning |
| `available_seats` | `integer` | Nominally availability (0-9) for this segment in this fare class |
| `booking_code` | `string` | Fare bucket (A-Z) typically the first letter of the fare basis code |
| `received_date` | `date` | Received date in Hopper TZ (partition) |
| `trip_type` | `string` | Trip type (partition) |
| `event.source` | `string` | The shopping provider system that generated these search results |
| `cities.origin` | `string` |  |
| `cities.destination` | `string` |  |

### flight_shops

Subset of best trips from each shop. A shop corresponds to a request sent to a GDS for information about flights. Shops are an important signal of demand/offer for each trip.

**Partitioned By** : `received_date`, `trip_type`

| Columns | Data Type | Description |
|-|-|-|
| `origin` | `string` |  |
| `destination` | `string` |  |
| `outgoing_departure_odate` | `string` | Departure date in origin timezone in yyyy-mm-dd format |
| `departure_date` | `string` | Departure date in origin timezone in yyyy-mm-dd format |
| `outgoing.duration_minutes` | `integer` | Total length of travel (including layovers?) in minutes |
| `outgoing.departure_day_of_week` | `integer` | Departing day of week in origin timezone, within Monday=1, Sunday=7 |
| `returning.departure_odate` | `string` | Departure date in origin timezone in yyyy-mm-dd format |
| `returning.duration_minutes` | `integer` | Total length of travel (including layovers?) in minutes |
| `returning.departure_day_of_week` | `integer` | departure day of week at destination, monday being 1|
| `non_stop` | `boolean` | True if the trip does not include a lay-over |
| `total_usd` | `double` | Total ticket price in USD, including all taxes and fees |
| `num_trips` | `integer` | Number of trips for that particular shop |
| `advance` | `integer` | Days before trip, in origin timezone |
| `los` | `integer` | Number of nights stay involved in the trip, same day return is 0 |
| `includes_saturday_night_stay` | `boolean` | Does the trip include a Saturday night stay? |
| `source` | `string` | Source of the shop request (typically a GDS, either Sabre or Travelport) |
| `received_date` | `date` | Date the trip was received in Hopper TZ (partition) |
| `trip_type` | `string` | Type of trip, one of `one_way`, `round_trip`, `open_jaw` |
| `filter` | `filter` | filter buckets the trip is falling into. Should look like, for instance, And(ShortLayover,NoLCC), meaning "has a short layover and does not use a Low Cost Carrier |

# GCP bucket structure

All the available data can be found in the gs://travelhacks-datasets GCP bucket, which is located in the travelhacks-data project. This data is structure as follows:

/ --- common --- airports         # these tables are small, so you can safely use them as-is
            |--- hotel_geo_info   
            |--- flight_schedules
  --- raw_datasets # raw dataset (as parquet) for 2017-2019 (large tables, do not use directly)
  --- raw_datasets_large # raw dataset (as parquet) for 2018-2019  (large tables, do not use directly)
  --- day (single day dataslice)
  --- all_2_years # 2017-2019 dataslice
  --- all_1_year # 2018-2019 dataslice
  --- other dataslices ...
  --- ...

# List of data slices

We offer a series of subsets of our dataset, which are easier to digest and should be easier to use. 
In order to maximize the number of iterations, we recommend using one of these slices.

## Single Day
A single day of our data, with a 20% sampling rate. This is very close to an actual "day in the life" at Hopper, and is recommended to simulate real-time applications

## All 2017-2019
A sparse sample (.1%) of our data from june 2017 to july 2019. Useful for analysis and predictions.

## All 2018-2019
A less sparse (.5%) sample of our data, with all traffic from june 2018 to july 2019

## Montreal 2018-2019
A less sparse (.5%) sample of our data from june 2018 to july 2019, for all trips with YUL as origin or destination

## US Internal 2018-2019
A .5% sample of our data, from june 2018 to july 2019, with all U.S. internal traffic

## Canada Internal 2018-2019
A .5% sample of our data, from june 2017 to july 2019, with all Canadian internal traffic

## E.U.-Canada 2018-2019
A .5% sample of our data, from june 2017 to july 2019, with all trips Europe-->Canada or Canada-->Europe

## Single Origin 2017-2019
A .1% sample of our data, from june 2017 to july 2019, with JFK airport as the origin

# Resources

## Google Cloud tutorials and documentation

* [Qwiklabs: Google Developer Essentials](https://google.qwiklabs.com/quests/86?qlcampaign=5l-hack-23)
