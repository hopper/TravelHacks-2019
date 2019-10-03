# TravelHacks 2019

* [Glossary](#Glossary)
* [List of schemas](#List-of-schemas)
     * [flight_airports](#flight_airports)
     * [flight_schedules](#flight_schedules)
     * [hotel_geo_metadata](#hotel_geo_metadata)
     * [flight_trips](#flight_trips)
     * [flight_segments](#flight_segments)
* [Getting Started](#Getting-Started)
* [Resources](#resources)
    * [Google Cloud tutorials and documentation](#Google-Cloud-tutorials-and-documentation)

## Glossary

See also [ATPCO's glossary](https://www.atpco.net/glossary).

 * ARC - The settlement plan for the United States.
 * Airline types
    * Disclosure - "For airline companies that have a code sharing agreement, the airline that operates the flight." (from Sabre)
    * Marketing - The carrier that sells a flight.
    * Operating - "The airline company or carrier that operates a flight. When a consumer requests an itinerary, the DOT requires the disclosure of the identity of the operating carrier by corporate name in any schedule that is displayed in a response." (abbreviated from Sabre)
    * Plating - a synonym for validating, used by Travelport in particular.
    * Validating - The carrier that collects payment, issues tickets, and distributes payment to any other carriers in the reservation. A Hopper user doesn't know this carrier unless they are issued travel credit for a cancellation. If the carriers in a reservation don't have an interline agreement, there are multiple validating carriers.
    * Primary - defined and used only internally at Hopper. For a slice, a primary carrier is the marketing carrier of the longest segment. For a trip, a primary carrier is the primary carrier of the first slice. We have multiple primary carriers for a trip only if a booking is multi tickets (a.k.a. hacker fares).
 * Authorization - A hold of funds on a credit card account. The actual transfer of funds doesn't occur until the authorization is captured. If an authorization is not captured within some time (around 7 days), it is automatically voided.
 * Booking - The exact scope can vary by context but it generally refers to the process of pricing, checking availability, reserving seats, transmitting passenger information, and other actions required to complete a reservation.
 * BSP - Business Settlement Plan. The type of settlement used everywhere except the United States. Each BSP country has its own rules, but operates relatively similarly.
 * Capture - Initiates the transfer of funds set aside by the authorization.
 * Codeshare - An agreement between two airlines in which the marketing airline puts its own airline identification code on flights that the other participating airline actually operates.
    * Online - An itinerary with a single marketing carrier on all segments
    * Interline - An itinerary with more than one marketing carrier, but the marketing carriers have agreements to work together for things like baggage transfer.
 * Consolidator - An agency that has access to better fares for some airlines, routes, and travel dates. A consolidator might provide ticketing in a situation where Hopper cannot ticket, such as before Hopper is accredited in a point of sale or if an airline hasn't granted ticketing rights to Hopper yet.
 * Fares
    * Account code - A short identifier that provides access to different fares when making a price quote in the GDS. For example, we use HOP to identify Hopper commissionable fares.
    * Base - The fare in the currency of the origin.
    * Booking class -
    * [Channel-private](https://docs.google.com/document/d/1Rorz9gW8TsNgQfPjZ1cKoZ2O8BD4491ACQ15CEgD7pU/edit) - non-negotiated yet nominally private fares. They are typically intended for distribution by OTAs but not traditional travel agencies. An important assumption of channel-private fares is that they are fine to display alongside public fares in public flight lists.
     (In technical terms, channel-private fares are [filed with Cat 15 but not Cat 25 or 35](http://archive.is/yENbx).)
    * Commission - Typically refers to money paid to an agency by an airline out of the cost of the ticket.
    * Equivalent - The fare in the currency of the point of sale when the base fare is in a different currency.
    * Fare basis code - An identifier for a set of fare rules.
    * Markup - An amount the agency adds to the price the airline charges, usually in the context of a net fare.
    * Net - A negotiated fare whose price is below the published price. Travel agencies can sell it at or slightly below the published price, pocketing the difference.
    * Private - A fare with restrictions on distribution or ticketing. Includes commissions and nets. Includes negotiated fares and channel-private fares. Airlines use these to reward or incentivize high-volume partners, and to offer flash sales without triggering price wars (since in principle airlines don't have access to their competitors' private fares).
    * Public / published - A fare available to all consumers.
 * GDS - Global distribution system, such as Sabre or Travelport.
 * Post-booking - anything that happens after the reservation is created.
 * Post-ticketing - anything that happens after a ticket is issued.
 * Shop -
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
 * Supplier - Supplies the inventory for sale on a provider (GDS). Suppliers are the airlines (that sell fares) and hotels (that sell rooms).
 * Ticketing - The process of collecting payment for airfare through a settlement agency (ARC or BSP).

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

### flight_trips

Itineraries received in response to requests by Hopper on the behalf of our users.

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
| `fare.total_usd` | `double` | Total ticket price in USD, including all taxes and fees |
| `fare.tax_usd` | `double` | Tax component of the ticket price |
| `fare.surcharge_usd` | `double` | Surcharge component (identically zero) |
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
| `outgoing.duration_minutes` | `integer` | Total length of travel (including layovers) in minutes |
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

### flight_segments

All segments (legs) within each trip of a shop, joinable with `flight_trips` using the combination of `trip_index` and `event.id` as a foreign key.

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

# Getting Started

* The captain of the team should receive an invite e-mail, which will provide access to the TravelHacks GCP organization
* The captain should then create a project for the team, following instructions [here](https://cloud.google.com/resource-manager/docs/creating-managing-projects)
* From that point there are several possible options to the team
* It is likely that you will want to run code locally using the GCP API, which will require valid credentials. In that case, see next section

## Using GCP Credentials locally

* Create a service account for your project, and give it the correct permissions [give it the correct permissions](https://cloud.google.com/iam/docs/creating-managing-service-accounts)
* Download the service account's credential json (this should be an available option when creating the service account)
* Export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials/json
* You should now be able to use the GCP API with any of their available clients

# Resources

## Google Cloud tutorials and documentation

* [Qwiklabs: Google Developer Essentials](https://google.qwiklabs.com/quests/86?qlcampaign=5l-hack-23)
