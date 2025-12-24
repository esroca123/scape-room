import streamlit as st
import random
import time
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Tirage au Sort de Noël", layout="wide")

# --- ESTILOS CSS (CENTRADO Y TAMAÑO) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), 
                    url("https://www.transparenttextures.com/patterns/snow.png"),
                    linear-gradient(to bottom, #d63031, #2d3436);
        background-attachment: fixed;
    }

    /* FORZAR CENTRADO DEL BOTÓN */
    div.stButton {
        text-align: center;
        display: flex;
        justify-content: center;
        margin: 30px 0;
    }

    div.stButton > button:first-child {
        width: 180px !important;
        height: 180px !important;
        border-radius: 50% !important;
        border: 8px solid #f1c40f !important;
        background-color: #e74c3c !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        box-shadow: 0 8px #c0392b, 0 15px 20px rgba(0,0,0,0.4) !important;
        transition: all 0.2s ease;
        z-index: 999;
    }

    /* Recuadro de información */
    .info-box {
        background-color: rgba(255, 255, 255, 0.95);
        color: #2d3436 !important;
        padding: 20px;
        border-radius: 20px;
        border: 4px solid #2ecc71;
        text-align: center;
        max-width: 400px;
        margin: 0 auto;
    }
    
    .info-box h2 { color: #d63031 !important; font-size: 35px !important; margin: 0; }

    /* REDUCIR TAMAÑO DE IMÁGENES DE EQUIPO */
    .stImage img {
        max-width: 90px !important; /* Ajusta este número si las quieres aún más pequeñas */
        border-radius: 50%;
        margin: 0 auto;
        display: block;
        border: 3px solid white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. DICTIONNAIRE DES PARTICIPANTS ---
PARTICIPANTES = {
    "Rose": "fotos/Rose.png",
    "Marie": "fotos/Marie.png",
    "Carl": "fotos/Carl.png",
    "Nataly": "fotos/Nataly.png",
    "Marc": "fotos/Marc.png",
    "Helene": "fotos/Helene.png",
    "Rejean": "fotos/Rejean.png",
    "Charlot": "fotos/Charlot.png",
    "Louis": "fotos/Louis.png"
}

FOTO_AVATAR = "https://cdn-icons-png.flaticon.com/512/147/147144.png"

# --- 2. INITIALISATION ---
if 'pendientes' not in st.session_state:
    nombres = list(PARTICIPANTES.keys())
    random.shuffle(nombres)
    st.session_state.pendientes = nombres
    st.session_state.grupo_a = []
    st.session_state.grupo_b = []
    st.session_state.ultimo_asignado = None

def asignar_siguiente():
    if st.session_state.pendientes:
        nom = st.session_state.pendientes.pop(0)
        
        # Lógica para elegir grupo aleatoriamente pero respetando el límite de 5
        opciones_validas = []
        if len(st.session_state.grupo_a) < 5:
            opciones_validas.append('A')
        if len(st.session_state.grupo_b) < 5:
            opciones_validas.append('B')
            
        equipe = random.choice(opciones_validas)
        
        chemin_photo = PARTICIPANTES.get(nom, FOTO_AVATAR)
        donnees = {"nom": nom, "foto": chemin_photo}
        
        if equipe == 'A':
            st.session_state.grupo_a.append(donnees)
        else:
            st.session_state.grupo_b.append(donnees)
            
        st.session_state.ultimo_asignado = (nom, equipe)

# --- 3. INTERFACE UTILISATEUR ---
st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px #000;'>🎅 Grand Tirage de Noël 🎄</h1>", unsafe_allow_html=True)

if st.session_state.pendientes:
    prochaine = st.session_state.pendientes[0]
    
    st.markdown(f"""
        <div class='info-box'>
            <h3 style='margin:0; font-size:16px;'>Prochaine personne :</h3>
            <h2>{prochaine}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Botón centrado
    if st.button("TIRER AU SORT"):
        with st.spinner("Le Père Noël réfléchit..."):
            time.sleep(1.2)
        asignar_siguiente()
        st.snow()
        st.rerun()
else:
    st.markdown("<div class='info-box'><h2>🎉 Tirage Terminé !</h2></div>", unsafe_allow_html=True)
    if st.button("🔄 Réinitialiser"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()

# Confirmación visual del sorteo
if st.session_state.ultimo_asignado:
    nom, grupo = st.session_state.ultimo_asignado
    nom_equipe = "ÉQUIPE A 🔴" if grupo == 'A' else "ÉQUIPE B 🔵"
    st.markdown(f"<p style='text-align: center; color: white; font-size: 18px;'>✨ <b>{nom}</b> est dans l'<b>{nom_equipe}</b> ! ✨</p>", unsafe_allow_html=True)
    if not st.session_state.pendientes:
        st.balloons()

st.divider()

# --- 4. AFFICHAGE DES ÉQUIPES ---
col_a, col_b = st.columns(2)

with col_a:
    st.markdown(f"<h3 style='text-align: center; color: white; background: #E74C3C; border-radius: 10px; padding: 5px;'>🎁 ÉQUIPE A ({len(st.session_state.grupo_a)})</h3>", unsafe_allow_html=True)
    res_a = st.columns(3)
    for i, p in enumerate(st.session_state.grupo_a):
        with res_a[i % 3]:
            st.image(p["foto"])
            st.markdown(f"<p style='text-align:center; color:white; font-size:12px;'>{p['nom']}</p>", unsafe_allow_html=True)

with col_b:
    st.markdown(f"<h3 style='text-align: center; color: white; background: #3498DB; border-radius: 10px; padding: 5px;'>❄️ ÉQUIPE B ({len(st.session_state.grupo_b)})</h3>", unsafe_allow_html=True)
    res_b = st.columns(3)
    for i, p in enumerate(st.session_state.grupo_b):
        with res_b[i % 3]:
            st.image(p["foto"])
            st.markdown(f"<p style='text-align:center; color:white; font-size:12px;'>{p['nom']}</p>", unsafe_allow_html=True)
