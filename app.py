import streamlit as st
import random
import time
import os

# --- CONFIGURACIÓN DE LA PAGE ---
st.set_page_config(page_title="Sorteo Navideño Noel", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS (NAVIDAD Y BOTÓN) ---
st.markdown("""
    <style>
    /* Fondo de la aplicación */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), 
                    url("https://www.transparenttextures.com/patterns/snow.png"),
                    linear-gradient(to bottom, #d63031, #2d3436);
        background-attachment: fixed;
    }

    /* Botón Circular Gigante */
    div.stButton > button:first-child {
        display: block;
        margin: 0 auto;
        width: 200px;
        height: 200px;
        border-radius: 50%;
        border: 10px solid #f1c40f;
        background-color: #e74c3c;
        color: white;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 10px #c0392b, 0 20px 30px rgba(0,0,0,0.5);
        transition: all 0.2s ease;
        text-transform: uppercase;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #ff7675;
        transform: scale(1.05);
    }

    div.stButton > button:first-child:active {
        box-shadow: 0 5px #c0392b, 0 10px 15px rgba(0,0,0,0.5);
        transform: translateY(5px);
    }

    /* Tarjetas de fotos */
    .img-card {
        border-radius: 50%;
        border: 4px solid #2ecc71;
        transition: transform 0.5s;
    }
    
    .img-card:hover {
        transform: rotate(10deg);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. DICCIONARIO DE PARTICIPANTES ---
PARTICIPANTES = {
    "ROSE": "fotos/ROSE.jpeg",
    "MARIE": "fotos/MARIE.jpeg",
    "CARL": "fotos/CARL.jpeg",
    "NATALIE": "fotos/NATALIE.jpeg",
    "MARC": "fotos/MARC.jpeg",
    "HELENE": "fotos/HELENE.jpeg",
    "REGEAN": "fotos/REGEAN.jpeg",
    "CHARLOT": "fotos/CHARLOT.jpeg",
    "LOUIS": "fotos/LOUIS.jpeg"
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
    st.session_state.mostrar_animacion = False

def asignar_siguiente():
    if st.session_state.pendientes:
        nom = st.session_state.pendientes.pop(0)
        equipe = random.choice(['A', 'B'])
        chemin_photo = PARTICIPANTES.get(nom, FOTO_AVATAR)
        
        # Simular emoción
        st.session_state.mostrar_animacion = True
        
        donnees = {"nom": nom, "foto": chemin_photo}
        if equipe == 'A':
            st.session_state.grupo_a.append(donnees)
        else:
            st.session_state.grupo_b.append(donnees)
        st.session_state.ultimo_asignado = (nom, equipe)

# --- 3. INTERFACE UTILISATEUR ---
st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px #000;'>🎅 Gran Sorteo de Navidad Noel 🎄</h1>", unsafe_allow_html=True)

# ESPACIO PARA EL BOTÓN CENTRAL
st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.pendientes:
    prochaine = st.session_state.pendientes[0]
    
    # Mostrar quién sigue con estilo
    st.markdown(f"<h3 style='text-align: center; color: white;'>Siguiente en pasar: <br><span style='font-size: 50px;'>{prochaine}</span></h3>", unsafe_allow_html=True)
    
    if st.button("SORTEAR"):
        with st.spinner("🎅 Santa está decidiendo..."):
            time.sleep(2) # Tiempo de suspenso
        asignar_siguiente()
        st.snow() # ¡Efecto de nieve al elegir!
        st.rerun()
else:
    st.success("🎉 ¡Todos los regalos... digo, personas, están asignadas!")
    if st.button("🔄 Reiniciar Navidad"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()

# Mostrar mensaje de último asignado con globos si es final
if st.session_state.ultimo_asignado:
    nom, grupo = st.session_state.ultimo_asignado
    color = "#E74C3C" if grupo == 'A' else "#3498DB"
    st.markdown(f"<div style='text-align: center; padding: 20px; background: white; border-radius: 15px; border: 5px solid {color};'><h2>✨ {nom} ahora es del Equipo {grupo} ✨</h2></div>", unsafe_allow_html=True)
    if not st.session_state.pendientes:
        st.balloons()

st.markdown("<br><hr>", unsafe_allow_html=True)

# --- 4. AFFICHAGE DES ÉQUIPES ---
col_a, col_espacio, col_b = st.columns([10, 1, 10])

with col_a:
    st.markdown("<h2 style='text-align: center; color: white; background: #E74C3C; border-radius: 10px;'>🎁 EQUIPO A (Rojos)</h2>", unsafe_allow_html=True)
    res_a = st.columns(3)
    for i, p in enumerate(st.session_state.grupo_a):
        with res_a[i % 3]:
            st.markdown(f"""
                <div style='text-align: center;'>
                    <img src='https://cdn-icons-png.flaticon.com/512/3893/3893071.png' width='30'><br>
                    <img src='app/{p["foto"]}' class='img-card' style='width: 100px; height: 100px; object-fit: cover;'>
                    <p style='color: white;'><b>{p['nom']}</b></p>
                </div>
            """, unsafe_allow_html=True)

with col_b:
    st.markdown("<h2 style='text-align: center; color: white; background: #3498DB; border-radius: 10px;'>❄️ EQUIPO B (Azules)</h2>", unsafe_allow_html=True)
    res_b = st.columns(3)
    for i, p in enumerate(st.session_state.grupo_b):
        with res_b[i % 3]:
            st.markdown(f"""
                <div style='text-align: center;'>
                    <img src='https://cdn-icons-png.flaticon.com/512/642/642000.png' width='30'><br>
                    <img src='app/{p["foto"]}' class='img-card' style='width: 100px; height: 100px; object-fit: cover;'>
                    <p style='color: white;'><b>{p['nom']}</b></p>
                </div>
            """, unsafe_allow_html=True)
