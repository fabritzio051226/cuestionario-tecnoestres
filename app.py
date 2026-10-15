import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Ecosistema de Bienestar RED-TIC", page_icon="🌿", layout="centered")

# --- CSS PERSONALIZADO (ECOSISTEMA AGRADABLE Y PSICOLÓGICO) ---
st.markdown("""
<style>
    /* Fondo principal suave y relajante (tonos menta/crema) */
    .stApp {
        background-color: #F4F8F6;
    }
    
    /* Tipografía y colores de encabezados */
    h1, h2, h3 {
        color: #3C5A53 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Estilo de los textos normales */
    p {
        color: #4A4A4A;
        font-size: 1.1rem;
    }

    /* Contenedores para las preguntas simulando tarjetas limpias */
    div[role="radiogroup"] {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        margin-bottom: 15px;
    }

    /* Separador suave */
    hr {
        border-top: 1px solid #D5E2DC;
    }
</style>
""", unsafe_allow_html=True)

# --- ENCABEZADO ---
st.title("🌿 Bienestar Digital: Ecosistema RED-TIC")
st.markdown("### *Un espacio seguro para entender y mejorar tu relación con la tecnología.*")
st.markdown("Este sistema te guiará paso a paso para encontrar la mejor solución a lo que estás experimentando, priorizando tu salud mental y eficiencia.")
st.divider()

# --- SELECTOR PRINCIPAL ---
st.markdown("#### ¿Qué sensación describe mejor tu experiencia actual con la tecnología?")
dimension = st.selectbox(
    "Selecciona una dimensión para comenzar:",
    [
        "Elige una opción...", 
        "A) Escepticismo (Siento rechazo o desconfianza)", 
        "B) Fatiga (Siento cansancio extremo o agotamiento)", 
        "C) Ansiedad (Siento tensión, miedo o nerviosismo)", 
        "D) Ineficacia (Siento que me faltan conocimientos)"
    ]
)

st.write("") # Espaciador

# --- LÓGICA DEL DIAGRAMA RED-TIC ---

# A) ESCEPTICISMO
if dimension.startswith("A)"):
    st.markdown("### 🧩 Analizando tu Escepticismo")
    q1 = st.radio("**¿Una experiencia negativa provocó este rechazo?**", ["Seleccionar", "No", "Sí"], horizontal=True)
    
    if q1 == "No":
        st.success("✨ **Acción Recomendada:** Usar una alternativa tecnológica con la que te sientas más cómodo/a.")
    
    elif q1 == "Sí":
        q2 = st.radio("**¿La causa fue una falla del sistema?**", ["Seleccionar", "No", "Sí"], horizontal=True)
        
        if q2 == "No":
            st.info("💡 **Primer paso:** Es recomendable recibir soporte técnico general.")
            q3 = st.radio("**¿Recibes apoyo para resolver este problema?**", ["Seleccionar", "No", "Sí"], horizontal=True, key="apoyo_no")
            if q3 == "No":
                st.success("✨ **Acción Recomendada:** Reducir el uso innecesario de esa tecnología para evitar frustración.")
            elif q3 == "Sí":
                st.success("✨ **Acción Recomendada:** Cambiar tu rutina de uso e integrar la tecnología poco a poco.")
                
        elif q2 == "Sí":
            st.info("💡 **Primer paso:** Es importante buscar orientación específica sobre esa falla.")
            q3 = st.radio("**¿Recibes apoyo para resolver este problema?**", ["Seleccionar", "No", "Sí"], horizontal=True, key="apoyo_si")
            if q3 == "No":
                st.success("✨ **Acción Recomendada:** Reducir el uso innecesario de esa tecnología.")
            elif q3 == "Sí":
                st.success("✨ **Acción Recomendada:** Cambiar tu rutina de uso apoyándote en la orientación recibida.")

# B) FATIGA
elif dimension.startswith("B)"):
    st.markdown("### 🔋 Analizando tu Fatiga Digital")
    q1 = st.radio("**¿Usas las TIC (tecnologías) durante muchas horas?**", ["Seleccionar", "No", "Sí"], horizontal=True)
    
    if q1 == "No":
        st.info("💡 **Primer paso:** Intenta reducir el tiempo continuo frente a la pantalla.")
        q2 = st.radio("**¿Trabajas con muchas tareas a la vez (Multitasking)?**", ["Seleccionar", "No", "Sí"], horizontal=True)
        if q2 == "No":
            st.success("✨ **Acción Recomendada:** Alternar la actividad (cambiar entre tareas digitales y físicas).")
        elif q2 == "Sí":
            st.success("✨ **Acción Recomendada:** Cambiar tu rutina de uso para enfocarte en una cosa a la vez.")
            
    elif q1 == "Sí":
        q2 = st.radio("**¿Realizas pausas durante tu jornada?**", ["Seleccionar", "No", "Sí"], horizontal=True)
        if q2 == "No":
            st.success("✨ **Acción Recomendada:** Establecer pausas activas obligatorias (ej. regla 20-20-20).")
        elif q2 == "Sí":
            st.success("✨ **Acción Recomendada:** Organizar mejor tus tareas para que las pausas sean más efectivas.")

# C) ANSIEDAD
elif dimension.startswith("C)"):
    st.markdown("### 🌬️ Analizando tu Ansiedad")
    q1 = st.radio("**¿Has tenido errores al usar la tecnología recientemente?**", ["Seleccionar", "No", "Sí"], horizontal=True)
    
    if q1 == "No":
        st.info("💡 **Sugerencia:** Intenta practicar en un entorno seguro antes de usarla para tareas importantes.")
        q2 = st.radio("**¿Existe otra causa personal o externa de rechazo?**", ["Seleccionar", "No", "Sí"], horizontal=True)
        if q2 == "No":
            st.success("✨ **Acción Recomendada:** Usar instrucciones detalladas paso a paso para ganar confianza.")
        elif q2 == "Sí":
            st.success("✨ **Acción Recomendada:** Cambiar la rutina de uso y adaptar la herramienta a tus necesidades.")
            
    elif q1 == "Sí":
        q2 = st.radio("**¿Estos errores te generan tensión o miedo?**", ["Seleccionar", "No", "Sí"], horizontal=True)
        if q2 == "No":
            st.success("✨ **Acción Recomendada:** Recibir capacitación para no volver a cometer esos errores.")
        elif q2 == "Sí":
            st.success("✨ **Acción Recomendada:** Solicitar apoyo directo. No enfrentes el problema solo/a.")

# D) INEFICACIA
elif dimension.startswith("D)"):
    st.markdown("### 🎯 Analizando tu Ineficacia Percibida")
    q1 = st.radio("**¿Consideras insuficientes tus conocimientos actuales?**", ["Seleccionar", "No", "Sí"], horizontal=True)
    
    if q1 == "No":
        st.info("💡 **Sugerencia:** Tal vez solo sea falta de costumbre. Puedes consultar el manual.")
        q2 = st.radio("**¿Sueles usar tutoriales o guías de ayuda?**", ["Seleccionar", "No", "Sí"], horizontal=True)
        if q2 == "No":
            st.success("✨ **Acción Recomendada:** Practicar con el sistema de forma libre y sin presión.")
        elif q2 == "Sí":
            st.success("✨ **Acción Recomendada:** Cambiar tu rutina de uso y aplicar lo aprendido en los tutoriales.")
            
    elif q1 == "Sí":
        q2 = st.radio("**¿Has recibido una capacitación adecuada para tu puesto/tarea?**", ["Seleccionar", "No", "Sí"], horizontal=True)
        if q2 == "No":
            st.success("✨ **Acción Recomendada:** Recibir capacitación formal y estructurada.")
        elif q2 == "Sí":
            st.success("✨ **Acción Recomendada:** Solicitar asistencia técnica o mentoría para resolver dudas específicas.")
