import streamlit as st
import random
import time
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Tirage au sort des équipes", layout="wide")

# --- 1. DICTIONNAIRE DES PARTICIPANTS ---
# Vérifiez bien l'extension (.jpg ou .png) et les majuscules
PARTICIPANTS = {
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

# Image par défaut si le fichier n'est pas trouvé
FOTO_AVATAR = "https://cdn-icons-png.flaticon.com/512/147/147144.png"

# --- 2. INITIALISATION DE LA MÉMOIRE (SESSION STATE) ---
if 'pendientes' not in st.session_state:
    nombres = list(PARTICIPANTES.keys())
    random.shuffle(nombres)
    st.session_state.pendientes = nombres
    st.session_state.grupo_a = []
    st.session_state.grupo_b = []
    st.session_state.ultimo_asignado = None

# --- 3. FONCTIONS ---
def asignar_siguiente():
    if st.session_state.pendientes:
        nombre_persona = st.session_state.pendientes.pop(0)
        equipo_destino = random.choice(['A', 'B'])
        
        ruta_foto = PARTICIPANTES.get(nombre_persona)
        
        # Vérification si le fichier existe sur le serveur
        if not os.path.exists(ruta_foto):
            ruta_foto = FOTO_AVATAR
        
        datos = {
            "nombre": nombre_persona,
            "foto": ruta_foto
        }
        
        if equipo_destino == 'A':
            st.session_state.grupo_a.append(datos)
        else:
            st.session_state.grupo_b.append(datos)
        
        st.session_state.ultimo_asignado = f"¡{nombre_persona} rejoint l'Équipe {equipo_destino}!"

# --- 4. INTERFACE UTILISATEUR (FRANÇAIS) ---
st.title("🎲 Tirage au sort des Équipes")
st.markdown("---")

col_izq, col_der = st.columns([1, 2])

with col_izq:
    if st.session_state.pendientes:
        proximo = st.session_state.pendientes[0]
        st.metric(label="Prochaine personne:", value=proximo)
        
        if st.button("🎰 LANCER LA ROULETTE", type="primary", use_container_width=True):
            with st.spinner("Assignation en cours..."):
                time.sleep(1)
                asignar_siguiente()
                st.rerun()
    else:
        st.success("🎉 Tirage au sort terminé !")
        if st.button("Réinitialiser le tirage"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

with col_der:
    if st.session_state.ultimo_asignado:
        st.info(st.session_state.ultimo_asignado)

st.divider()

# --- 5. AFFICHAGE DES ÉQUIPES ---
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("<h2 style='text-align: center; color: #E74C3C;'>🔴 ÉQUIPE A</h2>", unsafe_allow_html=True)
    st.write("---")
    
    filas_a = st.columns(3)
    for i, persona in enumerate(st.session_state.grupo_a):
        with filas_a[i % 3]:
            st.image(persona["foto"], width=150)
            st.caption(f"**{persona['nombre']}**")

with col_b:
    st.markdown("<h2 style='text-align: center; color: #3498DB;'>🔵 ÉQUIPE B</h2>", unsafe_allow_html=True)
    st.write("---")
    
    filas_b = st.columns(3)
    for i, persona in enumerate(st.session_state.grupo_b):
        with filas_b[i % 3]:
            st.image(persona["foto"], width=150)
            st.caption(f"**{persona['nombre']}**")
