
import streamlit as st
import requests

st.set_page_config(page_title="القرآن الكريم", page_icon="📖", layout="wide")

st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Amiri', serif;
        background-color: #fefbf1;
        color: #1c1c1c;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        color: #136e4f;
        text-align: center;
    }
    .sourah-box {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    audio {
        width: 100%;
        margin-top: 10px;
    }
</style>""", unsafe_allow_html=True)

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Quran_Kareem.svg/2048px-Quran_Kareem.svg.png", width=150)
st.sidebar.title("📘 القائمة الجانبية")
menu = st.sidebar.radio("انتقل إلى:", ["الرئيسية", "السور", "البحث"])

st.title("📖 تطبيق القرآن الكريم")

if menu == "الرئيسية":
    st.subheader("🎙️ أفضل ١٠ قراء")
    reciteurs = [
        "عبد الباسط عبد الصمد", "مشاري العفاسي", "سعد الغامدي",
        "أحمد العجمي", "ماهر المعيقلي", "ياسر الدوسري",
        "محمد أيوب", "ناصر القطامي", "إدريس أبكر", "خالد القحطاني"
    ]
    st.write("\n".join([f"{i+1}. {reciteur}" for i, reciteur in enumerate(reciteurs)]))

elif menu == "البحث":
    mot_cle = st.text_input("🔍 ابحث عن كلمة أو سورة أو رقم آية")
    st.info("ميزة البحث سيتم تفعيلها قريبًا إن شاء الله.")

elif menu == "السور":
    st.subheader("🕋 قائمة السور")
    try:
        resp = requests.get("https://api.quran.com:443/v4/chapters?language=ar")
        sourates = resp.json().get("chapters", [])
    except:
        sourates = []

    for sourah in sourates:
        with st.expander(f"{sourah['id']}. {sourah['name_arabic']} - {sourah['translated_name']['name']}"):
            st.markdown(f"**عدد الآيات:** {sourah['verses_count']}")
            st.markdown(f"**مكان النزول:** {sourah['revelation_place']}")
            if st.button(f"📖 قراءة {sourah['name_arabic']}", key=f"btn_{sourah['id']}"):
                st.session_state['sourah_id'] = sourah['id']
                st.session_state['sourah_name'] = sourah['name_arabic']

    if 'sourah_id' in st.session_state:
        sid = st.session_state['sourah_id']
        sname = st.session_state.get('sourah_name', '')
        st.subheader(f"📜 {sname}")
        try:
            vresp = requests.get(f"https://api.quran.com:443/v4/quran/verses/uthmani?chapter_number={sid}")
            tafsir_resp = requests.get(f"https://api.quran.com:443/v4/quran/tafsirs/ar-muyassar?chapter_number={sid}")
            audio_resp = requests.get(f"https://api.quran.com:443/v4/chapter_recitations/7/{sid}")

            verses = vresp.json().get("verses", [])
            tafsirs = tafsir_resp.json().get("tafsirs", [])
            audio_url = audio_resp.json().get("audio_file", {}).get("audio_url", None)

            for v in verses:
                st.markdown(f"**الآية {v['verse_number']}**: {v['text_uthmani']}")
                tafsir = next((t['text'] for t in tafsirs if t['verse_key'].endswith(str(v['verse_number']))), None)
                if tafsir:
                    st.markdown(f"<div style='background:#f0f8ff;padding:10px;border-radius:8px'><b>تفسير:</b> {tafsir}</div>", unsafe_allow_html=True)

            if audio_url:
                st.audio(audio_url, format='audio/mp3')

        except Exception as e:
            st.error("لم يتم تحميل البيانات. حاول مرة أخرى.")

st.markdown("---")
st.caption("© تطبيق القرآن الكريم - تصميم عربي جميل 🌙")
