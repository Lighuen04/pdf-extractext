"""
MongoDB repository for document persistence.

Handles:
- Inserting documents into MongoDB
- Retrieving documents by ID
- Finding documents by checksum
- Error handling for database operations
"""

from __future__ import annotations

import os

from pymongo import MongoClient
from bson.objectid import ObjectId


class DocumentRepository:
    """Repository for MongoDB document persistence."""

    def __init__(self, mongo_client: MongoClient | None = None):
        """Initialize repository with MongoDB client.
        
        Args:
            mongo_client: MongoDB client instance. If None, uses environment config.
        """
        if mongo_client is None:
            mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
            mongo_client = MongoClient(mongo_uri)
        
        self.client = mongo_client
        database_name = os.getenv("MONGO_DB_NAME", "pdf_extractext")
        collection_name = os.getenv("MONGO_COLLECTION_NAME", "documents")

        self.db = mongo_client[database_name]
        self.collection = self.db[collection_name]

    def save_document(self, document: dict) -> ObjectId:
        """Save document to MongoDB.
        
        Args:
            document: Document dictionary to persist
            
        Returns:
            ObjectId of inserted document
        """
        result = self.collection.insert_one(document)
        return result.inserted_id

    def find_by_id(self, document_id: ObjectId) -> dict | None:
        """Find document by MongoDB ID.
        
        Args:
            document_id: ObjectId of the document
            
        Returns:
            Document dictionary if found, None otherwise
        """
        return self.collection.find_one({"_id": document_id})

    def find_by_checksum(self, checksum: str) -> dict | None:
        """Find document by file checksum.
        
        Args:
            checksum: SHA256 checksum value
            
        Returns:
            Document dictionary if found, None otherwise
        """
        return self.collection.find_one({"checksum_archivo": checksum})
