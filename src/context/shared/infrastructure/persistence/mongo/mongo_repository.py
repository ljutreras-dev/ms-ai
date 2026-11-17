from typing import Any, Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from src.context.shared.infrastructure.persistence.mongo.mongo_client_factory import MongoClientFactory


class MongoRepository:
    """
    Base generic Mongo repository mirroring MongoRepository from the Node.js Clean Architecture.
    Provides async helpers to persist, query, and manage documents in MongoDB collections.
    """

    def __init__(self, client_factory: MongoClientFactory, database_name: Optional[str] = None) -> None:
        self._client_factory = client_factory
        self._database_name = database_name

    async def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        """Retrieves an asynchronous collection handle."""
        db = await self._client_factory.get_database(self._database_name)
        return db[collection_name]

    async def persist(self, collection_name: str, doc_id: str, document: Dict[str, Any]) -> None:
        """Upserts a document by its '_id'."""
        collection = await self.get_collection(collection_name)
        await collection.update_one(
            {"_id": doc_id},
            {"$set": document},
            upsert=True,
        )

    async def find_by_id(self, collection_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Finds a single document by its '_id'."""
        collection = await self.get_collection(collection_name)
        return await collection.find_one({"_id": doc_id})

    async def find(
        self,
        collection_name: str,
        query: Dict[str, Any],
        limit: int = 50,
        sort_by: Optional[str] = None,
        sort_order: int = 1,
    ) -> List[Dict[str, Any]]:
        """Finds multiple documents with optional sorting and limit."""
        collection = await self.get_collection(collection_name)
        cursor = collection.find(query)
        if sort_by:
            cursor = cursor.sort(sort_by, sort_order)
        cursor = cursor.limit(limit)
        return await cursor.to_list(length=limit)

    async def delete_by_id(self, collection_name: str, doc_id: str) -> bool:
        """Deletes a document by its '_id'."""
        collection = await self.get_collection(collection_name)
        result = await collection.delete_one({"_id": doc_id})
        return result.deleted_count > 0
