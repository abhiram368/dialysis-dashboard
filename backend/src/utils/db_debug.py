from typing import Any, Dict
from ...src.data.database import db

async def get_db_structure() -> Dict[str, Any]:
    assert db.client is not None

    result = {}

    # list databases
    db_names = await db.client.list_database_names()

    for db_name in db_names:
        database = db.client[db_name]
        collections = await database.list_collection_names()

        result[db_name] = {}

        for col in collections:
            collection = database[col]

            # get one sample document
            sample = await collection.find_one()

            if sample:
                fields = list(sample.keys())
            else:
                fields = []

            result[db_name][col] = {
                "fields": fields,
                "sample": sample
            }

    return result