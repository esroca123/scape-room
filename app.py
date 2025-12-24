import streamlit as st
import random
import time
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Tirage au Sort de Noël", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    /* Fondo con nieve y degradado */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), 
                    url("https://www.transparenttextures.com/patterns/snow.png"),
                    linear-gradient(to bottom, #d63031, #2d3436);
        background-attachment: fixed;
    }

    /* CENTRADO ABSOLUTO DEL BOTÓN */
    .stButton {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }

    /* Botón Circular Gigante Adaptable */
    div.stButton > button:first-child {
        margin: 0 auto !important;
        width: 200px !important;
        height: 200px !important;
        border-radius: 50% !important;
        border: 8px solid #f1c40f !important;
        background-color: #e74c3c !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        box-shadow: 0 8px #c0392b, 0 15px 20px rgba(0,0,0,0.4) !important;
        transition: all 0.2s ease;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* Recuadro de información con alto contraste */
    .info-box {
        background-color: rgba(255, 255, 255, 0.95);
        color: #2d3436 !important;
        padding: 25px;
        border-radius: 20px;
        border: 4px solid #2ecc71;
        text-align: center;
        margin: 15px auto;
        max-width: 500px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    .info-box h2 { color: #d63031 !important; font-size: 45px !important; margin: 0; }
    .info-box h3 { color: #2d3436 !important; margin-bottom: 5px; }

    /* Estilo de fotos en los equipos */
    .img-team {
        border-radius: 15px;
        border: 3px solid white;
        object-fit: cover;
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
        
        # LÓGICA DE EQUILIBRIO (4 vs 5)
        # Si un grupo ya tiene 5, el siguiente va al otro obligatoriamente
        if len(st.session_state.grupo_a) >= 5:
            equipe = 'B'
        elif len(st.session_state.grupo_b) >= 5:
            equipe = 'A'
        else:
            # Si ambos tienen espacio, azar total
            equipe = random.choice(['A', 'B'])
            
        chemin_photo = PARTICIPANTES.get(nom, FOTO_AVATAR)
        donnees = {"nom": nom, "foto": chemin_photo}
        
        if equipe == 'A':
            st.session_state.grupo_a.append(donnees)
        else:
            st.session_state.grupo_b.append(donnees)
            
        st.session_state.ultimo_asignado = (nom, equipe)

# --- 3. INTERFACE UTILISATEUR ---
st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px #000; margin-bottom: 0;'>🎅 Grand Tirage de Noël 🎄</h1>", unsafe_allow_html=True)

if st.session_state.pendientes:
    prochaine = st.session_state.pendientes[0]
    
    st.markdown(f"""
        <div class='info-box'>
            <h3>Prochaine personne :</h3>
            <h2>{prochaine}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # EL BOTÓN AHORA ESTÁ DENTRO DE UNA COLUMNA CENTRAL PARA ASEGURAR POSICIÓN
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button("TIRER AU SORT"):
            with st.spinner("Le Père Noël réfléchit..."):
                time.sleep(1.2)
            asignar_siguiente()
            st.snow()
            st.rerun()
else:
    st.markdown("<div class='info-box'><h2>🎉 Tous les lutins sont assignés !</h2></div>", unsafe_allow_html=True)
    _, col_reset, _ = st.columns([1, 1, 1])
    with col_reset:
        if st.button("🔄 Réinitialiser"):
            for key in st.session_state.keys(): del st.session_state[key]
            st.rerun()

# Resultado del último sorteo
if st.session_state.ultimo_asignado:
    nom, grupo = st.session_state.ultimo_asignado
    nom_equipe = "ÉQUIPE A 🔴" if grupo == 'A' else "ÉQUIPE B 🔵"
    st.markdown(f"<h3 style='text-align: center; color: white;'>✨ {nom} est dans l'{nom_equipe} ! ✨</h3>", unsafe_allow_html=True)
    if not st.session_state.pendientes:
        st.balloons()

st.divider()

# --- 4. AFFICHAGE DES ÉQUIPES ---
col_a, col_b = st.columns(2)

with col_a:
    st.markdown(f"<h2 style='text-align: center; color: white; background: #E74C3C; border-radius: 10px; padding: 10px;'>🎁 ÉQUIPE A ({len(st.session_state.grupo_a)})</h2>", unsafe_allow_html=True)
    res_a = st.columns(3)
    for i, p in enumerate(st.session_state.grupo_a):
        with res_a[i % 3]:
            st.image(p["foto"], use_container_width=True)
            st.markdown(f"<p style='text-align:center; color:white;'><b>{p['nom']}</b></p>", unsafe_allow_html=True)

with col_b:
    st.markdown(f"<h2 style='text-align: center; color: white; background: #3498DB; border-radius: 10px; padding: 10px;'>❄️ ÉQUIPE B ({len(st.session_state.grupo_b)})</h2>", unsafe_allow_html=True)
    res_b = st.columns(3)
    for i, p in enumerate(st.session_state.grupo_b):
        with res_b[i % 3]:
            st.image(p["foto"], use_container_width=True)
            st.markdown(f"<p style='text-align:center; color:white;'><b>{p['nom']}</b></p>", unsafe_allow_html=True)
