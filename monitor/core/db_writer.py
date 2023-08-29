from typing import Dict, Any

import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


INFLUXDB_TOKEN = "Hhw8zbuj0BukaLT-0lAVgB2gfKUdT0a_FDBWd7AXuZUJeFQE7lg1HMAnaOi4lLHzXyZBhlY3rVKWFKkh3fEoVA=="
ORG = "a13"
BUCKET = 'test'
URL = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=URL, token=INFLUXDB_TOKEN, org=ORG)


def write(measurement_name: str,
          tags: Dict[str, Any],
          fields: Dict[str, Any],
          bucket: str = BUCKET,
          org: str = ORG,
          verbose: bool = False,
          ) -> None:

    write_api = client.write_api(write_options=SYNCHRONOUS)
    point = Point(measurement_name)

    for tag_key, tag_value in tags.items():
        point = point.tag(tag_key, tag_value)

    for field_key, field_value in fields.items():
        point = point.field(field_key, field_value)

    if verbose:
        print('writing...', point)
    try:
        write_api.write(bucket=bucket, org=org, record=point)
    except Exception as e:
        print(f"Failed to write to InfluxDB: {e}")


def read(measurement_name: str,
         bucket: str = BUCKET,
         org: str = ORG,
         ) -> None:
    query_api = client.query_api()
    query = """from(bucket: "{}")
         |> range(start: -10m)
         |> filter(fn: (r) => r._measurement == "{}")
         """.format(bucket, measurement_name)
    print(query)
    tables = query_api.query(query, org=org)

    for table in tables:
        for record in table.records:
            print(record)


if __name__ == "__main__":

    read(measurement_name='node_monitoring')

    # write(
    #     measurement_name='node_monitoring',
    #     tags={'name': 'node10'},
    #     fields={'cpu_usage': 0.1},
    #     verbose=True,
    # )