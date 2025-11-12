import streamlit as st
import html
from translator import load_model, translate_text  # only allowed imports

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

SUPPORTED_CODES = list(LANGUAGE_NAMES.keys())

st.set_page_config(page_title="Polyglot Translator", page_icon="🌍", layout="centered")

# ---------------------- THEME ----------------------
def inject_theme(theme):
    css = """
    <style>
      :root {
        --bg: #0d0f12;
        --card: rgba(255,255,255,0.06);
        --text: #e7e7e7;
        --muted: #a5a5a5;
        --accent: #8ab4ff;
        --border: 1px solid rgba(255,255,255,0.12);
        --output: rgba(255,255,255,0.10);
      }
      .light {
        --bg: #f7f8fc;
        --card: rgba(255,255,255,0.98);
        --text: #16181d;
        --muted: #52545a;
        --accent: #1d4ed8;
        --border: 1px solid rgba(0,0,0,0.08);
        --output: rgba(0,0,0,0.06);
      }
      body { background: var(--bg); }
      .wrap { background: var(--bg); padding:20px; border-radius:16px; }
      .box {
        background: var(--card);
        border: var(--border);
        border-radius: 14px;
        padding: 16px;
        backdrop-filter: blur(8px);
      }
      .output_box {
        background: var(--output);
        border: var(--border);
        border-radius: 14px;
        padding: 18px;
        margin-top:10px;
      }
      .title { font-size:2.2rem; font-weight:800; color:var(--text); }
      .muted { color:var(--muted); }
      .text { color:var(--text); font-size:1.2rem; }
      .dots{display:inline-flex; gap:5px; margin-top:6px;}
      .dot{
        width:8px; height:8px; border-radius:50%;
        background:var(--accent); animation:bounce 1.2s infinite;
      }
      .dot:nth-child(2){animation-delay:.15s}
      .dot:nth-child(3){animation-delay:.3s}
      @keyframes bounce{
        0%,80%,100%{transform:translateY(0);opacity:.6}
        40%{transform:translateY(-7px);opacity:1}
      }
    </style>
    """
    tclass = "" if theme=="Dark" else "light"
    st.markdown(css + f'<div class="wrap {tclass}">', unsafe_allow_html=True)

def close():
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------- UI ----------------------
theme_choice = st.radio("Theme", ["Dark","Light"], horizontal=True)
inject_theme(theme_choice)

st.markdown('<div class="title">🌍 Polyglot Translator</div>', unsafe_allow_html=True)
st.markdown('<p class="muted">M2M100 · 100+ languages</p>', unsafe_allow_html=True)


# ---------------------- MODEL LOAD WITH REMOVABLE LOADER ----------------------
model_placeholder = st.empty()

@st.cache_resource(show_spinner=False)
def get_model():
    return load_model()

if "translator" not in st.session_state:
    model_placeholder.markdown(
        """
        <div class="box">
            <span class="muted">Loading model...</span>
            <div class="dots">
                <div class="dot"></div><div class="dot"></div><div class="dot"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.session_state["translator"] = get_model()
    model_placeholder.empty()  # ✅ dots disappear after load


# ---------------------- INPUT ----------------------
sorted_names = sorted(LANGUAGE_NAMES.values())
src = st.selectbox("Source language", sorted_names, index=sorted_names.index("English"))
tgt = st.selectbox("Target language", sorted_names, index=sorted_names.index("Hindi"))
text = st.text_area("Enter text...", height=150)

name_to_code = {v:k for k,v in LANGUAGE_NAMES.items()}
src_code = name_to_code[src]
tgt_code = name_to_code[tgt]


# ---------------------- TRANSLATION WITH REMOVABLE LOADER ----------------------
if st.button("⚡ Translate", use_container_width=True):
    if not text.strip():
        st.warning("Enter text.")
    elif src_code == tgt_code:
        st.info("Languages are same.")
    else:
        translate_placeholder = st.empty()

        translate_placeholder.markdown(
            """
            <div class="box">
                <span class="muted">Translating...</span>
                <div class="dots">
                    <div class="dot"></div><div class="dot"></div><div class="dot"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        out = translate_text(st.session_state["translator"], text.strip(), src_code, tgt_code)

        translate_placeholder.empty()  # ✅ removes dots

        translated = html.escape(out["translation"])
        safe_copy = out["translation"].replace("'", "\\'").replace('"','\\"').replace("`","'")

        st.markdown(
            f"""
            <div class="output_box">
                <p class="muted">Result ({src} → {tgt}) • {out['inference_time_sec']}s</p>
                <p class="text">{translated}</p>
                <button class="box" onclick="navigator.clipboard.writeText('{safe_copy}')">📋 Copy</button>
            </div>
            """,
            unsafe_allow_html=True
        )

close()
