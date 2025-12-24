import streamlit as st
import random
import time
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Tirage au sort des équipes", layout="wide")

# --- 1. DICTIONNAIRE DES PARTICIPANTS ---
PARTICIPANTES = {
    "ROSE": "fotos/ROSE.jpg",
    "MARIE": "fotos/MARIE.jpg",
    "CARL": "fotos/CARL.jpg",
    "NATALIE": "fotos/NATALIE.jpg",
    "MARC": "fotos/MARC.jpg",
    "HELENE": "fotos/HELENE.jpg",
    "REGEAN": "fotos/REGEAN.jpg",
    "CHARLOT": "fotos/CHARLOT.jpg",
    "LOUIS": "fotos/LOUIS.jpg"
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
        if not os.path.exists(chemin_photo):
            chemin_photo = FOTO_AVATAR
        donnees = {"nom": nom, "foto": chemin_photo}
        if equipe == 'A':
            st.session_state.grupo_a.append(donnees)
        else:
            st.session_state.grupo_b.append(donnees)
        st.session_state.ultimo_asignado = f"✨ {nom} rejoint l'Équipe {equipe} !"

# --- 3. INTERFACE UTILISATEUR ---
st.title("🎲 Tirage au sort des Équipes")
st.markdown("---")

col_control, col_info = st.columns([1, 2])
with col_control:
    if st.session_state.pendientes:
        prochaine = st.session_state.pendientes[0]
        st.metric(label="Prochaine personne :", value=prochaine)
        if st.button("🎰 LANCER LA ROULETTE", type="primary", use_container_width=True):
            asignar_siguiente()
            st.rerun()
    else:
        st.success("🎉 Tirage terminé !")
        if st.button("Réinitialiser"):
            for key in st.session_state.keys(): del st.session_state[key]
            st.rerun()

with col_info:
    if st.session_state.ultimo_asignado:
        st.info(st.session_state.ultimo_asignado)

st.divider()

# --- 4. AFFICHAGE DES ÉQUIPES CON DIVISIÓN ---
# Creamos las columnas pero añadimos un estilo de borde vertical
col_a, col_espacio, col_b = st.columns([10, 1, 10])

with col_a:
    st.markdown("<h2 style='text-align: center; color: #E74C3C;'>🔴 ÉQUIPE A</h2>", unsafe_allow_html=True)
    st.markdown("<div style='border-bottom: 2px solid #E74C3C; margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    res_a = st.columns(3)
    for i, p in enumerate(st.session_state.grupo_a):
        with res_a[i % 3]:
            st.image(p["foto"], width=120)
            st.caption(f"**{p['nom']}**")

# Esta columna vacía actúa como el separador visual
with col_espacio:
    st.markdown("""
        <div style='border-left: 2px solid #ddd; height: 500px; margin: auto; width: 1px;'></div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("<h2 style='text-align: center; color: #3498DB;'>🔵 ÉQUIPE B</h2>", unsafe_allow_html=True)
    st.markdown("<div style='border-bottom: 2px solid #3498DB; margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    res_b = st.columns(3)
    for i, p in enumerate(st.session_state.grupo_b):
        with res_b[i % 3]:
            st.image(p["foto"], width=120)
            st.caption(f"**{p['nom']}**")
