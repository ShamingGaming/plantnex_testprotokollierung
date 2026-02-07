import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time

# ---------------------------------------------------------
# 1. KONFIGURATION & STYLING (THE VIBE)
# ---------------------------------------------------------
st.set_page_config(
    page_title="PLANTNEX | LAB",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS für den "Dark Industrial / Cyberpunk" Look
st.markdown("""
    <style>
    /* Main Background & Text */
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    
    /* Headers - Industrial Font Style */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Primary Highlights (Neon Green) */
    .stSlider [data-baseweb="slider"] div[role="slider"] {
        background-color: #39FF14 !important;
    }
    .stSlider div[data-testid="stMarkdownContainer"] p {
        color: #39FF14; 
        font-weight: bold;
    }
    
    /* Buttons (Big & Bold) */
    div.stButton > button {
        background-color: #1E1E1E;
        color: #39FF14;
        border: 1px solid #39FF14;
        border-radius: 0px; /* Industrial corners */
        padding: 15px 20px;
        font-size: 18px;
        width: 100%;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #39FF14;
        color: #000000;
        box-shadow: 0 0 15px #39FF14;
    }

    /* Alert Boxes */
    div[data-baseweb="notification"] {
        border-left: 5px solid #39FF14;
        background-color: #1E1E1E;
    }
    </style>
    """, unsafe_allow_html=True)

# Dateiname
DATA_FILE = "plantnex_feedback.csv"

# ---------------------------------------------------------
# 2. HILFSFUNKTIONEN
# ---------------------------------------------------------
def save_feedback(data_dict):
    """Speichert Daten + Metadaten in CSV"""
    df_new = pd.DataFrame([data_dict])
    
    if not os.path.isfile(DATA_FILE):
        df_new.to_csv(DATA_FILE, index=False)
    else:
        df_new.to_csv(DATA_FILE, mode='a', header=False, index=False)

def check_password():
    """Simulierter Login für Tester (Optional)"""
    # Hier vereinfacht: Wir nehmen die ID aus der URL oder Input
    return True

# ---------------------------------------------------------
# 3. UI KOMPONENTEN
# ---------------------------------------------------------
def main():
    # --- HEADER ---
    st.title("PLANTNEX // BETA LAB")
    st.markdown("### SYSTEM STATUS: ONLINE 🟢")
    st.divider()

    # --- SETUP ---
    # URL Parameter lesen (?id=Max -> id="Max") oder Fallback
    query_params = st.query_params
    default_user = query_params.get("id", "")
    
    col1, col2 = st.columns(2)
    with col1:
        tester_name = st.text_input("OPERATOR NAME", value=default_user, placeholder="Dein Name")
    with col2:
        # Wichtig: Dropdown oder Text für Batch ID
        batch_id = st.text_input("BATCH ID", placeholder="z.B. B001-HD", help="Steht auf dem Beutel")

    if not batch_id:
        st.warning("⚠️ BATCH ID EINGEBEN UM ZU STARTEN")
        st.stop() # Stoppt hier, bis Batch ID da ist

    # -----------------------------------------------------
    # SZENARIO A: GLAS TEST
    # -----------------------------------------------------
    st.markdown("## A // GLAS TEST (QUANTITATIV)")
    st.info("ℹ️ 1 TL (5g) Granulat + 200ml Wasser mischen.")

    # --- Tool: Timer ---
    with st.expander("⏱️ LABOR TIMER ÖFFNEN", expanded=False):
        t_col1, t_col2, t_col3 = st.columns(3)
        if t_col1.button("15 MIN"):
            with st.spinner("Timer läuft: 15 min..."):
                time.sleep(1) # Nur Demo, echter Sleep blockiert UI zu sehr
                st.toast("Timer gestartet (Demo)", icon="⏱️")
        if t_col2.button("30 MIN"):
             st.toast("30 Min Timer aktiv", icon="⏱️")
    
    # --- Inputs Glas Test ---
    st.markdown("#### MESSWERTE")
    
    # Schieberegler sind mobil oft besser als Tippen
    swelling_vol = st.number_input("QUELLVOLUMEN (in ml)", min_value=0, max_value=500, step=5, help="Abgelesen am Messbecher")
    
    # LOGIK: Warnung bei wenig Volumen
    if 0 < swelling_vol < 30:
        st.error("⚠️ NIEDRIGES VOLUMEN DETEKTIERT!")
        st.markdown("> **System Message:** Scheint ein 'Hardcore-Batch' (Heavy Duty) zu sein. Bitte noch 1h warten und erneut messen.")

    swelling_time = st.number_input("ZEIT BIS SÄTTIGUNG (in min)", min_value=0, step=1)
    
    rest_water = st.radio("RESTWASSER STATUS", 
                          ["Alles aufgesaugt (Trocken)", "Leichter Film", "Pfütze vorhanden", "Suppe"],
                          index=0)

    st.divider()

    # -----------------------------------------------------
    # SZENARIO B: HAPTIK CHECK
    # -----------------------------------------------------
    st.markdown("## B // HAPTIK CHECK (QUALITÄT)")
    st.markdown("*Fasse in das aufgequollene Granulat.*")

    # Slider für Konsistenz
    consistency = st.slider("KONSISTENZ (1=Schleim, 5=Hartgummi)", 1, 5, 3)
    
    # LOGIK: Critical Fail
    if consistency == 1:
        st.error("🚨 CRITICAL FAIL: SLIME DETECTED")
        st.markdown("Das ist Konkurrenz-Niveau. Batch markieren!")
    elif consistency == 3:
        st.success("✅ TARGET: FESTER PUDDING")

    haptik_cols = st.columns(2)
    with haptik_cols[0]:
        stickiness = st.selectbox("KLEBRIGKEIT", ["Trocken", "Angenehm feucht", "Klebt leicht", "Klebt wie Honig"])
    with haptik_cols[1]:
        structure = st.selectbox("STRUKTUR", ["Bleibt körnig (Ziel)", "Zerfällt leicht", "Matsch"])

    st.divider()

    # -----------------------------------------------------
    # SZENARIO C: TOPF TEST (ANWENDUNG)
    # -----------------------------------------------------
    st.markdown("## C // TOPF TEST")
    
    app_method = st.radio("METHODE", ["Trockentermischung", "Pre-Soak (Vorgequollen)"], horizontal=True)

    # LOGIK: Pre-Soak Warnung
    if app_method == "Pre-Soak (Vorgequollen)":
        st.warning("⚠️ ACHTUNG: PFLANZENKOHLE FÄRBT! HANDSCHUHE TRAGEN.")

    c_col1, c_col2 = st.columns(2)
    dirty_hands = c_col1.checkbox("Schwarze Schlamm-Hände?")
    elevator_effect = c_col2.checkbox("Fahrstuhl-Effekt (Pflanze hochgedrückt)?")

    # -----------------------------------------------------
    # ABSCHLUSS & UPLOAD
    # -----------------------------------------------------
    st.divider()
    st.markdown("### D // DOKUMENTATION")
    
    free_text = st.text_area("FREITEXT / BEOBACHTUNGEN", placeholder="Glibber oder Gold?")
    
    uploaded_file = st.file_uploader("FOTO BEWEIS (Optional)", type=['png', 'jpg', 'jpeg'])
    
    # Submit Button Logic
    st.markdown("<br>", unsafe_allow_html=True)
    submit_btn = st.button("DATEN ÜBERTRAGEN [SEND]")

    if submit_btn:
        if not tester_name:
            st.error("❌ FEHLER: Name fehlt.")
        else:
            # Datensatz erstellen
            file_name_saved = "kein_bild"
            if uploaded_file is not None:
                file_name_saved = f"{batch_id}_{tester_name}_{uploaded_file.name}"
                # Hinweis: Hier würde man das Bild normalerweise speichern
            
            feedback_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "batch_id": batch_id,
                "tester": tester_name,
                "vol_ml": swelling_vol,
                "time_min": swelling_time,
                "rest_water": rest_water,
                "consistency": consistency,
                "stickiness": stickiness,
                "structure": structure,
                "method": app_method,
                "dirty_hands": dirty_hands,
                "elevator_effect": elevator_effect,
                "comment": free_text,
                "image": file_name_saved
            }
            
            save_feedback(feedback_data)
            
            st.balloons()
            st.success("✅ DATEN ERFOLGREICH IN DIE MATRIX ÜBERTRAGEN.")
            st.markdown(f"**Log:** Eintrag für Batch `{batch_id}` gespeichert.")

    # -----------------------------------------------------
    # ADMIN VIEW (Nur wenn ?admin=true)
    # -----------------------------------------------------
    if query_params.get("admin") == "true":
        st.divider()
        st.warning("🔒 ADMIN AREA")
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            st.dataframe(df)
            
            # Download Button für CSV
            with open(DATA_FILE, "rb") as f:
                st.download_button("DOWNLOAD CSV", f, file_name="plantnex_full_data.csv")

if __name__ == "__main__":
    main()
