from hack.database.models import async_session
from hack.database.models import MessageHistory
from config import URL_API, QDRANT_API
from qdrant_client import QdrantClient



async def get_vec_db():
    qdrant = QdrantClient(
        url=URL_API,
        api_key=QDRANT_API,
    )
    return qdrant

async def save_message(user_id, username, message_text):
    async with async_session() as session:
        async with session.begin():
            message = MessageHistory(
                user_id=user_id,
                username=username,
                message_text=message_text
            )
            session.add(message)
