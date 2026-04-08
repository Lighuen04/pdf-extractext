async def update_document_status(self, doc_id: str, status: str) -> bool:
    result = await self.collection.update_one(
        {"id": doc_id},
        {"$set": {"status": status}},
    )
    return result.modified_count > 0
