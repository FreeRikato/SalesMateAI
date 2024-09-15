from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import Generator
import time
from output import generate_markdown_output

app = FastAPI()

@app.get("/stream-markdown")
def stream_markdown():
    def markdown_streamer() -> Generator[str, None, None]:
        for markdown_chunk in generate_markdown_output():
            yield markdown_chunk
            time.sleep(1)  # Simulate a delay between outputs

    return StreamingResponse(markdown_streamer(), media_type="text/markdown")
