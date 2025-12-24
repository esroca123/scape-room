import streamlit as st
import random
import time
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Tirage au Sort de Noël", layout="wide")

# --- ESTILOS CSS (CENTRAR BOTÓN Y CONTRASTE) ---
st.markdown("""
    <style>
    /* Fondo con nieve y degradado */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), 
                    url("https://www.transparenttextures.com/patterns/snow.png"),
                    linear-gradient(to bottom, #d63031, #2d3436);
        background-attachment: fixed;
    }

    /* Contenedor para centrar el botón en móvil */
    .flex-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px 0;
    }

    /* Botón Circular Gigante Adaptable */
    div.stButton > button:first-child {
        display: block;
        margin: 0 auto !important;
        width: 180px !important;
        height: 180px !important;
        border-radius: 50% !important;
        border: 8px solid #f1c40f !important;
        background-color: #e74c3c !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        box-shadow: 0 8px #c0392b, 0 15px 20px rgba(0,0,0,0.4) !important;
        transition: all 0.2s ease;
    }

    /* Recuadro de información con alto contraste */
    .info-box {
        background-color: rgba(255, 255, 255, 0.9);
        color: #2d3436 !important;
        padding: 20px;
        border-radius: 15px;
        border: 4px solid #2ecc71;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    .info-box h2, .info-box h3 {
        color: #d63031 !important;
    }

    /* Estilo de fotos en los equipos */
    .img-team {
        border-radius: 50%;
        border: 3px solid white;
        object-fit: cover;
        width: 100px;
        height: 100px;
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
        equipe = random.choice(['A', 'B'])
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
    
    # Recuadro de quién sigue (Texto oscuro sobre fondo claro)
    st.markdown(f"""
        <div class='info-box'>
            <h3>Prochaine personne à passer :</h3>
            <h2 style='font-size: 40px;'>{prochaine}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Contenedor para centrar el botón
    st.markdown("<div class='flex-container'>", unsafe_allow_html=True)
    if st.button("TIRER AU SORT"):
        with st.spinner("Le Père Noël réfléchit..."):
            time.sleep(1.5)
        asignar_siguiente()
        st.snow()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='info-box'><h2>🎉 Tous les lutins sont assignés !</h2></div>", unsafe_allow_html=True)
    if st.button("🔄 Réinitialiser"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()

# Resultado del último sorteo
if st.session_state.ultimo_asignado:
    nom, grupo = st.session_state.ultimo_asignado
    nom_equipe = "ÉQUIPE A 🔴" if grupo == 'A' else "ÉQUIPE B 🔵"
    st.markdown(f"""
        <div style='text-align: center; color: white; padding: 10px;'>
            <h3>✨ {nom} a rejoint {nom_equipe} ! ✨</h3>
        </div>
    """, unsafe_allow_html=True)
    if not st.session_state.pendientes:
        st.balloons()

st.divider()

# --- 4. AFFICHAGE DES ÉQUIPES ---
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("<h2 style='text-align: center; color: white; background: #E74C3C; border-radius: 10px; padding: 10px;'>🎁 ÉQUIPE A</h2>", unsafe_allow_html=True)
    res_a = st.columns(3)
    for i, p in enumerate(st.session_state.grupo_a):
        with res_a[i % 3]:
            # Usamos st.image directamente para mayor compatibilidad de rutas
            st.image(p["foto"], use_container_width=True)
            st.markdown(f"<p style='text-align:center; color:white;'><b>{p['nom']}</b></p>", unsafe_allow_html=True)

with col_b:
    st.markdown("<h2 style='text-align: center; color: white; background: #3498DB; border-radius: 10px; padding: 10px;'>❄️ ÉQUIPE B</h2>", unsafe_allow_html=True)
    res_b = st.columns(3)
    for i, p in enumerate(st.session_state.grupo_b):
        with res_b[i % 3]:
            st.image(p["foto"], use_container_width=True)
            st.markdown(f"<p style='text-align:center; color:white;'><b>{p['nom']}</b></p>", unsafe_allow_html=True)
