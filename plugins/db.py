# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import motor.motor_asyncio

# Don't Remove Credit Tg - @VJ_Botz

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    async def connect(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.uri)
        self.db = self.client[self.db_name]

    async def close(self):
        if self.client:
            self.client.close()

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    async def add_file(self, collection_name: str, file_id):
        collection = self.get_collection(collection_name)
        file = {"file_id": file_id}
        return await collection.insert_one(file)

    async def is_file_exist(self, collection_name: str, file_id):
        collection = self.get_collection(collection_name)
        f = await collection.find_one({"file_id": file_id})
        return bool(f)

    async def get_all_files(self, collection_name: str):
        collection = self.get_collection(collection_name)
        return collection.find({})

    async def drop_all(self, collection_name: str):
        collection = self.get_collection(collection_name)
        return await collection.drop()

# Example usage to connect to a user's custom DB and collection
async def connect_user_db(user_id, uri, chat):
    chat = f"{user_id}{chat}"
    dbname = f"{user_id}-Forward-Bot"
    db = MongoDB(uri, dbname)
    try:
        await db.connect()
    except Exception as e:
        print(f"Connection error: {e}")
        return False, db
    return True, db