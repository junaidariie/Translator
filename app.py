from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, M2M100Tokenizer
from translator import translate_text,get_supported_languages, SUPPORTED_LANGS
import asyncio

app = FastAPI(title="translator")


class Input_schema(BaseModel):
    message : str
    src_lng : str
    tgt_lng : str


class Output_schema(BaseModel):
    input_text          : str
    source_language     : str
    target_language     : str
    translation         : str
    inference_time_sec  : float


@app.get("/")
def home():
    return {"message" : "The translator api is live now...!"}

@app.get("/supported_languages")
def supported_languages():
    try:
        return {"supported_languages" : get_supported_languages()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/translate", response_model=Output_schema)
async def translate(input_data: Input_schema):
    try:
        if input_data.src_lng not in SUPPORTED_LANGS:
            raise HTTPException(400, f"Unsupported source language: {input_data.src_lng}")
        if input_data.tgt_lng not in SUPPORTED_LANGS:
            raise HTTPException(400, f"Unsupported target language: {input_data.tgt_lng}")
        if input_data.src_lng == input_data.tgt_lng:
            raise HTTPException(400, "Source and target languages must differ.")
        
        result = await asyncio.to_thread(
            translate_text, input_data.message, input_data.src_lng, input_data.tgt_lng
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))