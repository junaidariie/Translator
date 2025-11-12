from transformers import pipeline, M2M100Tokenizer
import torch, time



tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
SUPPORTED_LANGS = list(tokenizer.lang_code_to_id.keys())


def get_supported_languages():
    return SUPPORTED_LANGS

#-----------------  loading model ---------------------------
def load_model():
    try:
        translator = pipeline(
            "translation",
            model="facebook/m2m100_418M",
            use_fast=True
        )
        return translator
    except Exception  as e:
        return ("Error while loading the model", e)


# ------------------------ translator ---------------------------------------

def translate_text(translator, text, src:str, tgt:str):
    start = time.time()
    result = translator(text, src_lang=src, tgt_lang=tgt, max_length=100)
    elapsed = time.time() - start

    output = {
    "input_text": text,
    "source_language": src,
    "target_language": tgt,
    "translation": result[0]["translation_text"],
    "inference_time_sec": round(elapsed, 3)
            }
    return output

