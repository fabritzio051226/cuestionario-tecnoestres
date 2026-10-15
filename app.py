import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURACIÓN E INTRODUCCIÓN ---
st.set_page_config(page_title="Cuestionario RED-TIC", page_icon="💻", layout="centered")

st.title("💻 Evaluación de Tecnoestrés (RED-TIC)")

# NUEVO: Menú desplegable con la explicación
with st.expander("📚 ¿Qué es el Tecnoestrés y cuáles son sus tipos? (Haz clic para leer)"):
    st.markdown('''
    El **Tecnoestrés** es un estado psicológico negativo relacionado con el uso de las Tecnologías de la Información y la Comunicación (TIC). Ocurre cuando sentimos que las demandas tecnológicas superan nuestra capacidad para manejarlas.
    
    **Se divide en 4 tipos principales:**
    * 🧩 **Escepticismo:** Sentir rechazo o desconfianza hacia la tecnología, a menudo por experiencias negativas previas.
    * 🔋 **Fatiga:** Cansancio físico y mental extremo, derivado de largas jornadas frente a pantallas o multitarea.
    * 🌬️ **Ansiedad:** Sentir tensión, miedo a cometer errores o nerviosismo al enfrentarse a herramientas digitales.
    * 🎯 **Ineficacia:** Sentir que los conocimientos actuales son insuficientes o dudar de la capacidad para aprender nuevos programas.
    ''')

st.divider()

# --- 2. CUESTIONARIO INTEGRADO ---
# Usamos dos escalas: Una Likert para frecuencia y una Binaria (Sí/No) para el árbol de decisiones.

ESCALA_LIKERT = {
    0: "0 = Nunca",
    1: "1 = Casi nunca",
    2: "2 = A veces",
    3: "3 = Regularmente",
    4: "4 = Frecuentemente",
    5: "5 = Casi siempre",
    6: "6 = Siempre"
}

ESCALA_BINARIA = ["Seleccionar...", "No", "Sí"]

# Combinamos las preguntas clásicas RED-TIC con las preguntas del árbol de decisiones.
PREGUNTAS = {
    "Escepticismo": [
        ("Siento tensión y ansiedad al trabajar con tecnologías.", "likert"),
        ("¿Una experiencia negativa provocó rechazo a la tecnología?", "binaria"),
        ("¿La causa del rechazo fue una falla del sistema?", "binaria")
    ],
    "Fatiga": [
        ("Me siento agotado/a mentalmente por usar tecnologías.", "likert"),
        ("¿Usas las TIC durante muchas horas seguidas?", "binaria"),
        ("¿Trabajas con muchas tareas a la vez?", "binaria")
    ],
    "Ansiedad": [
        ("Me asusta la idea de cometer errores al usar sistemas informáticos.", "likert"),
        ("¿Has tenido errores al usar la tecnología?", "binaria"),
        ("¿Los errores te generan tensión o miedo?", "binaria")
    ],
    "Ineficacia": [
        ("Dudo de mis capacidades para adaptarme a nuevos programas.", "likert"),
        ("¿Consideras insuficientes tus conocimientos actuales?", "binaria"),
        ("¿Has recibido capacitación adecuada para usarlas?", "binaria")
    ]
}

# st.form agrupa todas las preguntas
with st.form("formulario_cuestionario"):
    st.subheader("📝 Responde el cuestionario")
    st.markdown("Combina preguntas sobre la frecuencia de tus sensaciones y situaciones específicas de tu entorno:")
    
    respuestas_likert = {}
    respuestas_binarias = {}
    
    for dimension, lista_preguntas in PREGUNTAS.items():
        st.markdown(f"### **{dimension}**")
        respuestas_likert[dimension] = []
        respuestas_binarias[dimension] = []
        
        for i, (pregunta, tipo) in enumerate(lista_preguntas):
            if tipo == "likert":
                val = st.select_slider(
                    label=f"**{pregunta}**",
                    options=list(ESCALA_LIKERT.keys()),
                    format_func=lambda x: ESCALA_LIKERT[x],
                    value=0,
                    key=f"{dimension}_{i}_likert"
                )
                respuestas_likert[dimension].append(val)
            elif tipo == "binaria":
                val = st.radio(
                    f"**{pregunta}**",
                    options=ESCALA_BINARIA,
                    horizontal=True,
                    key=f"{dimension}_{i}_binaria"
                )
                respuestas_binarias[dimension].append(val)
        st.divider()
        
    submitted = st.form_submit_button("📊 Calcular Mis Resultados", type="primary")

# --- 3. MENÚ DE RESULTADOS Y DIAGNÓSTICO ---
if submitted:
    st.header("📊 Menú de Resultados y Plan de Acción")
    
    # 1. Calcular el promedio de las preguntas Likert
    promedios = {dim: np.mean(vals) for dim, vals in respuestas_likert.items()}
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Tus Puntajes (Severidad)")
        for dim, score in promedios.items():
            if score < 2.0:
                estado = "🟢 Bajo"
            elif score < 4.0:
                estado = "🟡 Moderado"
            else:
                estado = "🔴 Alto"
            st.markdown(f"**{dim}:** {score:.1f}/6.0  - {estado}")
            
    with col2:
        st.subheader("Gráfico de Perfil")
        # Gráfico de radar (araña)
        categorias = list(promedios.keys())
        valores = list(promedios.values())
        valores += valores[:1] 
        angulos = [n / float(len(categorias)) * 2 * np.pi for n in range(len(categorias))]
        angulos += angulos[:1]

        fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(polar=True))
        ax.plot(angulos, valores, color='#38B2AC', linewidth=2)
        ax.fill(angulos, valores, color='#38B2AC', alpha=0.3)
        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(categorias, fontsize=8)
        ax.set_ylim(0, 6)
        
        st.pyplot(fig)
        
    st.divider()
    
    # 2. Generar recomendaciones basadas en el árbol de decisiones (Preguntas Binarias)
    st.subheader("💡 Plan de Acción Personalizado")
    st.markdown("Basado en tus respuestas específicas:")
    
    # Escepticismo
    esc_ans = respuestas_binarias["Escepticismo"]
    if esc_ans[0] == "Sí":
        if esc_ans[1] == "Sí":
            st.info("🧩 **Escepticismo:** Como la causa fue una falla del sistema, es vital buscar orientación específica y soporte técnico antes de volver a usar la herramienta.")
        elif esc_ans[1] == "No":
            st.info("🧩 **Escepticismo:** Tu rechazo proviene de una experiencia negativa no relacionada al sistema. Considera usar una alternativa tecnológica con la que te sientas cómodo/a.")
            
    # Fatiga
    fat_ans = respuestas_binarias["Fatiga"]
    if fat_ans[0] == "Sí":
        st.warning("🔋 **Fatiga:** Usas la tecnología muchas horas seguidas. Implementa pausas obligatorias organizando mejor tus tareas.")
    elif fat_ans[0] == "No" and fat_ans[1] == "Sí":
        st.warning("🔋 **Fatiga:** La multitarea te está agotando. Intenta alternar actividades y enfocarte en una sola cosa a la vez.")
        
    # Ansiedad
    ans_ans = respuestas_binarias["Ansiedad"]
    if ans_ans[0] == "Sí":
        if ans_ans[1] == "Sí":
            st.error("🌬️ **Ansiedad:** Los errores te generan tensión. Es importante que solicites apoyo directo para no enfrentar el problema solo/a.")
        elif ans_ans[1] == "No":
            st.error("🌬️ **Ansiedad:** Para evitar futuros errores, solicita recibir capacitación formal.")
            
    # Ineficacia
    inef_ans = respuestas_binarias["Ineficacia"]
    if inef_ans[0] == "Sí":
        if inef_ans[1] == "No":
            st.info("🎯 **Ineficacia:** Sientes que te faltan conocimientos y no has recibido capacitación. Solicita recibir capacitación formal estructurada.")
        elif inef_ans[1] == "Sí":
            st.info("🎯 **Ineficacia:** Sientes ineficacia a pesar de estar capacitado. Solicita asistencia técnica para resolver dudas puntuales.")

