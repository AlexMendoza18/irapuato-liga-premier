import streamlit as st
import pandas as pd
import datetime

# Configuración de página con la identidad del Club Deportivo Irapuato
st.set_page_config(
    page_title="Club Deportivo Irapuato — Plataforma de Gestión (v2.0)",
    page_icon="⚽",
    layout="wide"
)

# Estilos CSS personalizados (Rojo Fresa y Azul)
st.markdown("""
<style>
    .main-header {
        font-size: 26px; font-weight: bold; color: #DA291C;
        text-align: center; padding: 12px; border-bottom: 3px solid #002D62; margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F8F9FA; padding: 15px; border-radius: 8px;
        border-left: 5px solid #002D62; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>⚽ CLUB DEPORTIVO IRAPUATO — LIGA PREMIER SERIE B (PLATAFORMA v2.0)</div>", unsafe_allow_html=True)

# Menú de navegación
st.sidebar.title("Menú de Gestión")
opcion = st.sidebar.radio(
    "Módulos del Sistema:",
    [
        "📋 Plantilla y Minutos Totales",
        "📍 Citaciones y Sedes de Partido",
        "⏱️ Control de Minutos por Partido",
        "⚽ Análisis Táctico, Rival y Reporte",
        "🖼️ Plan de Sesiones y Ejercicios",
        "📊 Control de Fatiga (RPE)"
    ]
)

# Base de datos en memoria
if 'jugadores' not in st.session_state:
    st.session_state.jugadores = pd.DataFrame([
        {"Dorsal": 1, "Nombre": "Gerardo Aguilar", "Posicion": "Portero", "Estado": "Disponible", "Telefono": "462-123-4567", "Contacto_Emergencia": "María Aguilar (462-987-6543)", "Talla_m": 1.88, "Peso_kg": 81.0, "Caracteristicas": "Liderazgo, juego aéreo, gran alcance bajo palos"},
        {"Dorsal": 4, "Nombre": "Carlos Pérez", "Posicion": "Defensa Central", "Estado": "Disponible", "Telefono": "462-234-5678", "Contacto_Emergencia": "Juan Pérez (462-876-5432)", "Talla_m": 1.84, "Peso_kg": 78.5, "Caracteristicas": "Marcaje fiero, buen cabeceo ofensivo, salida limpia"},
        {"Dorsal": 10, "Nombre": "Luis Fernando Gómez", "Posicion": "Mediocampista Ofensivo", "Estado": "Disponible", "Telefono": "462-456-7890", "Contacto_Emergencia": "Pedro Gómez (462-654-3210)", "Talla_m": 1.72, "Peso_kg": 68.0, "Caracteristicas": "Visión de juego, último pase, especialista en balón parado"}
    ])

if 'citaciones' not in st.session_state:
    st.session_state.citaciones = pd.DataFrame([
        {"ID": "J01", "Jornada": "Jornada 1", "Fecha": "2026-10-10", "Hora_Partido": "16:00", "Rival": "Aguacateros de Peribán", "Sede_Estadio": "Estadio Sergio León Chávez (Local)", "Ubicacion": "Irapuato, Gto.", "Hora_Cita": "14:00", "Salida_Autobus": "N/A (Local)", "Uniforme": "Rojo Fresa / Azul", "Estado": "Programado"},
        {"ID": "J02", "Jornada": "Jornada 2", "Fecha": "2026-10-17", "Hora_Partido": "12:00", "Rival": "Ayama FC", "Sede_Estadio": "Estadio Municipal de Ayama (Visitante)", "Ubicacion": "Ayama, Jal.", "Hora_Cita": "07:30", "Salida_Autobus": "08:00 A.M.", "Uniforme": "Blanco / Rojo", "Estado": "Programado"}
    ])

if 'minutos_log' not in st.session_state:
    st.session_state.minutos_log = pd.DataFrame([
        {"ID_Partido": "J01", "Fecha": "2026-10-10", "Jugador": "Gerardo Aguilar", "Posicion": "Portero", "Minutos": 90, "Condicion": "Titular", "Goles": 0, "Asistencias": 0, "Amarillas": 0, "Rojas": 0},
        {"ID_Partido": "J01", "Fecha": "2026-10-10", "Jugador": "Carlos Pérez", "Posicion": "Defensa Central", "Minutos": 90, "Condicion": "Titular", "Goles": 0, "Asistencias": 0, "Amarillas": 1, "Rojas": 0},
        {"ID_Partido": "J01", "Fecha": "2026-10-10", "Jugador": "Luis Fernando Gómez", "Posicion": "Mediocampista Ofensivo", "Minutos": 90, "Condicion": "Titular", "Goles": 1, "Asistencias": 0, "Amarillas": 0, "Rojas": 0}
    ])

if 'reportes_partido' not in st.session_state:
    st.session_state.reportes_partido = pd.DataFrame([
        {"ID_Partido": "J01", "Rival": "Aguacateros de Peribán", "Sistema_Irapuato": "1-4-3-3", "Sistema_Rival": "1-4-4-2", "Analisis_Rival": "Peligrosos a balón parado.", "Plan_Juego": "Presión alta tras pérdida.", "Marcador": "CD Irapuato 2 - 1 Aguacateros", "Resultado": "Victoria", "Resumen": "Dominio del balón. Gol de tiro libre de Luis Gómez.", "MVP": "Luis Fernando Gómez"}
    ])

# 1. Módulo: Plantilla y Minutos
if opcion == "📋 Plantilla y Minutos Totales":
    st.subheader("📋 Plantilla Oficial y Minutos Acumulados")
    df_min_tot = st.session_state.minutos_log.groupby("Jugador")["Minutos"].sum().reset_index()
    df_min_tot.columns = ["Nombre", "Minutos_Acumulados"]
    df_full = pd.merge(st.session_state.jugadores, df_min_tot, on="Nombre", how="left").fillna({"Minutos_Acumulados": 0})
    
    col1, col2 = st.columns([1, 2])
    with col1:
        jug_sel = st.selectbox("Seleccionar Jugador:", df_full["Nombre"].tolist())
        d_jug = df_full[df_full["Nombre"] == jug_sel].iloc[0]
        st.markdown(f"""
        <div class='metric-card'>
            <h4>#{int(d_jug['Dorsal'])} — {d_jug['Nombre']}</h4>
            <p><b>Posición:</b> {d_jug['Posicion']} | <b>Estado:</b> {d_jug['Estado']}</p>
            <p><b>Minutos Acumulados:</b> <span style='font-size:18px; font-weight:bold; color:#002D62;'>{int(d_jug['Minutos_Acumulados'])} min</span></p>
            <p><b>Teléfono:</b> {d_jug['Telefono']}</p>
            <p><b>Contacto Emergencia:</b> {d_jug['Contacto_Emergencia']}</p>
            <p><b>Perfil Táctico:</b> {d_jug['Caracteristicas']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.dataframe(df_full[["Dorsal", "Nombre", "Posicion", "Estado", "Talla_m", "Peso_kg", "Minutos_Acumulados"]], use_container_width=True)

# 2. Módulo: Citaciones y Sedes
elif opcion == "📍 Citaciones y Sedes de Partido":
    st.subheader("📍 Citaciones a Partido y Logística de Sede")
    st.dataframe(st.session_state.citaciones, use_container_width=True)

# 3. Módulo: Control de Minutos
elif opcion == "⏱️ Control de Minutos por Partido":
    st.subheader("⏱️ Registro e Historial de Minutos Jugados")
    col_reg, col_hist = st.columns([1, 2])
    with col_reg:
        with st.form("form_minutos"):
            part_sel = st.selectbox("Partido / Jornada:", st.session_state.citaciones["ID"].tolist())
            jug_sel = st.selectbox("Jugador:", st.session_state.jugadores["Nombre"].tolist())
            min_j = st.number_input("Minutos Jugados:", 0, 120, 90)
            cond = st.selectbox("Condición:", ["Titular", "Suplente", "No Jugó"])
            goles = st.number_input("Goles:", 0, 10, 0)
            asist = st.number_input("Asistencias:", 0, 10, 0)
            if st.form_submit_button("Guardar Minutos"):
                nuevo_m = pd.DataFrame([{"ID_Partido": part_sel, "Fecha": str(datetime.date.today()), "Jugador": jug_sel, "Posicion": "Campo", "Minutos": min_j, "Condicion": cond, "Goles": goles, "Asistencias": asist, "Amarillas": 0, "Rojas": 0}])
                st.session_state.minutos_log = pd.concat([st.session_state.minutos_log, nuevo_m], ignore_index=True)
                st.success("¡Minutos guardados!")
                st.rerun()
    with col_hist:
        st.dataframe(st.session_state.minutos_log, use_container_width=True)

# 4. Módulo: Análisis Táctico y Reporte
elif opcion == "⚽ Análisis Táctico, Rival y Reporte":
    st.subheader("⚽ Sistema de Juego, Análisis del Rival y Reporte Post-Partido")
    st.dataframe(st.session_state.reportes_partido, use_container_width=True)
    with st.form("form_reporte"):
        id_p = st.selectbox("Jornada:", st.session_state.citaciones["ID"].tolist())
        riv = st.text_input("Rival:", "Aguacateros de Peribán")
        sis_ira = st.selectbox("Sistema Irapuato:", ["1-4-3-3", "1-4-2-3-1", "1-3-5-2", "1-4-4-2"])
        marcador = st.text_input("Marcador Final:", "CD Irapuato 2 - 1 Rival")
        mvp = st.text_input("MVP del Partido:", "Luis Fernando Gómez")
        if st.form_submit_button("Guardar Reporte"):
            nuevo_r = pd.DataFrame([{"ID_Partido": id_p, "Rival": riv, "Sistema_Irapuato": sis_ira, "Sistema_Rival": "1-4-4-2", "Analisis_Rival": "-", "Plan_Juego": "-", "Marcador": marcador, "Resultado": "Victoria", "Resumen": "-", "MVP": mvp}])
            st.session_state.reportes_partido = pd.concat([st.session_state.reportes_partido, nuevo_r], ignore_index=True)
            st.success("¡Reporte Táctico Guardado!")
            st.rerun()

# 5. Módulo: Plan de Sesiones
elif opcion == "🖼️ Plan de Sesiones y Ejercicios":
    st.subheader("🖼️ Comunicación de Ejercicios Tácticos")
    st.image("https://via.placeholder.com/600x350.png?text=Esquema+Táctico+Irapuato", use_container_width=True)

# 6. Módulo: Control RPE
elif opcion == "📊 Control de Fatiga (RPE)":
    st.subheader("📊 Control Diario RPE")
    st.dataframe(st.session_state.rpe_log, use_container_width=True)
