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
# (Liest automatisch aus .streamlit/secrets.toml)
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
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. LOGIK: DATEN LADEN & SPEICHERN
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

def save_to_supabase(data_dict):
    """Speichert oder updated den Datensatz (Upsert)"""
    if not supabase: return False
    try:
        # Upsert funktioniert nur, wenn wir batch_id + tester_name als Unique Key in SQL definiert haben
        response = supabase.table("plantnex_tests").upsert(data_dict).execute()
        return True
    except Exception as e:
        st.error(f"Speicherfehler: {e}")
        return False

# ---------------------------------------------------------
# 3. ANLEITUNGS-TEXT (KORRIGIERT)
# ---------------------------------------------------------
def show_instructions():
    # ACHTUNG: Der folgende Text ist absichtlich ganz links am Rand,
    # damit die Formatierung im Browser korrekt angezeigt wird.
    st.markdown("""
<div class="instruction-box">
<h3>🧪 PLANTNEX BETA-TEST: KURZANLEITUNG</h3>
<p>Danke, dass du Teil der Test-Crew bist! Du hältst einen Prototypen ("Batch") unseres Bio-Superabsorbers in den Händen. Da es noch keine Verpackung gibt, befolge bitte genau diese Schritte:</p>
<p class="warning-text">⚠️ WARNUNG VORAB:</p>
<p>Das Granulat enthält echte <u>Pflanzenkohle</u>. Es kann stauben und färbt bei Nässe tiefschwarz.</p>
<ul>
<li>Bitte nicht über dem weißen Teppich öffnen.</li>
<li>Wir empfehlen Handschuhe oder vorsichtiges Arbeiten (lässt sich aber mit Seife abwaschen).</li>
</ul>
<h4>SCHRITT 1: DER GLAS-TEST (Pflicht für das Feedback!)</h4>
<p>Bevor du es der Pflanze gibst, müssen wir wissen, wie dieser spezielle Batch reagiert.</p>
<ul>
<li><strong>Nimm 1 gehäuften Teelöffel</strong> (ca. 5g) Granulat.</li>
<li>Gib es in ein durchsichtiges Glas (ca. 200ml).</li>
<li>Kippe das Glas voll mit Wasser.</li>
<li><strong>Wartezeit:</strong> Schau nach 30 Minuten und nach 2 Stunden nach.</li>
<li><strong>Beobachte:</strong> Wie viel ist es geworden? Wie fühlt es sich an (fest/weich)?</li>
</ul>
<p><em>(Diese Daten trägst du gleich unten in das Formular ein.)</em></p>
<h4>SCHRITT 2: AB IN DIE ERDE (Die Kür)</h4>
<p>Nach dem Messen kannst du das Produkt verwenden:</p>
<p><strong>🌱 Der "Profi-Weg" (Empfohlen):</strong><br>
Nimm den nassen "Gelee-Klumpen" aus deinem Test-Glas und mische ihn direkt unter die Erde im Wurzelbereich deiner Pflanze. Das ist der sofortige Wasserspeicher.</p>
<p><strong>⏱️ Der "Schnelle Weg":</strong><br>
Mische 1 Teelöffel trockenes Granulat unter die Erde und gieße sofort kräftig an, damit es aktiviert wird.</p>
<p><strong>Dosierung:</strong> 1 Teelöffel reicht für einen Standard-Topf (ca. 1 Liter Erde). Übertreibe es nicht – das Zeug hat Kraft!</p>
<hr style="border-color: #333; margin-top: 20px;">
<p style="text-align: center; color: #00FF41; font-weight: bold; font-size: 1.1em;">Bereit? Dann starte jetzt deinen Timer und das Formular! 🚀</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. HAUPTANWENDUNG
# ---------------------------------------------------------
def main():
    # --- ANLEITUNG OBEN ---
    show_instructions()

    # --- SESSION STATE INITIALISIERUNG ---
    default_keys = {
        "swelling_vol": 0, "swelling_time": 0, "rest_water": "Alles weg (Trocken)",
        "consistency": 3, "stickiness": "Angenehm feucht", "structure": "Körnig / Stückig (Gut)",
        "app_method": "Trocken einmischen", "dirty_hands": False, "elevator_effect": False,
        "comment": "", "logged_in": False
    }
    
    for key, val in default_keys.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # --- LOGIN BEREICH (Name & Charge) ---
    st.markdown("### 🔐 START / LOGIN")
    col1, col2 = st.columns(2)
    with col1:
        tester_name_input = st.text_input("OPERATOR NAME", placeholder="Kürzel / Vorname")
    with col2:
        batch_id_input = st.text_input("CHARGEN-NUMMER", placeholder="z.B. B005-X")

    # Button zum Laden/Starten
    if st.button("PROTOKOLL STARTEN / FORTSETZEN ➡️"):
        if not tester_name_input or not batch_id_input:
            st.error("❌ Bitte Name und Chargen-Nummer eingeben!")
        else:
            existing = load_existing_data(batch_id_input, tester_name_input)
            
            if existing:
                # Session State mit DB-Daten überschreiben
                st.session_state.swelling_vol = existing.get('swelling_vol', 0)
                st.session_state.swelling_time = existing.get('swelling_time', 0)
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

    # Stop, wenn nicht eingeloggt
    if not st.session_state.logged_in:
        st.stop()

    # -----------------------------------------------------
    # START FORMULAR
    # -----------------------------------------------------
    st.divider()
    st.markdown(f"**AKTIVE SITZUNG:** {tester_name_input} | Batch: {batch_id_input}")

    # --- A: GLAS TEST ---
    st.markdown("### A // GLAS TEST")
    
    # Timer Buttons (lokal)
    t1, t2 = st.columns(2)
    if t1.button("⏱️ 30 MINUTEN"): st.toast("Timer: 30 Min gestartet", icon="⏳")
    if t2.button("⏱️ 2 STUNDEN"): st.toast("Timer: 2 Std gestartet", icon="⏳")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # WICHTIG: Alle Widgets nutzen value=st.session_state.key
    vol = st.slider("Volumen im Glas (ml)", 0, 300, value=st.session_state.swelling_vol, key="input_vol")
    if 0 < vol < 30: st.error("⚠️ Zu wenig Volumen (Inaktiv)")

    dur = st.number_input("Dauer bis voll (Minuten)", min_value=0, value=st.session_state.swelling_time, key="input_dur")
    
    water_opts = ["Alles weg (Trocken)", "Leichter Film", "Pfütze", "Suppe (Schwimmt)"]
    idx_water = water_opts.index(st.session_state.rest_water) if st.session_state.rest_water in water_opts else 0
    rest = st.radio("Restwasser Status", water_opts, index=idx_water, horizontal=True, key="input_rest")

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
    
    if meth == "Vorgequollen (Nass)":
        st.warning("⚠️ HANDSCHUHE TRAGEN!")

    cc1, cc2 = st.columns(2)
    dirty = cc1.checkbox("Schwarze Hände?", value=st.session_state.dirty_hands, key="input_dirty")
    elevator = cc2.checkbox("Fahrstuhl-Effekt?", value=st.session_state.elevator_effect, key="input_elev")

    st.divider()
    
    # --- ABSCHLUSS ---
    comm = st.text_area("Kommentar / Freitext", value=st.session_state.comment, placeholder="Deine Beobachtungen...", key="input_comm")
    
    st.caption("Neues Foto hochladen (Optional):")
    uploaded_file = st.file_uploader("", type=['jpg', 'png'], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # SPEICHER BUTTON
    if st.button("💾 BERICHT ABSENDEN / AKTUALISIEREN"):
        # Daten sammeln
        img_str = "kein_bild"
        if uploaded_file:
            img_str = f"IMG_{batch_id_input}_{tester_name_input}"

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
        
        success = save_to_supabase(payload)
        
        if success:
            st.balloons()
            st.success("✅ DATEN GESPEICHERT! Du kannst die Seite schließen oder später weitermachen.")
            time.sleep(2)
            # Seite neu laden, um sicherzugehen, dass alles synchron ist
            st.rerun()

if __name__ == "__main__":
    main()
