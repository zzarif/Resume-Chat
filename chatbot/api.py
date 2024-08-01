from fastapi import FastAPI, File, UploadFile
from docs.vectorizer import save_doc_to_vector_store
from chatbot.streamer import stream_response
from fastapi.responses import StreamingResponse
from fastapi import status, HTTPException
import uvicorn


app = FastAPI()


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if save_doc_to_vector_store(file):
        return {'filename': file.filename}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'File {file.filename} could not be vectorized.',
        )


@app.post("/chat")
async def chat(query: str):
    return StreamingResponse(stream_response(query), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000)
