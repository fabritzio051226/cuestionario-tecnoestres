import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="RED-TIC Ecosistema", page_icon="🍃", layout="centered")

# --- CSS AVANZADO (GLASSMORPHISM Y MINIMALISMO) ---
st.markdown('''
<style>
    /* Ocultar elementos por defecto de Streamlit para look de App nativa */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Fondo degradado moderno y limpio */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%) !important;
    }

    /* Tipografía elegante y forzar colores oscuros para evitar problemas con el Modo Oscuro */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #2D3748 !important;
    }

    /* Diseño de tarjetas (Glassmorphism) para las preguntas */
    div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        padding: 25px !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        box-shadow: 0 10px 30px 0 rgba(31, 38, 135, 0.05) !important;
        margin-bottom: 15px !important;
        transition: transform 0.2s ease-in-out !important;
    }
    div[role="radiogroup"]:hover {
        transform: translateY(-2px) !important;
    }

    /* Tabs modernos e integrados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background-color: transparent;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff !important;
        border-radius: 30px !important;
        padding: 10px 20px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
        transition: all 0.3s ease !important;
        color: #2D3748 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #38B2AC !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(56, 178, 172, 0.3) !important;
    }
    
    /* Alertas y resultados */
    .stAlert {
        border-radius: 16px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04) !important;
    }
    
    /* Forzar color oscuro en elementos de Streamlit */
    .stMarkdown p {
        color: #4A5568 !important;
    }
</style>
''', unsafe_allow_html=True)

# --- ENCABEZADO MINIMALISTA ---
st.markdown("<h1 style='text-align: center; color: #2D3748 !important;'>🍃 Ecosistema RED-TIC</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; margin-bottom: 2rem; color: #4A5568 !important;'>Navega directamente por tus sensaciones y encuentra soluciones al instante.</p>", unsafe_allow_html=True)

# --- TABS (ACCESO INMEDIATO, SIN PASOS EXTRA) ---
t_escep, t_fatiga, t_ans, t_inef = st.tabs(["🧩 Escepticismo", "🔋 Fatiga", "🌬️ Ansiedad", "🎯 Ineficacia"])

# --- 🧩 ESCEPTICISMO ---
with t_escep:
    st.write("")
    q1_a = st.radio("**¿Una experiencia negativa provocó este rechazo a la tecnología?**", ["Seleccionar...", "No", "Sí"], horizontal=True, key="a1")
    
    if q1_a == "No":
        st.success("✨ **Solución:** Intenta usar una alternativa tecnológica con la que te sientas más cómodo/a.")
    elif q1_a == "Sí":
        q2_a = st.radio("**¿La causa fue una falla del sistema?**", ["Seleccionar...", "No", "Sí"], horizontal=True, key="a2")
        
        if q2_a == "No":
            st.info("💡 **Dato:** Es recomendable recibir soporte técnico general.")
            q3_a = st.radio("**¿Recibes apoyo para resolverlo?**", ["Seleccionar...", "No", "Sí"], horizontal=True, key="a3_no")
            if q3_a == "No":
                st.success("✨ **Solución:** Reducir el uso innecesario de la herramienta.")
            elif q3_a == "Sí":
                st.success("✨ **Solución:** Cambiar tu rutina de uso y apoyarte en el equipo.")
        elif q2_a == "Sí":
            st.info("💡 **Dato:** Debes buscar orientación específica para esa falla.")
            q3_a2 = st.radio("**¿Recibes apoyo para resolverlo?**", ["Seleccionar...", "No", "Sí"], horizontal=True, key="a3_si")
            if q3_a2 == "No":
                st.success("✨ **Solución:** Reducir el uso innecesario hasta que haya solución.")
            elif q3_a2 == "Sí":
                st.success("✨ **Solución:** Cambiar rutina de uso mientras lo resuelven.")

# --- 🔋 FATIGA ---
with t_fatiga:
    st.write("")
    q1_b = st.radio("**¿Usas la tecnología durante muchas horas seguidas?**", ["Seleccionar...", "No", "Sí"], horizontal=True, key="b1")
    
    if q1_b == "No":
        st.info("💡 Intenta reducir tu tiempo continuo.")
        q2_b = st.radio("**¿Trabajas con muchas tareas a la vez?**", ["Seleccionar...", "No", "Sí"], horizontal=True, key="b2_no")
        if q2_b == "No":
            st.success("✨ **Solución:** Alternar tu actividad (intercambiar tareas digitales con físicas).")
        elif q2_b == "Sí":
            st.success("✨ **Solución:** Cambiar rutina de uso. Enfócate en una sola cosa a la vez.")
    elif q1_b == "Sí":
        q2_b2 = st.radio("**¿Realizas pausas durante la jornada?**", ["Seleccionar...", "No", "Sí"], horizontal=True, key="b2_si")
        if q2_b2 == "No":
            st.success("✨ **Solución:** Establecer pausas obligatorias periódicamente.")
        elif q2_b2 == "Sí":
            st.success("✨ **Solución:** Organizar mejor tus tareas para no saturarte.")

# --- 🌬️ ANSIEDAD ---
with t_ans:
    st.write("")
    q1_c = st.radio("**¿Has tenido errores al usar la tecnología?**", ["Seleccionar...", "No", "Sí"], horizontal=True, key="c1")
    
    if q1_c == "No":
        st.info("💡 Practica en un entorno seguro antes de tareas clave.")
        q2_c = st.radio("**¿Existe otra causa de rechazo?**", ["Seleccionar...", "No", "Sí"], horizontal=True, key="c2_no")
        if q2_c == "No":
            st.success("✨ **Solución:** Usar instrucciones o manuales paso a paso.")
        elif q2_c == "Sí":
            st.success("✨ **Solución:** Cambiar la rutina de uso.")
    elif q1_c == "Sí":
        q2_c2 = st.radio("**¿Los errores te generan tensión o miedo?**", ["Seleccionar...", "No", "Sí"], horizontal=True, key="c2_si")
        if q2_c2 == "No":
            st.success("✨ **Solución:** Recibir capacitación para evitar esos errores.")
        elif q2_c2 == "Sí":
            st.success("✨ **Solución:** Solicitar apoyo. No cargues con la presión solo/a.")

# --- 🎯 INEFICACIA ---
with t_inef:
    st.write("")
    q1_d = st.radio("**¿Consideras insuficientes tus conocimientos?**", ["Seleccionar...", "No", "Sí"], horizontal=True, key="d1")
    
    if q1_d == "No":
        st.info("💡 Consultar el manual técnico podría refrescar tu memoria.")
        q2_d = st.radio("**¿Sueles usar tutoriales o guías?**", ["Seleccionar...", "No", "Sí"], horizontal=True, key="d2_no")
        if q2_d == "No":
            st.success("✨ **Solución:** Practicar más con el sistema.")
        elif q2_d == "Sí":
            st.success("✨ **Solución:** Cambiar rutina de uso integrando lo aprendido.")
    elif q1_d == "Sí":
        q2_d2 = st.radio("**¿Has recibido capacitación adecuada?**", ["Seleccionar...", "No", "Sí"], horizontal=True, key="d2_si")
        if q2_d2 == "No":
            st.success("✨ **Solución:** Recibir capacitación formal.")
        elif q2_d2 == "Sí":
            st.success("✨ **Solución:** Solicitar asistencia técnica especializada.")
