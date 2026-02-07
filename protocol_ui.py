import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import time

# ---------------------------------------------------------
# 1. KONFIGURATION & SETUP
# ---------------------------------------------------------
st.set_page_config(
    page_title="PLANTNEX LAB",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Verbindung zu Supabase herstellen
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception:
        st.error("Fehler: Secrets nicht gefunden. Bitte Supabase URL/Key in secrets.toml eintragen.")
        return None

supabase = init_connection()

# CSS (Industrial Theme + UI Hiding + Styling für Anleitung)
st.markdown("""
    <style>
    /* UI Elemente verstecken */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Dark Industrial Theme */
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3, h4 { color: #FFFFFF !important; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Neon Green Accents */
    .stSlider [data-baseweb="slider"] div[role="slider"] { background-color: #00FF41 !important; }
    div.stButton > button {
        background-color: #1F2937; color: #00FF41; border: 1px solid #00FF41;
        width: 100%; padding: 15px 0px; font-weight: bold; transition: all 0.2s;
    }
    div.stButton > button:hover { background-color: #00FF41; color: #000000; }
    
    /* Radio Buttons größer machen für Touch */
    div[role="radiogroup"] > label {
        background-color: #161b22;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        border: 1px solid #333;
        width: 100%;
    }
    div[role="radiogroup"] > label:hover {
        border-color: #00FF41;
    }
    
    /* Anleitung Box Styling */
    .instruction-box {
        border: 1px solid #444;
        background-color: #161b22;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 25px;
        font-family: 'Arial', sans-serif;
        line-height: 1.6;
    }
    .instruction-box h3 { border-bottom: 1px solid #00FF41; padding-bottom: 10px; margin-bottom: 15px; }
    .instruction-box h4 { color: #00FF41 !important; margin-top: 20px; margin-bottom: 5px; }
    .instruction-box ul { padding-left: 20px; margin-bottom: 15px; }
    .instruction-box li { margin-bottom: 5px; }
    .warning-text { color: #FFD700; font-weight: bold; } /* Goldgelb für Warnungen */
    
    /* Info Box für den Speicher-Hinweis */
    .info-box {
        background-color: #0d211c;
        border-left: 4px solid #00FF41;
        padding: 10px;
        margin-bottom: 20px;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. LOGIK: DATEN LADEN, SPEICHERN & UPLOAD
# ---------------------------------------------------------

def load_existing_data(batch_id, tester_name):
    """Prüft, ob Eintrag existiert und lädt Daten in Session State"""
    if not supabase: return None
    try:
        response = supabase.table("plantnex_tests").select("*")\
            .eq("batch_id", batch_id)\
            .eq("tester_name", tester_name)\
            .execute()
        
        if response.data and len(response.data) > 0:
            data = response.data[0]
            st.toast("♻️ DATEN GEFUNDEN & GELADEN!", icon="💾")
            return data
        else:
            return None
    except Exception as e:
        st.error(f"Verbindungsfehler: {e}")
        return None

def upload_image(file, batch_id, tester_name):
    """Lädt das Bild in den Supabase Storage Bucket 'plantnex-fotos'"""
    if not supabase or not file: return None
    try:
        # Dateiname generieren: Batch_Name_Zeitstempel.jpg
        timestamp = int(time.time())
        file_ext = file.name.split('.')[-1]
        file_path = f"{batch_id}_{tester_name}_{timestamp}.{file_ext}"
        
        # Upload durchführen
        bucket_name = "plantnex-fotos"
        file_bytes = file.getvalue()
        
        supabase.storage.from_(bucket_name).upload(
            path=file_path,
            file=file_bytes,
            file_options={"content-type": file.type}
        )
        
        # Öffentliche URL abrufen
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
        return public_url
        
    except Exception as e:
        st.error(f"Bild-Upload Fehler: {e}")
        return None

def save_to_supabase(data_dict):
    """Speichert oder updated den Datensatz (Upsert)"""
    if not supabase: return False
    try:
        response = supabase.table("plantnex_tests").upsert(data_dict).execute()
        return True
    except Exception as e:
        st.error(f"Speicherfehler: {e}")
        return False

# ---------------------------------------------------------
# 3. ANLEITUNGS-TEXT
# ---------------------------------------------------------
def show_instructions():
    st.markdown("""
<div class="instruction-box">
<h3>🧪 PLANTNEX BETA-TEST: KURZANLEITUNG</h3>
<p>Danke, dass du Teil der Test-Crew bist! Du hältst einen Prototypen ("Batch") unseres Bio-Superabsorbers in den Händen. Da es noch keine Verpackung gibt, befolge bitte genau diese Schritte:</p>

<div class="info-box">
<strong>💡 WICHTIG ZUM ABLAUF:</strong><br>
Du kannst das Formular jederzeit schließen und später weitermachen (einfach mit gleichem Namen & Nummer wieder einloggen).<br>
<em>Idealerweise füllst du es aber erst aus, <strong>nachdem</strong> du die folgenden Experimente gestartet hast.</em>
</div>

<p class="warning-text">⚠️ WARNUNG VORAB:</p>
<p>Das Granulat enthält echte <u>Pflanzenkohle</u>. Es kann stauben und färbt bei Nässe tiefschwarz.</p>
<ul>
<li>Bitte nicht über dem weißen Teppich öffnen.</li>
<li>Wir empfehlen Handschuhe oder vorsichtiges Arbeiten.</li>
</ul>
<h4>SCHRITT 1: DER GLAS-TEST (Pflicht für das Feedback!)</h4>
<p>Bevor du es der Pflanze gibst, müssen wir wissen, wie dieser spezielle Batch reagiert.</p>
<ul>
<li><strong>Nimm 1 gehäuften Teelöffel</strong> (ca. 5g) Granulat.</li>
<li>Gib es in ein durchsichtiges Glas (ca. 200ml) und kippe Wasser dazu.</li>
<li><strong>Der Zeit-Check:</strong> Wir wollen wissen, wie es sich über Zeit verändert.</li>
<li>Schaue es dir z.B. nach <strong>30 Min</strong> oder <strong>2 Stunden</strong> an und trage deine Beobachtung unten ein.</li>
</ul>
<p><em>(Wähle unten einfach deinen aktuellen Mess-Zeitpunkt aus.)</em></p>
<h4>SCHRITT 2: AB IN DIE ERDE (Die Kür)</h4>
<p>Nach dem Messen kannst du das Produkt verwenden:</p>
<p><strong>🌱 Der "Profi-Weg" (Empfohlen):</strong><br>
Nimm den nassen "Gelee-Klumpen" aus deinem Test-Glas und mische ihn direkt unter die Erde im Wurzelbereich deiner Pflanze.</p>
<p><strong>⏱️ Der "Schnelle Weg":</strong><br>
Mische 1 Teelöffel trockenes Granulat unter die Erde und gieße sofort kräftig an.</p>
<p><strong>Dosierung:</strong> 1 Teelöffel reicht für einen Standard-Topf (ca. 1 Liter Erde).</p>
<hr style="border-color: #333; margin-top: 20px;">
<p style="text-align: center; color: #00FF41; font-weight: bold; font-size: 1.1em;">Bereit? Dann starte jetzt das Protokoll! 🚀</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. HAUPTANWENDUNG
# ---------------------------------------------------------
def main():
    show_instructions()

    # --- SESSION STATE INITIALISIERUNG ---
    default_keys = {
        "swelling_vol": 0, "swelling_time": 30, "rest_water": "Alles weg (Trocken)",
        "consistency": 3, "stickiness": "Angenehm feucht", "structure": "Körnig / Stückig (Gut)",
        "app_method": "Trocken einmischen", "dirty_hands": False, "elevator_effect": False,
        "comment": "", "logged_in": False
    }
    
    for key, val in default_keys.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # --- LOGIN ---
    st.markdown("### 🔐 START / LOGIN")
    col1, col2 = st.columns(2)
    with col1:
        tester_name_input = st.text_input("OPERATOR NAME", placeholder="Kürzel / Vorname")
    with col2:
        batch_id_input = st.text_input("CHARGEN-NUMMER", placeholder="z.B. B005-X")

    if st.button("PROTOKOLL STARTEN / FORTSETZEN ➡️"):
        if not tester_name_input or not batch_id_input:
            st.error("❌ Bitte Name und Chargen-Nummer eingeben!")
        else:
            existing = load_existing_data(batch_id_input, tester_name_input)
            if existing:
                st.session_state.swelling_vol = existing.get('swelling_vol', 0)
                st.session_state.swelling_time = existing.get('swelling_time', 30)
                st.session_state.rest_water = existing.get('rest_water', "Alles weg (Trocken)")
                st.session_state.consistency = existing.get('consistency', 3)
                st.session_state.stickiness = existing.get('stickiness', "Angenehm feucht")
                st.session_state.structure = existing.get('structure', "Körnig / Stückig (Gut)")
                st.session_state.app_method = existing.get('app_method', "Trocken einmischen")
                st.session_state.dirty_hands = existing.get('dirty_hands', False)
                st.session_state.elevator_effect = existing.get('elevator_effect', False)
                st.session_state.comment = existing.get('comment', "")
            
            st.session_state.logged_in = True
            st.rerun()

    if not st.session_state.logged_in:
        st.stop()

    # --- FORMULAR START ---
    st.divider()
    st.markdown(f"**AKTIVE SITZUNG:** {tester_name_input} | Batch: {batch_id_input}")

    # --- A: GLAS TEST ---
    st.markdown("### A // GLAS TEST")
    
    st.markdown("**1. Wann misst du gerade? (Zeitpunkt)**")
    time_mapping = {"Nach 30 Minuten": 30, "Nach 2 Stunden": 120, "Nach 24 Stunden (Langzeit)": 1440}
    stored_time = st.session_state.swelling_time
    default_idx = 0
    vals = list(time_mapping.values())
    if stored_time in vals: default_idx = vals.index(stored_time)

    selected_label = st.radio("Zeitpunkt wählen:", list(time_mapping.keys()), index=default_idx, label_visibility="collapsed", key="time_radio")
    dur = time_mapping[selected_label]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    vol = st.slider("2. Volumen im Glas (ml)", 0, 300, value=st.session_state.swelling_vol, key="input_vol")
    if 0 < vol < 30: st.error("⚠️ Zu wenig Volumen (Inaktiv)")

    st.markdown("**3. Restwasser Status**")
    water_opts = ["Alles weg (Trocken)", "Leichter Film", "Pfütze", "Suppe (Schwimmt)"]
    idx_water = water_opts.index(st.session_state.rest_water) if st.session_state.rest_water in water_opts else 0
    rest = st.radio("Restwasser Status", water_opts, index=idx_water, horizontal=True, key="input_rest", label_visibility="collapsed")

    st.divider()

    # --- B: HAPTIK ---
    st.markdown("### B // HAPTIK")
    cons = st.slider("Konsistenz (1=Schleim, 5=Hartgummi)", 1, 5, value=st.session_state.consistency, key="input_cons")
    if cons == 1: st.error("KRITISCHER FEHLER: SCHLEIM")
    
    c1, c2 = st.columns(2)
    stick_opts = ["Trocken / Krümelig", "Angenehm feucht", "Klebt leicht", "Klebt wie Honig"]
    idx_stick = stick_opts.index(st.session_state.stickiness) if st.session_state.stickiness in stick_opts else 1
    stick = c1.selectbox("Klebrigkeit", stick_opts, index=idx_stick, key="input_stick")
    
    struct_opts = ["Körnig / Stückig (Gut)", "Zerfällt sofort", "Matschig / Brei"]
    idx_struct = struct_opts.index(st.session_state.structure) if st.session_state.structure in struct_opts else 0
    struct = c2.selectbox("Struktur", struct_opts, index=idx_struct, key="input_struct")

    st.divider()

    # --- C: ANWENDUNG ---
    st.markdown("### C // ANWENDUNG")
    method_opts = ["Trocken einmischen", "Vorgequollen (Nass)"]
    idx_method = method_opts.index(st.session_state.app_method) if st.session_state.app_method in method_opts else 0
    meth = st.radio("Angewandte Methode", method_opts, index=idx_method, horizontal=True, key="input_meth")
    
    if meth == "Vorgequollen (Nass)": st.warning("⚠️ HANDSCHUHE TRAGEN!")

    cc1, cc2 = st.columns(2)
    dirty = cc1.checkbox("Schwarze Hände?", value=st.session_state.dirty_hands, key="input_dirty")
    elevator = cc2.checkbox("Fahrstuhl-Effekt?", value=st.session_state.elevator_effect, key="input_elev")

    st.divider()
    
    # --- ABSCHLUSS ---
    comm = st.text_area("Kommentar / Freitext", value=st.session_state.comment, placeholder="Deine Beobachtungen...", key="input_comm")
    
    st.caption("Neues Foto hochladen (Optional):")
    uploaded_file = st.file_uploader("", type=['jpg', 'png', 'jpeg'], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # SPEICHER BUTTON
    if st.button("💾 BERICHT ABSENDEN / AKTUALISIEREN"):
        with st.spinner("Speichere Daten & lade Bild hoch..."):
            
            # Bild Upload Logik
            image_url = None
            if uploaded_file:
                # Versuch das Bild hochzuladen
                image_url = upload_image(uploaded_file, batch_id_input, tester_name_input)
            
            # Daten zusammenstellen
            payload = {
                "batch_id": batch_id_input,
                "tester_name": tester_name_input,
                "swelling_vol": vol,
                "swelling_time": dur,
                "rest_water": rest,
                "consistency": cons,
                "stickiness": stick,
                "structure": struct,
                "app_method": meth,
                "dirty_hands": dirty,
                "elevator_effect": elevator,
                "comment": comm,
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Wenn ein Bild hochgeladen wurde, URL hinzufügen
            if image_url:
                payload["image_url"] = image_url

            success = save_to_supabase(payload)
            
            if success:
                st.balloons()
                st.success("✅ DATEN & BILD GESPEICHERT! Danke für das Feedback.")
                time.sleep(2)
                st.rerun()

if __name__ == "__main__":
    main()
