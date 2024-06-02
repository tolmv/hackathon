from config import EMBEDDING_MODEL, URL_API, QDRANT_API
from aiogram import Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
import hack.database.requests as rq
import openai
from openai import OpenAI
from qdrant_client import QdrantClient



prompt = """You are an assistant who looks at a question and several suitable answers in 3-4 sentences MAX to that question.ANSWER ON LANGUAGE FROM [QUESTIONS]. Your task is to CAREFULLY analyze them and give your answer based on those answers. Question: [Question]
  Asnwer from Document: [Document] """

router = Router()



@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет, " + message.from_user.first_name + "! Как я могу тебе помочь?")


@router.message(Command("help"))
async def send_help(message: Message):
    await message.answer("Я здесь, чтобы помочь! Вот что я умею:\n/start - начать диалог\n/help - помощь")


@router.message()
async def answer(message: Message):
    if message.text is not None:
        await rq.save_message(message.from_user.id, message.from_user.username, message.text)
        await message.answer(chatgpt(message.text))


def chatgpt(message: str) -> str:
    client = OpenAI()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "assistant",
                "content": prompt.replace('[Document]', query_qdrant(message)).replace("[Question]", message)
            }
        ],
        model="gpt-4")
    return chat_completion.choices[0].message.content


def query_qdrant(message):
    embedded_query = openai.embeddings.create(
        input=message,
        model=EMBEDDING_MODEL,
    ).data[0].embedding  # We take the first embedding from the list
    qdrant = QdrantClient(
        url=URL_API,
        api_key=QDRANT_API)

    query_results = qdrant.search(
        collection_name='Articles',
        query_vector=(
            'vector', embedded_query
        ),
        limit=5,
        query_filter=None
    )
    res = []
    for i, article in enumerate(query_results):
        res.append(f'{i + 1}. {article.payload["content"]}')
    return ' '.join(res)
