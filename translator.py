from transformers import pipeline, M2M100Tokenizer
import torch, time



tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
SUPPORTED_LANGS = list(tokenizer.lang_code_to_id.keys())


def get_supported_languages():
    return SUPPORTED_LANGS

#-----------------  loading model ---------------------------
translator = pipeline(
    "translation",
    model="facebook/m2m100_418M",
    use_fast=True
)


# ------------------------ translator ---------------------------------------

def translate_text(text, src:str, tgt:str):
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



"""
message = "what's going on hope u are doing good?"
output  = translate_text(message)

translation = output["translation"]
infrance_time = output["inference_time_sec"]

print(f"The translated text is {translation}, it took {infrance_time} to translate the text")"""