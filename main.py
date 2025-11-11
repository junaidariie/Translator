import streamlit as st
from transformers import pipeline, M2M100Tokenizer
import torch
import time

# Language names mapping
LANGUAGE_NAMES = {
    "fr": "French", "af": "Afrikaans", "am": "Amharic", "ar": "Arabic",
    "ast": "Asturian", "az": "Azerbaijani", "ba": "Bashkir", "be": "Belarusian",
    "bg": "Bulgarian", "bn": "Bengali", "br": "Breton", "bs": "Bosnian",
    "ca": "Catalan", "ceb": "Cebuano", "cs": "Czech", "cy": "Welsh",
    "da": "Danish", "de": "German", "el": "Greek", "en": "English",
    "eo": "Esperanto", "es": "Spanish", "et": "Estonian", "fa": "Persian",
    "ff": "Fulah", "fi": "Finnish", "fy": "Western Frisian", "ga": "Irish",
    "gd": "Scottish Gaelic", "gl": "Galician", "gu": "Gujarati", "ha": "Hausa",
    "he": "Hebrew", "hi": "Hindi", "hr": "Croatian", "ht": "Haitian Creole",
    "hu": "Hungarian", "hy": "Armenian", "id": "Indonesian", "ig": "Igbo",
    "ilo": "Iloko", "is": "Icelandic", "it": "Italian", "ja": "Japanese",
    "jv": "Javanese", "ka": "Georgian", "kk": "Kazakh", "km": "Central Khmer",
    "kn": "Kannada", "ko": "Korean", "lb": "Luxembourgish", "lg": "Ganda",
    "ln": "Lingala", "lo": "Lao", "lt": "Lithuanian", "lv": "Latvian",
    "mg": "Malagasy", "mk": "Macedonian", "ml": "Malayalam", "mn": "Mongolian",
    "mr": "Marathi", "ms": "Malay", "my": "Burmese", "ne": "Nepali",
    "nl": "Dutch", "no": "Norwegian", "ns": "Northern Sotho", "oc": "Occitan",
    "or": "Oriya", "pa": "Panjabi", "pl": "Polish", "ps": "Pushto",
    "pt": "Portuguese", "ro": "Romanian", "ru": "Russian", "sd": "Sindhi",
    "si": "Sinhala", "sk": "Slovak", "sl": "Slovenian", "so": "Somali",
    "sq": "Albanian", "sr": "Serbian", "ss": "Swati", "su": "Sundanese",
    "sv": "Swedish", "sw": "Swahili", "ta": "Tamil", "th": "Thai",
    "tl": "Tagalog", "tn": "Tswana", "tr": "Turkish", "uk": "Ukrainian",
    "ur": "Urdu", "uz": "Uzbek", "vi": "Vietnamese", "wo": "Wolof",
    "xh": "Xhosa", "yi": "Yiddish", "yo": "Yoruba", "zh": "Chinese",
    "zu": "Zulu"
}

# Custom CSS for bouncing loader and styling
st.markdown("""
<style>
    .loader-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    
    .bouncing-loader {
        display: flex;
        justify-content: center;
    }
    
    .bouncing-loader > div {
        width: 12px;
        height: 12px;
        margin: 3px 6px;
        border-radius: 50%;
        background-color: #4A90E2;
        opacity: 1;
        animation: bouncing-loader 0.6s infinite alternate;
    }
    
    .bouncing-loader > div:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .bouncing-loader > div:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes bouncing-loader {
        to {
            opacity: 0.3;
            transform: translateY(-16px);
        }
    }
    
    .translation-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .metric-container {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
    }
    
    .stTextArea textarea {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Cache the model loading
@st.cache_resource
def load_model():
    tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
    translator = pipeline(
        "translation",
        model="facebook/m2m100_418M",
        use_fast=True
    )
    return translator, tokenizer

def translate_text(text, src, tgt, translator):
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

def show_loader():
    return st.markdown("""
    <div class="loader-container">
        <div class="bouncing-loader">
            <div></div>
            <div></div>
            <div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main app
def main():
    st.set_page_config(
        page_title="M2M100 Translator",
        page_icon="🌍",
        layout="wide"
    )
    
    st.title("🌍 M2M100 Multilingual Translator")
    st.markdown("### Translate text between 100+ languages powered by Meta's M2M100 model")
    
    # Load model with progress indicator
    with st.spinner("Loading translation model..."):
        translator, tokenizer = load_model()
    
    # Create language display options
    lang_display = {f"{name} ({code})": code for code, name in LANGUAGE_NAMES.items()}
    lang_display_sorted = dict(sorted(lang_display.items()))
    
    # Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Source")
        src_lang_display = st.selectbox(
            "Source Language",
            options=list(lang_display_sorted.keys()),
            index=list(lang_display_sorted.values()).index("en")
        )
        src_lang = lang_display_sorted[src_lang_display]
        
        input_text = st.text_area(
            "Enter text to translate",
            height=200,
            placeholder="Type or paste your text here..."
        )
    
    with col2:
        st.subheader("🎯 Target")
        tgt_lang_display = st.selectbox(
            "Target Language",
            options=list(lang_display_sorted.keys()),
            index=list(lang_display_sorted.values()).index("es")
        )
        tgt_lang = lang_display_sorted[tgt_lang_display]
        
        output_placeholder = st.empty()
    
    # Translation button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        translate_btn = st.button("🔄 Translate", use_container_width=True, type="primary")
    
    # Perform translation
    if translate_btn:
        if not input_text.strip():
            st.warning("⚠️ Please enter some text to translate!")
        else:
            # Show loader
            loader_placeholder = st.empty()
            with loader_placeholder:
                show_loader()
            
            # Translate
            result = translate_text(input_text, src_lang, tgt_lang, translator)
            
            # Clear loader
            loader_placeholder.empty()
            
            # Display results
            with col2:
                st.markdown(f"""
                <div class="translation-box">
                    <h4>Translation Result:</h4>
                    <p style="font-size: 18px; line-height: 1.6;">{result['translation']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Show metrics
            st.markdown("---")
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.metric("⏱️ Inference Time", f"{result['inference_time_sec']}s")
            
            with metric_col2:
                st.metric("📊 Input Length", f"{len(input_text)} chars")
            
            with metric_col3:
                st.metric("📊 Output Length", f"{len(result['translation'])} chars")
            
            # Download button
            st.download_button(
                label="💾 Download Translation",
                data=result['translation'],
                file_name="translation.txt",
                mime="text/plain"
            )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>Powered by <b>facebook/m2m100_418M</b> • Supports 100+ languages</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()