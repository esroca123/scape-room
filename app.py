import streamlit as st
import random
import time
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Tirage au sort des équipes", layout="wide")

# --- 1. DICTIONNAIRE DES PARTICIPANTS ---
# Note : Assurez-vous que les fichiers sont bien dans le dossier 'fotos' sur GitHub
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

# Image de secours si la photo n'est pas trouvée
FOTO_AVATAR = "https://cdn-icons-png.flaticon.com/512/147/147144.png"

# --- 2. INITIALISATION DU TIRAGE ---
if 'pendientes' not in st.session_state:
    nombres = list(PARTICIPANTES.keys())
    random.shuffle(nombres)
    st.session_state.pendientes = nombres
    st.session_state.grupo_a = []
    st.session_state.grupo_b = []
    st.session_state.ultimo_asignado = None

# --- 3. LOGIQUE DU TIRAGE ---
def asignar_siguiente():
    if st.session_state.pendientes:
        nom = st.session_state.pendientes.pop(0)
        equipe = random.choice(['A', 'B'])
        
        chemin_photo = PARTICIPANTES.get(nom, FOTO_AVATAR)
        
        # On vérifie si le fichier existe, sinon on met l'avatar
        if not os.path.exists(chemin_photo):
            chemin_photo = FOTO_AVATAR
            
        donnees = {"nom": nom, "foto": chemin_photo}
        
        if equipe == 'A':
            st.session_state.grupo_a.append(donnees)
        else:
            st.session_state.grupo_b.append(donnees)
            
        st.session_state.ultimo_asignado = f"✨ {nom} rejoint l'Équipe {equipe} !"

# --- 4. INTERFACE UTILISATEUR ---
st.title("🎲 Tirage au sort des Équipes")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    if st.session_state.pendientes:
        prochaine = st.session_state.pendientes[0]
        st.metric(label="Prochaine personne :", value=prochaine)
        
        if st.button("🎰 LANCER LA ROULETTE", type="primary", use_container_width=True):
            with st.spinner("Assignation..."):
                time.sleep(1)
                asignar_siguiente()
                st.rerun()
    else:
        st.success("🎉 Tirage terminé !")
        if st.button("Réinitialiser"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

with col2:
    if st.session_state.ultimo_asignado:
        st.info(st.session_state.ultimo_asignado)

st.divider()

# --- 5. AFFICHAGE DES RÉSULTATS ---
equipe_a, equipe_b = st.columns(2)

with equipe_a:
    st.markdown("<h2 style='text-align: center; color: #E74C3C;'>🔴 ÉQUIPE A</h2>", unsafe_allow_html=True)
    st.write("---")
    res_a = st.columns(3)
    for i, p in enumerate(st.session_state.grupo_a):
        with res_a[i % 3]:
            st.image(p["foto"], width=120)
            st.caption(f"**{p['nom']}**")

with equipe_b:
    st.markdown("<h2 style='text-align: center; color: #3498DB;'>🔵 ÉQUIPE B</h2>", unsafe_allow_html=True)
    st.write("---")
    res_b = st.columns(3)
    for i, p in enumerate(st.session_state.grupo_b):
        with res_b[i % 3]:
            st.image(p["foto"], width=120)
            st.caption(f"**{p['nom']}**")
