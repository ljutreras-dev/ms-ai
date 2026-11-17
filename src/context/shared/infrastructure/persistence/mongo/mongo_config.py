from dataclasses import dataclass


@dataclass
class MongoConfig:
    """Configuration parameters for MongoDB connection."""

    uri: str
    database_name: str
    server_selection_timeout_ms: int = 5000
