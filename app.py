import streamlit as st
import random
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Sorteo de Equipos Pro", layout="wide")

# --- 1. DICCIONARIO DE PARTICIPANTES (EDITA AQUÍ) ---
# Estructura: "Nombre": "fotos/nombre_archivo.ext"
PARTICIPANTES = {
    "ROSE": "fotos/ROSE.jpg",
    "MARIE": "fotos/MARIE.jpg",
    "CARL": "fotos/CARL.jpg",
    "NATALIE": "fotos/NATALIE.jpg",
    "MARC": "fotos/MARC.jpg",
    "HELENE": "fotos/HELENE.jpg"
    "REGEAN": "fotos/REGEAN.jpg",
    "CHARLOT": "fotos/CHARLOT.jpg"
    "LOUIS": "fotos/LOUIS.jpg",
   
}

# Imagen de respaldo por si falla la ruta de alguna foto
FOTO_AVATAR = "https://cdn-icons-png.flaticon.com/512/147/147144.png"
BANNER_EQUIPO_A = "fotos/equipo_a_banner.png" # Si no tienes, se saltará
BANNER_EQUIPO_B = "fotos/equipo_b_banner.png" # Si no tienes, se saltará

# --- 2. INICIALIZACIÓN DE LA MEMORIA (SESSION STATE) ---
if 'pendientes' not in st.session_state:
    nombres = list(PARTICIPANTES.keys())
    random.shuffle(nombres) # Mezcla inicial para que no sea siempre el mismo orden
    st.session_state.pendientes = nombres
    st.session_state.grupo_a = []
    st.session_state.grupo_b = []
    st.session_state.ultimo_asignado = None

# --- 3. FUNCIONES ---
def asignar_siguiente():
    if st.session_state.pendientes:
        nombre_persona = st.session_state.pendientes.pop(0)
        equipo_destino = random.choice(['A', 'B'])
        
        datos = {
            "nombre": nombre_persona,
            "foto": PARTICIPANTES.get(nombre_persona, FOTO_AVATAR)
        }
        
        if equipo_destino == 'A':
            st.session_state.grupo_a.append(datos)
        else:
            st.session_state.grupo_b.append(datos)
        
        st.session_state.ultimo_asignado = f"¡{nombre_persona} va al Equipo {equipo_destino}!"

# --- 4. INTERFAZ DE USUARIO ---
st.title("🎲 Sorteo de Grupos con Fotos")
st.markdown("---")

# Zona de acción
col_izq, col_der = st.columns([1, 2])

with col_izq:
    if st.session_state.pendientes:
        proximo = st.session_state.pendientes[0]
        st.metric(label="Siguiente persona:", value=proximo)
        
        if st.button("🎰 GIRAR RULETA", type="primary", use_container_width=True):
            with st.spinner("Asignando..."):
                time.sleep(1) # Efecto de suspenso
                asignar_siguiente()
                st.rerun()
    else:
        st.success("🎉 ¡Sorteo Completado!")
        if st.button("Reiniciar Sorteo"):
            for key in st.session_state.keys(): del st.session_state[key]
            st.rerun()

with col_der:
    if st.session_state.ultimo_asignado:
        st.info(st.session_state.ultimo_asignado)

st.divider()

# --- 5. VISUALIZACIÓN DE EQUIPOS ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🔴 EQUIPO A")
    # Intentar cargar banner de equipo
    try: st.image(BANNER_EQUIPO_A, use_container_width=True)
    except: st.write("---")
    
    # Cuadrícula de fotos para el Equipo A
    filas_a = st.columns(4)
    for i, persona in enumerate(st.session_state.grupo_a):
        with filas_a[i % 4]:
            try:
                st.image(persona["foto"], caption=persona["nombre"], use_container_width=True)
            except:
                st.image(FOTO_AVATAR, caption=f"{persona['nombre']} (Sin foto)", use_container_width=True)

with col_b:
    st.subheader("🔵 EQUIPO B")
    # Intentar cargar banner de equipo
    try: st.image(BANNER_EQUIPO_B, use_container_width=True)
    except: st.write("---")
    
    # Cuadrícula de fotos para el Equipo B
    filas_b = st.columns(4)
    for i, persona in enumerate(st.session_state.grupo_b):
        with filas_b[i % 4]:
            try:
                st.image(persona["foto"], caption=persona["nombre"], use_container_width=True)
            except:
                st.image(FOTO_AVATAR, caption=f"{persona['nombre']} (Sin foto)", use_container_width=True)
