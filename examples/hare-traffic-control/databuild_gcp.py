'''
    Utility functions to create a dataset on GCP, populate it the flight segments,
    query it and save the result locally as JSON and avro
'''

from google.cloud import bigquery
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from datetime import datetime
from google.api_core.exceptions import Conflict
import json
import sys
import logging
from urllib.error import HTTPError
from urllib.request import urlopen, Request

# expects a timestamp as argument, representing the beginning of a 1-week slice of flight segments 
def query_gcp_flight_segments(start_time): 
    # Create a new Google BigQuery client using Google Cloud Platform project
    # defaults.
    client = bigquery.Client()

    dataset_id = initialize_dataset(client)

    add_to_dataset(client, dataset_id, 'flight_segments')

    # Configure the query job.
    job_config = bigquery.QueryJobConfig()
    job_config.use_legacy_sql = True

    # Set up a query in Standard SQL, which is the default for the BigQuery
    # Python client library.
    # The query selects the fields of interest.
    # Check the field mapping and update the query 

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    logging.info('** Pulling segments data **')

    query_string = '''
    select
        concat('_', origin, destination, CAST(departure_timestamp AS STRING), marketing_carrier, marketing_flightno) as segment_id,
        count(*) as pax,
        first(origin) as origin,
        first(destination) as destination,
        first(departure_timestamp) as departure_timestamp,
        first(arrival_timestamp) as arrival_timestamp,
        first(marketing_carrier) as marketing_carrier,
        first(marketing_flightno) as marketing_flightno
    from (
        select
            origin,
            destination,
            duration as duration_s,
            CAST(departure_ms/1000 AS INTEGER) as departure_timestamp,
            CAST(arrival_ms/1000 AS INTEGER) as arrival_timestamp,
            marketing_carrier as marketing_carrier,
            flight_number as marketing_flightno,
            operating_carrier as operating_carrier,
        from hackathon_dataset.flight_segments
        where 
            arrival_ms > {time_arg:d} * 1000
            and departure_ms < ({time_arg:d} + 7*24*60*60) * 1000
    )
    group by segment_id
    '''.format(time_arg=start_time)

    # Run the query.
    query_job = client.query(query_string, job_config=job_config)
    query_job.result()  # Waits for the query to finish

    segments_df = query_job.to_dataframe()

    logging.info('** Read {0} segments **'.format(segments_df.count()))

    return segments_df

source_format_dic = {
    'avro': bigquery.SourceFormat.AVRO,
    'parquet': bigquery.SourceFormat.PARQUET,
    'json': bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    'csv': bigquery.SourceFormat.CSV
}

def initialize_dataset(client):
    project = client.project
    dataset_id = f'hackathon_dataset'

    try:
        dataset = bigquery.Dataset(f"{project}.{dataset_id}")
        dataset = client.create_dataset(f'{project}.{dataset_id}')  # API request
        print('Created dataset {}.{}'.format(client.project, dataset.dataset_id))
    except Conflict:
        print('already created')

    return dataset_id

def table_exist(client, project_id, dataset_id, table_id):
  try:
    client.tables().get(
        projectId=project_id, 
        datasetId=dataset_id,
        tableId=table_id).execute()
    return True
  except HTTPError as err:
    if err.resp.status != 404:
       raise
    return False

def add_to_dataset(client, dataset_id, table_name):
    table_uri = 'gs://travelhacks-datasets/all_2017_2019/flight_segments/*.avro'
    table_id = table_name

    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.source_format = bigquery.SourceFormat.AVRO

    dataset_ref = client.dataset(dataset_id)

    load_job = client.load_table_from_uri(
        table_uri, dataset_ref.table(table_id), job_config=job_config
    )  # API request
    print('Starting job {}'.format(load_job.job_id))

    load_job.result()  # Waits for table load to complete.
    print('Job finished.')

    destination_table = client.get_table(dataset_ref.table(table_id))
    print('Loaded {} rows.'.format(destination_table.num_rows))
