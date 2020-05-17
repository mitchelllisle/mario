from mario.sinks.base import Sink
from pymongo import MongoClient
from pymongo.results import InsertOneResult
from typing import Dict, Optional


class MongoSink(Sink):
    """MongoSink
    Very basic Mongo connection and insert capability
    """
    def __init__(self, host: str, port: int, database: str = "mario", **kwargs):
        super().__init__(name="Mongo")
        self.client = MongoClient(host=host, port=port, **kwargs)
        self._database = self.client[database]

    def read(self, query: Dict, projections: Optional[Dict], collection: str = "executions"):
        _collection = self._database[collection]

        records = []
        for record in _collection.find(query, projections):
            records.append(record)
        return records

    def write(self, record: Dict, collection: str = "executions") -> InsertOneResult:
        _collection = self._database[collection]

        _collection.create_index("id")
        object_id = _collection.insert_one(record)
        return object_id
