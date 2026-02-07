import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time

# ---------------------------------------------------------
# 1. KONFIGURATION & STYLING (KIOSK MODE)
# ---------------------------------------------------------
st.set_page_config(
    page_title="PLANTNEX LAB",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS: Dark Mode + Streamlit UI Elemente verstecken
st.markdown("""
    <style>
    /* 1. Alles verstecken, was nach Streamlit aussieht */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* 2. Farben & Look (Industrial Dark) */
    .stApp {
        background-color: #0E1117; /* Sehr dunkles Grau */
        color: #E0E0E0;
    }
    
    /* Überschriften */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-family: 'Arial', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Grüne Akzente (PLANTNEX Vibe) */
    .stSlider [data-baseweb="slider"] div[role="slider"] {
        background-color: #00FF41 !important; /* Matrix Green */
    }
    .stProgress > div > div > div > div {
        background-color: #00FF41;
    }
    
    /* 3. Breite Buttons für Touch-Bedienung */
    div.stButton > button {
        background-color: #1F2937;
        color: #00FF41;
        border: 1px solid #00FF41;
        font-weight: bold;
        padding: 15px 0px;
        width: 100%;
        border-radius: 4px;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color: #00FF41;
        color: #000000;
        border: 1px solid #FFFFFF;
    }
    
    /* Warnboxen Styling */
    div[data-baseweb="notification"] {
        border-left: 5px solid #00FF41;
        background-color: #1F2937;
    }
    </style>
    """, unsafe_allow_html=True)

# Dateiname für CSV
DATA_FILE = "plantnex_feedback.csv"

# ---------------------------------------------------------
# 2. HILFSFUNKTIONEN
# ---------------------------------------------------------
def save_feedback(data_dict):
    """Speichert Daten in CSV"""
    df_new = pd.DataFrame([data_dict])
    if not os.path.isfile(DATA_FILE):
        df_new.to_csv(DATA_FILE, index=False)
    else:
        df_new.to_csv(DATA_FILE, mode='a', header=False, index=False)

# ---------------------------------------------------------
# 3. APP UI
# ---------------------------------------------------------
def main():
    # URL Parameter lesen (?id=Max -> id="Max")
    query_params = st.query_params
    default_user = query_params.get("id", "")
    
    # --- HEADER ---
    st.markdown("## PLANTNEX // LAB PROTOKOLL")
    st.caption("Qualitätskontrolle & Beta-Test")
    st.divider()

    # --- ABSCHNITT 0: WER UND WAS ---
    col1, col2 = st.columns(2)
    with col1:
        tester_name = st.text_input("NAME DES PRÜFERS", value=default_user, placeholder="Dein Vorname")
    with col2:
        batch_id = st.text_input("CHARGEN-NR.", placeholder="z.B. B004-Mais", help="Steht auf dem Testbeutel")

    if not batch_id:
        st.warning("⚠️ Bitte gib zuerst die Chargen-Nr. ein.")
        st.stop() # App stoppt hier, bis ID da ist

    # -----------------------------------------------------
    # SZENARIO A: GLAS TEST
    # -----------------------------------------------------
    st.markdown("### A // GLAS TEST")
    st.info("ℹ️ Mischung: 1 Teelöffel (5g) + 200ml Wasser.")

    # Timer Buttons
    st.caption("Stoppuhr starten:")
    t_col1, t_col2 = st.columns(2)
    if t_col1.button("15 MINUTEN"):
        st.toast("Timer läuft: 15 Min (Simuliert)", icon="⏱️")
    if t_col2.button("30 MINUTEN"):
        st.toast("Timer läuft: 30 Min (Simuliert)", icon="⏱️")
    
    # Eingaben
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Schieberegler für Volumen
    st.markdown("**1. Wie viel Masse ist entstanden? (in ml)**")
    swelling_vol = st.slider("", 0, 300, 0, step=10, key="vol_slider")
    st.write(f"Eingabe: **{swelling_vol} ml**")
    
    # LOGIK: Warnung
    if 0 < swelling_vol < 30:
        st.error("⚠️ ACHTUNG: Sehr wenig Volumen!")
        st.markdown("*Das Material wirkt inaktiv. Bitte noch 30-60 min warten.*")

    st.markdown("**2. Wie lange hat es gedauert? (Minuten)**")
    swelling_time = st.number_input("", min_value=0, step=1, label_visibility="collapsed")
    
    st.markdown("**3. Restwasser im Glas?**")
    rest_water = st.radio("Restwasser Status", 
                          ["Alles weg (Trocken)", "Leichter Film", "Pfütze", "Suppe (Schwimmt)"],
                          index=0, label_visibility="collapsed")

    st.divider()

    # -----------------------------------------------------
    # SZENARIO B: HAPTIK CHECK
    # -----------------------------------------------------
    st.markdown("### B // HAPTIK & GEFÜHL")
    st.markdown("*Fasse in das aufgequollene Granulat.*")

    st.markdown("**1. Konsistenz (Gefühl)**")
    # Custom Labels unter dem Slider simulieren wir durch Text
    consistency = st.slider("Slider Konsistenz", 1, 5, 3, label_visibility="collapsed")
    
    # Visuelles Feedback zum Slider-Wert
    if consistency == 1:
        st.error("URTEIL: SCHLEIM (FLÜSSIG)")
        st.markdown("🚨 **KRITISCHER FEHLER!** Das ist zu weich.")
    elif consistency == 2:
        st.warning("URTEIL: ZU WEICH")
    elif consistency == 3:
        st.success("URTEIL: PERFEKT (WACKELPUDDING)")
    elif consistency == 4:
        st.info("URTEIL: FEST")
    else:
        st.info("URTEIL: HARTGUMMI (ZU FEST)")

    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.markdown("**2. Klebrigkeit**")
        stickiness = st.selectbox("", ["Trocken / Krümelig", "Angenehm feucht", "Klebt leicht", "Klebt wie Honig"], label_visibility="collapsed")
    with col_h2:
        st.markdown("**3. Struktur**")
        structure = st.selectbox("", ["Körnig / Stückig (Gut)", "Zerfällt sofort", "Matschig / Brei"], label_visibility="collapsed")

    st.divider()

    # -----------------------------------------------------
    # SZENARIO C: ANWENDUNG
    # -----------------------------------------------------
    st.markdown("### C // ANWENDUNG")
    
    app_method = st.radio("Wie wendest du es an?", ["Trocken einmischen", "Vorgequollen (Nass)"], horizontal=True)

    if app_method == "Vorgequollen (Nass)":
        st.warning("⚠️ VORSICHT: FÄRBT SCHWARZ! Handschuhe anziehen.")

    c1, c2 = st.columns(2)
    dirty_hands = c1.checkbox("Schwarze Hände?")
    elevator_effect = c2.checkbox("Pflanze hochgedrückt?")

    st.divider()
    
    # -----------------------------------------------------
    # ABSCHLUSS
    # -----------------------------------------------------
    st.markdown("**Freitext / Anmerkungen:**")
    free_text = st.text_area("", placeholder="Ist dir sonst noch etwas aufgefallen?", label_visibility="collapsed")
    
    st.markdown("**Foto vom Ergebnis (Optional):**")
    uploaded_file = st.file_uploader("", type=['jpg', 'png', 'jpeg'], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Der große Absende-Button
    submit_btn = st.button("BERICHT ABSENDEN 🚀")

    if submit_btn:
        if not tester_name:
            st.error("❌ Bitte gib oben deinen Namen ein!")
        else:
            # Daten speichern
            image_name = "kein_bild"
            if uploaded_file:
                image_name = f"{batch_id}_{tester_name}_{uploaded_file.name}"
                # Hier würde man das Bild speichern code einfügen
            
            feedback_data = {
                "zeitstempel": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "charge": batch_id,
                "pruefer": tester_name,
                "volumen_ml": swelling_vol,
                "dauer_min": swelling_time,
                "restwasser": rest_water,
                "konsistenz_wert": consistency,
                "klebrigkeit": stickiness,
                "struktur": structure,
                "methode": app_method,
                "schmutzige_haende": dirty_hands,
                "fahrstuhl_effekt": elevator_effect,
                "kommentar": free_text,
                "bild": image_name
            }
            
            save_feedback(feedback_data)
            
            st.balloons()
            st.success("✅ DATEN ÜBERMITTELT! Danke für den Test.")
            st.markdown(f"Eintrag für Charge **{batch_id}** wurde gespeichert.")

    # -----------------------------------------------------
    # ADMIN LINK (Versteckt)
    # -----------------------------------------------------
    # Nur sichtbar wenn ?admin=true in URL
    if query_params.get("admin") == "true":
        st.divider()
        st.error("🔒 ADMIN BEREICH")
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            st.dataframe(df)
            
            with open(DATA_FILE, "rb") as f:
                st.download_button("CSV HERUNTERLADEN", f, file_name="plantnex_daten.csv")

if __name__ == "__main__":
    main()
