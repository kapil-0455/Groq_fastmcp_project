from fastapi import APIRouter
from app.llm.groq_local import ask_local
from app.llm.groq_remote import ask_remote
from app.schemas import AskRequest, AskResponse

router = APIRouter()


@router.get('/health')
def health():
    return {'ok': True}


@router.post('/ask/local', response_model=AskResponse)
async def ask_local_route(body: AskRequest):
    return AskResponse(answer=await ask_local(body.question))


# Plain def: FastAPI runs it in a threadpool, so the sync OpenAI client is fine.
@router.post('/ask/remote', response_model=AskResponse)
def ask_remote_route(body: AskRequest):
    return AskResponse(answer=ask_remote(body.question))
