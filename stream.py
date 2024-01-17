from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import json
import requests


default_args = {
    "owner": "airscholar",
    "start_date": datetime(2024, 1, 17)
}

def get_data():
        result = requests.get("https://randomuser.me/api/").json()
        return result['results'][0]

def data_formatter(dataset):
      df = dict()
      location = dataset['location']

      df['first_name'] = dataset['name']['first']
      df['last_name'] = dataset['name']['last']
      df['gender'] = dataset['gender']
      df['location'] = f"{str(location['street']['number'])} {str(location['street']['name'])} {location['city']}"
      df['postcode'] = location['postcode']
      df['email'] = dataset['email']
      df['username'] = dataset['login']['username']

      df = json.dumps(df, indent=4)
      return df


def stream_data():
      result = data_formatter(get_data())
      print(result)

with DAG("user_automation",
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    streaming_task = PythonOperator(
            task_id = 'stram_data_from_api',
            python_callable=stream_data
    )

stream_data()
