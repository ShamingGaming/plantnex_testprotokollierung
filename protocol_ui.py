import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ---------------------------------------------------------
# KONFIGURATION & SETUP
# ---------------------------------------------------------
# Layout "centered" ist besser für mobile Ansichten als "wide"
st.set_page_config(
    page_title="Produkt-Feedback",
    page_icon="⭐",
    layout="centered" 
)

# Dateiname für die lokale Speicherung (CSV)
DATA_FILE = "bewertungen.csv"

# ---------------------------------------------------------
# HILFSFUNKTIONEN (BACKEND)
# ---------------------------------------------------------
def save_feedback(user_id, ratings_dict):
    """Speichert das Feedback in einer CSV-Datei."""
    
    # Metadaten hinzufügen
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tester_id": user_id
    }
    # Die eigentlichen Bewertungen hinzufügen
    data.update(ratings_dict)
    
    # DataFrame erstellen
    new_entry = pd.DataFrame([data])
    
    # Speichern (Anhängen an CSV oder neu erstellen)
    if not os.path.isfile(DATA_FILE):
        new_entry.to_csv(DATA_FILE, index=False)
    else:
        new_entry.to_csv(DATA_FILE, mode='a', header=False, index=False)

# ---------------------------------------------------------
# HAUPTANWENDUNG (FRONTEND)
# ---------------------------------------------------------
def main():
    # 1. URL Parameter auslesen (Wer ist der Tester?)
    # Aufruf via: deinedomain.streamlit.app/?id=max_muster
    query_params = st.query_params
    tester_id = query_params.get("id", "Gast_Tester")

    # 2. Header & Einleitung
    st.title("Produkt-Feedback")
    
    # KI-PLATZHALTER: Hier dynamische Begrüßung einfügen
    st.write(f"Hallo! Danke, dass du dir Zeit nimmst.") 

    # 3. Das Formular
    # 'clear_on_submit=True' sorgt dafür, dass das Formular nach dem Senden leer ist
    with st.form("bewertungs_form", clear_on_submit=True):
        
        st.info("Bitte bewerte die folgenden Punkte ehrlich.")

        # --- ANWEISUNG FÜR DIE KI: HIER FRAGEN EINFÜGEN ---
        # Nutze st.slider, st.feedback (Sterne), st.selectbox oder st.text_area.
        # Beispielstruktur (wird durch die KI ersetzt):
        
        rating_overall = st.slider("Gesamteindruck (1-10)", 1, 10, 5)
        
        # Für Mobile besser: Selectbox statt Radio Buttons (weniger Platzbedarf)
        usability = st.selectbox(
            "Wie einfach war die Bedienung?",
            ["Sehr einfach", "Okay", "Kompliziert", "Sehr schwer"]
        )
        
        comment = st.text_area("Was hat dir besonders gefallen / nicht gefallen?")
        
        # --- ENDE FRAGEN ---

        # Absende-Button (breit für gute Touch-Erreichbarkeit)
        submitted = st.form_submit_button("Bewertung absenden", use_container_width=True)

        if submitted:
            # Daten sammeln
            feedback_data = {
                "Gesamteindruck": rating_overall,
                "Bedienbarkeit": usability,
                "Kommentar": comment
                # KI: Hier weitere Felder mappen
            }
            
            # Speichern
            save_feedback(tester_id, feedback_data)
            
            st.success("Vielen Dank! Deine Bewertung wurde gespeichert.")
            st.balloons()

    # 4. Admin-Ansicht (Optional: Nur sichtbar, wenn ?admin=true in URL)
    if query_params.get("admin") == "true":
        st.divider()
        st.subheader("Admin Bereich: Alle Daten")
        if os.path.isfile(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            st.dataframe(df)
        else:
            st.write("Noch keine Daten vorhanden.")

if __name__ == "__main__":
    main()
