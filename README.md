# TravelHacks 2019

* [List of schemas](#List-of-schemas)
     * [production_internal_trips_10pct_v3](#production_internal_trips_10pct_v3)
     * [production_internal_segments_10pct_v3](#production_internal_segments_10pct_v3)
     * [airports_v9](#airports-v9)
     * [innovata_long](#innovata_long)
     * [geotables_hotel_metadata](#geotables_hotel_metadata)
     * [geotables_hotel_market_xref](#geotables_hotel_market_xref)
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

**Partitioned By** : `received_date`

| Columns | Data Type | Description |
|-|-|-|
| `date` | `date` | The date a flight is/was scheduled to fly. |
| `carrier` | `string` | The two or three letter code assigned by IATA or ICAO for the Carrier. |
| `flightnumber` | `string` | The flight number. |
| `serviceType` | `string` | The service type indicator is used to classify carriers according to the type of air service they provide. As specified in Appendix C of the IATA SSIM manual |
| `effectiveDate` | `string` | The effective date represents the date that the carrier has scheduled this flight service to begin. DD/MM/YYYY |
| `discontinuedDate` | `string` | The discontinued date represents the last date that the carrier has scheduled this flight service to operate. DD/MM/YYYY |
| `day1` | `string` | Indicates whether the flight has service on Monday. 0 = no  1 = yes |
| `day2` | `string` | Indicates whether the flight has service on Tuesday. 0 = no  1 = yes |
| `day3` | `string` | Indicates whether the flight has service on Wednesday. 0 = no  1 = yes |
| `day4` | `string` | Indicates whether the flight has service on Thursday. 0 = no  1 = yes |
| `day5` | `string` | Indicates whether the flight has service on Friday. 0 = no  1 = yes |
| `day6` | `string` | Indicates whether the flight has service on Saturday. 0 = no  1 = yes |
| `day7` | `string` | Indicates whether the flight has service on Sunday. 0 = no  1 = yes |
| `departureAirport` | `string` | The IATA airport code for the origin airport. |
| `departureCity` | `string` | The IATA metropolitan area code contains the city code for the point of trip origin. |
| `departureState` | `string` | Innovata State Code |
| `departureCountry` | `string` | The standard IATA Country code for the point of trip origin. |
| `departureTimePub` | `string` | The Published flight departure time. HH:MM:SS |
| `departureTimeActual` | `string` | The agreed SLOT departure time.  HH:MM:SS |
| `departureUTCVariance` | `string` | UTC Variant for the departure airport. +/- HHMM |
| `departureTerminal` | `string` | Departure terminal. |
| `arrivalAirport` | `string` | The standard IATA Airport code for the point of arrival. |
| `arrivalCity` | `string` | The arrival city code contains the city code for the point of trip origin. The city code could be used to display flight information for multiple airports/stations affiliated with the same city code. |
| `arrivalState` | `string` | Innovata State Code |
| `arrivalCountry` | `string` | The standard IATA Country code for the point of arrival. |
| `arrivalTimePub` | `string` | The Published flight arrival time.  HH:MM:SS |
| `arrivalTimeActual` | `string` | The agreed SLOT arrival time.  HH:MM:SS |
| `arrivalUTCVariance` | `string` | UTC Variant for the arrival airport.  + / - HHMM |
| `arrivalTerminal` | `string` | Departure terminal. |
| `subAircraftCode` | `string` | The sub aircraft type on the first leg of the flight.  (i.e. 763 = Boeing 767 300 series). |
| `groupAircraftCode` | `string` | The group aircraft type on the first leg of the flight.  (i.e. 767 = Boeing 767 series). |
| `classes` | `string` | Contains the most commonly used service classes (i.e. RFYC). |
| `classesFull` | `string` | Full list of Service Class descriptions. |
| `trafficRestriction` | `string` | As specified in Appendix G of the IATA SSIM manual. It may be found online. |
| `flightArrivalDayIndicator` | `string` | The arrival day indicator signifies which day the flight will arrive with respect to the origin depart day. <br>`blank` = arrives same day<br> -1 = Arrives the day before<br> +1 = Arrives the one day after<br> +2 = Arrives two days after |
| `stops` | `string` | The number of stops will be set to zero (i.e. nonstop) if the flight does not land between the point of origin and final destination |
| `stopCodes` | `string` | IATA airport codes where stops occur, separated by `!` (i.e. 2 stops = CDG!FRA) |
| `stopsubAircraftCodes` | `string` | Shows the sub-aircraft type on each leg of the flight. |
| `aircraftChangeIndicator` | `string` | The Aircraft change indicator signifies whether there has been an aircraft change at a stopover point for the flight leg.  (True / False) |
| `meals` | `string` | The meal codes field contains up to two meal codes per class of service. The meal codes are used by the airline industry to differentiate between the various food service types.  |
| `flightDistance` | `string` | The shortest distance (in miles) between the origin and destination points. |
| `elapsedTime` | `string` | The elapsed flight time is a calculation (in minutes) of the flight duration from the point of origin to the point of final destination (does not include layover times). |
| `layoverTime` | `string` | The layover time that indicates (in minutes) how much time will be spent on the ground during a flight stopover. |
| `inFlightService` | `string` | Standard IATA In-Flight Service codes. |
| `SSIMcodeShareCarrier` | `string` |  Alternate flight designator or ticket selling airline. Submitted by carriers on the SSIM Chapter 7 file record and linked to the Code Share Status data field. Note: The Codeshare Info flags (below) should be used whenever possible as this is populated with information submitted in the DEI10, DEI50 and DEI127 fields.  |
| `codeshareIndicator` | `string` | Flag that is set to true if the flight is operated by another carrier.  0 = no   1 = yes |
| `wetleaseIndicator` | `string` | Flag that is set to true if the flight is a wet lease.  A Wet Lease occurs when an aircraft is owned by one carrier and operated by another.  0 = no   1 = yes |
| `codeshareInfo` | `string` | Contains information regarding operating and marketing carriers.<br> e.g. AA1001 and QF1001 are marketed flights with the BA0001 operated flight.<br> For the AA1001 record, the Codeshare data field will be set to `Y` and the operating flight BA0001 will appear in this data field.<br> For the BA0001 entry, Codeshare will be set to `false`, and all the flights marketing BA001 will appear.  i.e. AA1001 /QF1001.<br> Multiple legs are separated by the `!` character. When number of stops is greater than 2, multiple logical legs are then separated by the `#` character.  |
| `wetleaseInfo` | `string` | Shows the actual owner of the aircraft |
| `operationalSuffix` | `string` | Flight number suffix as provided by carrier. |
| `ivi` | `string` | Itinerary Variation Identifier.  Used when linking back to a SSIM file for DEI information. |
| `leg` | `string` | Leg number.  Used when linking back to a SSIM file for DEI information. |
| `recordId` | `string` | Unique record indicator |
| `totalSeats` | `string` | The sum of all first class, business class, and economy class seats in the aircraft. Note: premium economy is treated as a subset of economy. |
| `firstClassSeats` | `string` | The number of first class seats in the aircraft. |
| `businessClassSeats` | `string` | The number of business class seats in the aircraft. |
| `premiumEconomyClassSeats` | `string` | The number of premium economy class seats in the aircraft. Note:  this is a subset of economy class and not used in the Total Seats calculation |
| `economyClassSeats` | `string` | The number of economy class seats in the aircraft (includes the number of premium economy class seats) |
| `received_date` | `date` | The date we received the final schedule for this flight. Rows with `received_dates` in the future may be subject to change. |

### hotel_geo_metadata

Basic metadata for hotels

| Columns | Data Type | Description |
|-|-|-|
| `geo_hotel_metadata_im_lodging_id` | `string` |  |
| `geo_hotel_metadata_im_name` | `string` |  |
| `geo_hotel_metadata_im_lat` | `double` |  |
| `geo_hotel_metadata_im_lon` | `double` |  |
| `geo_hotel_metadata_GiataID` | `long` |  |
| `geo_hotel_metadata_GiataName` | `string` |  |
| `geo_hotel_metadata_category_name` | `string` |  |
| `geo_hotel_metadata_GiataAddress` | `string` |  |
| `geo_hotel_metadata_GiataAccuracy` | `string` |  |


### internal_flight_trips

Itineraries received in response to requests by Hopper on the behalf of our users.

**Partitioned By** : `received_date`, `trip_type`

| Columns | Data Type | Description |
|-|-|-|
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
| `event.source` | `string` | The shopping provider system that generated these search results |
| `event.received_ms` | `long` | The timestamp we received these search results, in epoch millis |
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

All segments (legs) within each trip of a shop, joinable with `internal_flight_trips`.

**Partitioned By** : `received_date`, `trip_type`

| Columns | Data Type | Description |
|-|-|-|
| `trip_index` | `integer` | Index of this trip within the shop event |
| `segment_index` | `integer` | Index of this slice within the trip |
| `origin` | `string` | Origin airport for this slice |
| `destination` | `string` | Destination airport for this slice |
| `departure_ms` | `long` | Departure time in epoch millis |
| `arrival_ms` | `long` | Arrival time in epoch millis |
| `duration` | `integer` | Flight duration in minutes(?) |
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

* [Qwiklabs](TODO)
