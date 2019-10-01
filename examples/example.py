from google.cloud import bigquery
client = bigquery.Client()

datasets = list(client.list_datasets())
project = client.project

if datasets:
    print("Datasets in project {}:".format(project))
    for dataset in datasets:  # API request(s)
        print("\t{}".format(dataset.dataset_id))
else:
    print("{} project does not contain any datasets.".format(project))

dataset_id = "hackathon_dataset"

print(f"dataset ids: {[d.dataset_id for d in datasets]}")

if dataset_id in [d.dataset_id for d in datasets]:
    print("Already created")
else:     
    # Construct a full Dataset object to send to the API.
    dataset = bigquery.Dataset(dataset_id)

    dataset = client.create_dataset(dataset)  # API request
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

#Read Airports avro file and append to dataset

airports_uri = "gs://hackathon-mtl-2019/avro/flight_airports.avro/*"
airport_table_id = "flight_airports"

job_config = bigquery.LoadJobConfig()
job_config.autodetect = True
job_config.source_format = bigquery.SourceFormat.AVRO

dataset_ref = client.dataset(dataset_id)

print(f"existing table: {list(client.list_tables(dataset_id))}")

load_job = client.load_table_from_uri(
    airports_uri, dataset_ref.table(airport_table_id), job_config=job_config
)  # API request
print("Starting job {}".format(load_job.job_id))

load_job.result()  # Waits for table load to complete.
print("Job finished.")

destination_table = client.get_table(dataset_ref.table(airport_table_id))
print("Loaded {} rows.".format(destination_table.num_rows))






