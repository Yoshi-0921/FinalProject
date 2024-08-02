import requests
from cachetools import TTLCache, cached


@cached(cache=TTLCache(maxsize=1024, ttl=86400))
def get_server_database_schema():
    url = "http://127.0.0.1:5000/openai/database/schema"
    headers = {"Content-Type": "application/json"}
    database_schema_response = requests.get(url, headers=headers).json()
    database_schema_dict = database_schema_response.get("schema")
    database_schema_string = "\n".join(
        [
            f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
            for table in database_schema_dict
        ]
    )
    print(database_schema_string)
    return database_schema_string
