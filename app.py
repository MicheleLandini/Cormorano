"""
Script description: Sistema di gestione noleggio ombrelloni e kit mare per il Cormorano.

Libraries imported:
-------------------
- yaml: Module implementing the data serialization used for human readable documents.
- streamlit: Framework used to build pure Python web applications.
- json: Module for JSON data handling.
- datetime: Module for date and time operations.
- os: Module for operating system interface.
"""

import yaml
import streamlit as st
import json
import os
from datetime import datetime, date
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import *

# Configurazione pagina
st.set_page_config(
    page_title="Cormorano Gest..",
    page_icon="🏖️",
    layout="wide"
)

# File di configurazione e dati
CONFIG_FILE = 'config.yaml'
RESERVATIONS_FILE = 'reservations.json'

# Funzioni per gestire i dati JSON
def load_reservations():
    """Carica le prenotazioni dal file JSON"""
    if os.path.exists(RESERVATIONS_FILE):
        try:
            with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_reservations(reservations):
    """Salva le prenotazioni nel file JSON"""
    try:
        with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(reservations, f, ensure_ascii=False, indent=2, default=str)
        return True
    except Exception as e:
        st.error(f"Errore nel salvataggio: {e}")
        return False

# Inizializzazione session state
if "reservations" not in st.session_state:
    st.session_state.reservations = load_reservations()

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Loading config file
try:
    with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error(f"File {CONFIG_FILE} non trovato. Assicurati che esista nella directory.")
    st.stop()

# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Stato della pagina
if "mode" not in st.session_state:
    st.session_state.mode = "login"

# Funzioni per cambiare modalità e pagine
def show_login():
    st.session_state.mode = "login"

def show_register():
    st.session_state.mode = "register"

def change_page(page):
    st.session_state.current_page = page

# CSS personalizzato
st.markdown("""
<style>
    /* Cards responsive e con effetto vetro */
    .rental-card, .completed-rental {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
        width: 100%;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    /* Gradiente per rental-card */
    .rental-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%);
    }

    /* Stessa dimensione e margini ma colore verde per completed-rental */
    .completed-rental {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.8) 0%, rgba(69, 160, 73, 0.8) 100%);
    }

    #Tolgo spazio vuolto inizio pagina    NON VAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA PORCA TROIA   
    .st-emotion-cache-8atqhb.e1mlolmg0 {
        display: none;
    }

    /* Stats cards responsive con effetto vetro */
    .stats-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px 0;
        width: 100%;
        box-sizing: border-box;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Equipment badge */
    .equipment-badge {
        background-color: rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 5px 12px;
        margin: 5px;
        display: inline-block;
        font-size: 0.9em;
    }

    /* Bottone stile */
    .stButton > button {
        border-radius: 10px;
        border: none;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        width: 100%;
        max-width: 200px;
        padding: 10px;
        margin: 5px 0;
    }

    /* Media query per mobile */
    @media (max-width: 768px) {
    .rental-card, .completed-rental, .stats-card {
        padding: 7px;
        align-items: center;
        justify-content: left;
        display: flex;
    }
            
    .txt-card {
        margin: 0px !important;
    }
        
    .equipment-badge {
        font-size: 0.8em;
        padding: 4px 10px;
    }
    }
</style>
""", unsafe_allow_html=True)

# Header principale
#st.title("🏖️ Cormorano Gest..")
#st.markdown("Sistema di gestione ombrelloni e kit mare")

# Bottoni login/register (solo se non autenticato)
# Bottoni login/register (solo se non autenticato)
if "name" not in st.session_state or not st.session_state.get('authentication_status'):
    # Mostra solo il bottone opposto a quello attualmente visualizzato
    if st.session_state.get('mode') == "login":
        st.button("📝 Registrati", on_click=show_register, use_container_width=True)
    elif st.session_state.get('mode') == "register":
        st.button("🔑 Accedi", on_click=show_login, use_container_width=True)
    else:
        # Se nessun form è visibile, mostra entrambi i bottoni
        col1, col2 = st.columns(2)
        with col1:
            st.button("🔑 Login", on_click=show_login, use_container_width=True)
        with col2:
            st.button("📝 Register", on_click=show_register, use_container_width=True)

# Visualizzazione condizionale per login/register
if st.session_state.mode == "login" and ("name" not in st.session_state or not st.session_state.get('authentication_status')):
    st.markdown("### 🔑 Accesso al Sistema")
    try:
        authenticator.login()
    except LoginError as e:
        st.error(f"Errore di login: {e}")

    if st.session_state.get('authentication_status'):
        st.success(f'✅ Benvenuto *{st.session_state["name"]}*!')
        st.rerun()
    elif st.session_state.get('authentication_status') is False:
        st.error('❌ Username/password errato')
    elif st.session_state.get('authentication_status') is None:
        st.warning('⚠️ Inserisci username e password')

elif st.session_state.mode == "register" and ("name" not in st.session_state or not st.session_state.get('authentication_status')):
    st.markdown("### 📝 Registrazione Nuovo Utente")
    try:
        (email_of_registered_user,
         username_of_registered_user,
         name_of_registered_user) = authenticator.register_user()
        if email_of_registered_user:
            st.success('✅ Utente registrato con successo!')
            # Salva automaticamente il config
            with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
                yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
    except RegisterError as e:
        st.error(f"Errore registrazione: {e}")

# Sidebar e contenuto principale (solo se autenticato)
if "name" in st.session_state and st.session_state.get('authentication_status'):
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🏖️  Gestionale Cormorano")
        
        # Informazioni utente
        st.info(f"👤 **Utente:** {st.session_state['name']}")
        
        st.divider()
        
        # Navigazione
        if st.button("🏠 Dashboard", use_container_width=True):
            change_page("home")
        
        if st.button("📋 Gestione Noleggi", use_container_width=True):
            change_page("rentals")
        
        if st.button("📊 Statistiche", use_container_width=True):
            change_page("stats")
        
        if st.button("👤 Profilo", use_container_width=True):
            change_page("profile")
        
        if st.button("⚙️ Impostazioni", use_container_width=True):
            change_page("settings")
        
        st.divider()
        
        # Logout
        authenticator.logout("Logout", "sidebar")

    # Contenuto principale basato sulla pagina corrente
    if st.session_state.current_page == "home":
        st.markdown("## 🏠 Dashboard Generale")
        
        # Statistiche rapide
        col1, col2 = st.columns(2)
        
        total_rentals = len(st.session_state.reservations)
        completed_rentals = len([r for r in st.session_state.reservations if r.get('completed', False)])
        active_rentals = total_rentals - completed_rentals
        
        # Stile CSS
        st.markdown("""
            <style>
            .stats-card h2, .stats-card p {
                color: #000000 !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Colonna 1 - Elementi in verticale
        with col1:
            st.markdown("""
            <div class="stats-card">
                <h3>📋</h3>
                <h2>{}</h2>
                <p class="txt-card">Noleggi Totali</p>
            </div>
            """.format(total_rentals), unsafe_allow_html=True)
            
            st.markdown("""
            <div class="stats-card">
                <h3>✅</h3>
                <h2>{}</h2>
                <p class="txt-card">Completati</p>
            </div>
            """.format(completed_rentals), unsafe_allow_html=True)
        
        # Colonna 2 - Elementi in verticale
        with col2:
            st.markdown("""
            <div class="stats-card">
                <h3>⏳</h3>
                <h2>{}</h2>
                <p class="txt-card">Attivi</p>
            </div>
            """.format(active_rentals), unsafe_allow_html=True)
            
            today_rentals = len([r for r in st.session_state.reservations 
                            if r.get('date') == str(date.today())])
            st.markdown("""
            <div class="stats-card">
                <h3>📅</h3>
                <h2>{}</h2>
                <p class="txt-card">Oggi</p>
            </div>
            """.format(today_rentals), unsafe_allow_html=True)
        
        st.divider()
        
        # Noleggi recenti
        st.markdown("### 📅 Noleggi Recenti")
        st.markdown("##### Ultimi 5 noleggi")
        recent_rentals = sorted(st.session_state.reservations, 
                              key=lambda x: x.get('created_at', ''), reverse=True)[:5]
        
        if recent_rentals:
            for rental in recent_rentals:
                status_class = "completed-rental" if rental.get('completed', False) else "rental-card"
                status_icon = "✅" if rental.get('completed', False) else "⏳"
                
                equipment_badges = ""
                if rental.get('ombrellone', 0) > 0:
                    equipment_badges += f'<span class="equipment-badge">☂️ {rental["ombrellone"]}</span>'
                if rental.get('sdraio', 0) > 0:
                    equipment_badges += f'<span class="equipment-badge">🪑 {rental["sdraio"]}</span>'
                if rental.get('lettino', 0) > 0:
                    equipment_badges += f'<span class="equipment-badge">🛏️ {rental["lettino"]}</span>'
                if rental.get('regista', 0) > 0:
                    equipment_badges += f'<span class="equipment-badge">🎬 {rental["regista"]}</span>'
                
                st.markdown(f"""
                <div class="{status_class}">
                    <h4>{status_icon} {rental['name']}</h4>
                    <p><strong>📅 Data:</strong> {rental['date']}</p>
                    <p><strong>🏖️ Kit:</strong> {equipment_badges}</p>
                    <small>👤 Creato da: {rental.get('created_by', 'N/A')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🌊 Nessun noleggio presente")

    elif st.session_state.current_page == "rentals":
        st.markdown("## 📋 Gestione Noleggi")
        
        # Form per nuovo noleggio
        with st.expander("➕ Nuovo Noleggio", expanded=False):
            with st.form("new_rental"):
                st.markdown("### 📝 Dettagli Cliente")
                col1, col2 = st.columns(2)
                
                with col1:
                    client_name = st.text_input("👤 Nome Cliente", placeholder="Nome e cognome")
                    rental_date = st.date_input("📅 Data Noleggio", value=date.today())
                    phone = st.text_input("📞 Telefono", placeholder="Numero di telefono")
                
                with col2:
                    email = st.text_input("📧 Email", placeholder="email@esempio.com")
                    return_date = st.date_input("📅 Data Restituzione", value=date.today())
                    price = st.number_input("💰 Prezzo Totale (€)", min_value=0.0, step=0.5)
                
                st.divider()
                st.markdown("### 🏖️ Kit Mare")
                
                # Contatori per attrezzature
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    ombrellone = st.number_input("☂️ Ombrelloni", min_value=0, max_value=20, value=0)
                with col2:
                    sdraio = st.number_input("🪑 Sedie Sdraio", min_value=0, max_value=50, value=0)
                with col3:
                    lettino = st.number_input("🛏️ Lettini", min_value=0, max_value=30, value=0)
                with col4:
                    regista = st.number_input("🎬 Sedie Regista", min_value=0, max_value=20, value=0)
                
                notes = st.text_area("📝 Note Aggiuntive", placeholder="Eventuali note sul noleggio...")
                
                col1, col2 = st.columns(2)
                with col1:
                    deposit_paid = st.checkbox("💳 Deposito Pagato")
                with col2:
                    insurance = st.checkbox("🛡️ Assicurazione")
                
                if st.form_submit_button("💾 Salva Noleggio", use_container_width=True):
                    if client_name.strip():
                        # Genera ID unico
                        rental_id = max([r.get('id', 0) for r in st.session_state.reservations], default=0) + 1
                        
                        new_rental = {
                            'id': rental_id,
                            'name': client_name.strip(),
                            'phone': phone,
                            'email': email,
                            'date': str(rental_date),
                            'return_date': str(return_date),
                            'ombrellone': ombrellone,
                            'sdraio': sdraio,
                            'lettino': lettino,
                            'regista': regista,
                            'price': price,
                            'deposit_paid': deposit_paid,
                            'insurance': insurance,
                            'notes': notes,
                            'completed': False,
                            'created_at': datetime.now().isoformat(),
                            'created_by': st.session_state['name']
                        }
                        
                        st.session_state.reservations.append(new_rental)
                        
                        if save_reservations(st.session_state.reservations):
                            st.success("✅ Noleggio salvato con successo!")
                            st.rerun()
                        else:
                            st.error("❌ Errore nel salvataggio")
                    else:
                        st.error("⚠️ Il nome del cliente è obbligatorio")
        
        st.divider()
        
        # Filtri
        st.markdown("### 🔍 Filtri di Ricerca")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            filter_date = st.date_input("📅 Data", value=None, key="filter_date")
        with col2:
            filter_status = st.selectbox("Stato", ["Tutti", "Attivi", "Completati"])
        with col3:
            search_name = st.text_input("🔍 Cerca nome", key="search_name")
        with col4:
            equipment_filter = st.selectbox("Attrezzatura", ["Tutte", "Ombrelloni", "Sdraio", "Lettini", "Regista"])
        
        # Lista noleggi
        st.markdown("### 📋 Lista Noleggi")
        
        # Applica filtri
        filtered_rentals = st.session_state.reservations.copy()
        
        if filter_date:
            filtered_rentals = [r for r in filtered_rentals if r['date'] == str(filter_date)]
        
        if filter_status == "Attivi":
            filtered_rentals = [r for r in filtered_rentals if not r.get('completed', False)]
        elif filter_status == "Completati":
            filtered_rentals = [r for r in filtered_rentals if r.get('completed', False)]
        
        if search_name:
            filtered_rentals = [r for r in filtered_rentals 
                              if search_name.lower() in r['name'].lower()]
        
        if equipment_filter != "Tutte":
            equipment_map = {
                "Ombrelloni": "ombrellone",
                "Sdraio": "sdraio", 
                "Lettini": "lettino",
                "Regista": "regista"
            }
            equipment_key = equipment_map[equipment_filter]
            filtered_rentals = [r for r in filtered_rentals if r.get(equipment_key, 0) > 0]
        
        # Ordinamento
        filtered_rentals = sorted(filtered_rentals, key=lambda x: x['date'], reverse=True)
        
        if filtered_rentals:
            for rental in filtered_rentals:
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    # Card noleggio
                    status_class = "completed-rental" if rental.get('completed', False) else "rental-card"
                    status_icon = "✅ COMPLETATO" if rental.get('completed', False) else "⏳ ATTIVO"
                    
                    equipment_info = []
                    if rental.get('ombrellone', 0) > 0:
                        equipment_info.append(f"☂️ {rental['ombrellone']} Ombrelloni")
                    if rental.get('sdraio', 0) > 0:
                        equipment_info.append(f"🪑 {rental['sdraio']} Sdraio")
                    if rental.get('lettino', 0) > 0:
                        equipment_info.append(f"🛏️ {rental['lettino']} Lettini")
                    if rental.get('regista', 0) > 0:
                        equipment_info.append(f"🎬 {rental['regista']} Regista")
                    
                    equipment_badges = ' '.join([f'<span class="equipment-badge">{eq}</span>' for eq in equipment_info])
                    
                    payment_status = "💳 Deposito Pagato" if rental.get('deposit_paid') else "💳 Deposito NON Pagato"
                    insurance_status = "🛡️ Assicurato" if rental.get('insurance') else ""
                    
                    st.markdown(f"""
                    <div class="{status_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3>👤 {rental['name']}</h3>
                            <span><strong>{status_icon}</strong></span>
                        </div>
                        <p><strong>📅 Dal:</strong> {rental['date']} <strong>Al:</strong> {rental.get('return_date', 'N/A')}</p>
                        <p><strong>📞:</strong> {rental.get('phone', 'N/A')} <strong>📧:</strong> {rental.get('email', 'N/A')}</p>
                        <p><strong>🏖️ Kit Mare:</strong></p>
                        <div>{equipment_badges}</div>
                        <p><strong>💰 Prezzo:</strong> €{rental.get('price', 0)} - {payment_status} {insurance_status}</p>
                        {f"<p><strong>📝 Note:</strong> {rental.get('notes', '')}</p>" if rental.get('notes') else ""}
                    </div>
                    """, unsafe_allow_html=True)

                
                with col2:
                    st.write("")  # Spaziatura
                    st.write("")  # Spaziatura
                    
                    # Checkbox completamento
                    completed = st.checkbox(
                        "Restituito",
                        value=rental.get('completed', False),
                        key=f"completed_{rental['id']}"
                    )

                    # Aggiorna stato se cambiato
                    if completed != rental.get('completed', False):
                        for idx, res in enumerate(st.session_state.reservations):
                            if res['id'] == rental['id']:
                                st.session_state.reservations[idx]['completed'] = completed
                                if completed:
                                    st.session_state.reservations[idx]['deposit_paid'] = True
                                save_reservations(st.session_state.reservations)
                                st.rerun()

                    
                    # Bottone elimina
                    if st.button("🗑️ Elimina", key=f"delete_{rental['id']}", help="Elimina noleggio"):
                        st.session_state.reservations = [r for r in st.session_state.reservations 
                                                        if r['id'] != rental['id']]
                        save_reservations(st.session_state.reservations)
                        st.success("Noleggio eliminato!")
                        st.rerun()
            
            st.divider()
        else:
            st.info("🌊 Nessun noleggio trovato con i filtri applicati")

    elif st.session_state.current_page == "stats":
        st.markdown("## 📊 Statistiche Dettagliate")
        
        if st.session_state.reservations:
            # Statistiche attrezzature
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🏖️ Utilizzo Attrezzature")
                total_equipment = {}
                for rental in st.session_state.reservations:
                    for equipment in ['ombrellone', 'sdraio', 'lettino', 'regista']:
                        total_equipment[equipment] = total_equipment.get(equipment, 0) + rental.get(equipment, 0)
                
                for equipment, total in total_equipment.items():
                    emoji_map = {'ombrellone': '☂️', 'sdraio': '🪑', 'lettino': '🛏️', 'regista': '🎬'}
                    st.metric(f"{emoji_map[equipment]} {equipment.title()}", total)
            
            with col2:
                st.markdown("### 💰 Statistiche Finanziarie")
                total_revenue = sum([r.get('price', 0) for r in st.session_state.reservations])
                avg_rental = total_revenue / len(st.session_state.reservations) if st.session_state.reservations else 0
                deposits_paid = len([r for r in st.session_state.reservations if r.get('deposit_paid')])
                
                st.metric("Ricavi Totali", f"€{total_revenue:.2f}")
                st.metric("Media per Noleggio", f"€{avg_rental:.2f}")
                st.metric("Depositi Pagati", deposits_paid)
        else:
            st.info("🌊 Nessun dato disponibile per le statistiche")

    elif st.session_state.current_page == "profile":
        st.markdown("## 👤 Profilo Utente")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Nome:** {st.session_state['name']}")
            st.info(f"**Username:** {st.session_state['username']}")
        
        with col2:
            st.markdown("### 🔒 Cambia Password")
            try:
                if authenticator.reset_password(st.session_state['username']):
                    st.success('✅ Password cambiata con successo')
                    with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
                        yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
            except ResetError as e:
                st.error(f"Errore: {e}")
                

    elif st.session_state.current_page == "settings":
        st.markdown("## ⚙️ Impostazioni Sistema")
        
        # Gestione dati
        st.markdown("### 📊 Gestione Dati")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Esporta JSON", use_container_width=True):
                if st.session_state.reservations:
                    json_data = json.dumps(st.session_state.reservations, ensure_ascii=False, indent=2)
                    st.download_button(
                        "⬇️ Scarica Backup",
                        data=json_data,
                        file_name=f"noleggi_backup_{date.today()}.json",
                        mime="application/json"
                    )
                else:
                    st.info("Nessun dato da esportare")
        
        with col2:
            uploaded_file = st.file_uploader("📤 Importa JSON", type=['json'])
            if uploaded_file is not None:
                try:
                    imported_data = json.load(uploaded_file)
                    if isinstance(imported_data, list):
                        st.session_state.reservations = imported_data
                        save_reservations(st.session_state.reservations)
                        st.success("✅ Dati importati con successo!")
                        st.rerun()
                    else:
                        st.error("❌ Formato file non valido")
                except Exception as e:
                    st.error(f"❌ Errore nell'importazione: {e}")
        
        with col3:
            if st.button("🗑️ Cancella Tutti", use_container_width=True):
                if st.session_state.reservations:
                    if st.checkbox("⚠️ Conferma cancellazione"):
                        st.session_state.reservations = []
                        save_reservations(st.session_state.reservations)
                        st.success("Tutti i dati sono stati eliminati")
                        st.rerun()
                else:
                    st.info("Nessun dato da eliminare")

# Salvataggio automatico config
try:
    with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
        yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
except Exception as e:
    if "name" in st.session_state:
        st.sidebar.error(f"Errore salvataggio config: {e}")