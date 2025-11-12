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

# Initialize session state for theme
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def get_theme_styles():
    if st.session_state.dark_mode:
        return """
        <style>
            .main {
                background-color: #1a1a2e;
                color: #eee;
            }
            
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
                background-color: #64b5f6;
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
            
            .header-container {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                padding: 30px;
                border-radius: 12px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            }
            
            .header-title {
                color: #fff;
                font-size: 36px;
                font-weight: 600;
                margin: 0;
                text-align: center;
            }
            
            .header-subtitle {
                color: #bdc3c7;
                font-size: 16px;
                text-align: center;
                margin-top: 10px;
            }
            
            .translation-card {
                background-color: #16213e;
                padding: 25px;
                border-radius: 12px;
                margin: 15px 0;
                border: 1px solid #2c3e50;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            }
            
            .translation-result {
                background-color: #0f3460;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #64b5f6;
                margin-top: 15px;
            }
            
            .result-text {
                font-size: 18px;
                line-height: 1.8;
                color: #eee;
            }
            
            .metric-box {
                background: linear-gradient(135deg, #2c3e50 0%, #3d5a80 100%);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 10px 0;
                border: 1px solid #34495e;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
            
            .metric-label {
                color: #bdc3c7;
                font-size: 14px;
                margin-bottom: 8px;
            }
            
            .metric-value {
                color: #64b5f6;
                font-size: 24px;
                font-weight: 600;
            }
            
            .footer {
                text-align: center;
                color: #95a5a6;
                padding: 25px;
                margin-top: 30px;
                border-top: 1px solid #34495e;
            }
            
            .theme-toggle {
                position: fixed;
                top: 80px;
                right: 20px;
                z-index: 999;
            }
            
            .stTextArea textarea {
                font-size: 16px;
                background-color: #16213e !important;
                color: #eee !important;
                border: 1px solid #34495e !important;
            }
        </style>
        """
    else:
        return """
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
                background-color: #3498db;
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
            
            .header-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 30px;
                border-radius: 12px;
                margin-bottom: 30px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }
            
            .header-title {
                color: #fff;
                font-size: 36px;
                font-weight: 600;
                margin: 0;
                text-align: center;
            }
            
            .header-subtitle {
                color: #f0f0f0;
                font-size: 16px;
                text-align: center;
                margin-top: 10px;
            }
            
            .translation-card {
                background-color: #ffffff;
                padding: 25px;
                border-radius: 12px;
                margin: 15px 0;
                border: 1px solid #e0e0e0;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            }
            
            .translation-result {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #667eea;
                margin-top: 15px;
            }
            
            .result-text {
                font-size: 18px;
                line-height: 1.8;
                color: #333;
            }
            
            .metric-box {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 10px 0;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            }
            
            .metric-label {
                color: #fff;
                font-size: 14px;
                margin-bottom: 8px;
                opacity: 0.9;
            }
            
            .metric-value {
                color: #fff;
                font-size: 24px;
                font-weight: 600;
            }
            
            .footer {
                text-align: center;
                color: #666;
                padding: 25px;
                margin-top: 30px;
                border-top: 1px solid #e0e0e0;
            }
            
            .theme-toggle {
                position: fixed;
                top: 80px;
                right: 20px;
                z-index: 999;
            }
            
            .stTextArea textarea {
                font-size: 16px;
            }
        </style>
        """

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
    
    # Apply theme styles
    st.markdown(get_theme_styles(), unsafe_allow_html=True)
    
    # Theme toggle button in sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
        theme_text = "Dark Mode" if not st.session_state.dark_mode else "Light Mode"
        
        if st.button(f"{theme_icon} Switch to {theme_text}", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 About")
        st.info("This app uses Meta's M2M100 model to translate between 100+ languages with high accuracy.")
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🌍 Multilingual Translator</h1>
        <p class="header-subtitle">Powered by Meta's M2M100 • Supporting 100+ Languages</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load model with progress indicator
    with st.spinner("🔄 Loading translation model..."):
        translator, tokenizer = load_model()
    
    # Create language display options
    lang_display = {f"{name} ({code})": code for code, name in LANGUAGE_NAMES.items()}
    lang_display_sorted = dict(sorted(lang_display.items()))
    
    # Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Source Text")
        src_lang_display = st.selectbox(
            "Source Language",
            options=list(lang_display_sorted.keys()),
            index=list(lang_display_sorted.values()).index("en"),
            key="src_lang"
        )
        src_lang = lang_display_sorted[src_lang_display]
        
        input_text = st.text_area(
            "Enter text to translate",
            height=250,
            placeholder="Type or paste your text here...",
            key="input_text"
        )
    
    with col2:
        st.markdown("### 🎯 Translation")
        tgt_lang_display = st.selectbox(
            "Target Language",
            options=list(lang_display_sorted.keys()),
            index=list(lang_display_sorted.values()).index("es"),
            key="tgt_lang"
        )
        tgt_lang = lang_display_sorted[tgt_lang_display]
        
        output_placeholder = st.empty()
    
    # Translation button
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        translate_btn = st.button("🔄 Translate Now", use_container_width=True, type="primary")
    
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
            st.markdown(f"""
            <div class="translation-result">
                <h4 style="margin-top: 0;">✨ Translation Result</h4>
                <p class="result-text">{result['translation']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show metrics
            st.markdown("<br>", unsafe_allow_html=True)
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">⏱️ Inference Time</div>
                    <div class="metric-value">{result['inference_time_sec']}s</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_col2:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">📊 Input Length</div>
                    <div class="metric-value">{len(input_text)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_col3:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">📊 Output Length</div>
                    <div class="metric-value">{len(result['translation'])}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Download button
            st.markdown("<br>", unsafe_allow_html=True)
            col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 1])
            with col_dl2:
                st.download_button(
                    label="💾 Download Translation",
                    data=result['translation'],
                    file_name="translation.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p><strong>M2M100 Translator</strong> • Built with Streamlit & Transformers</p>
        <p style="font-size: 14px; margin-top: 10px;">Model: facebook/m2m100_418M</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
