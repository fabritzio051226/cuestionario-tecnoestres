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
    * 🧩 **Escepticismo / Ineficacia:** Sentir que no eres bueno usando la tecnología o dudar de tu capacidad para aprender nuevas herramientas.
    * 🔋 **Tecnofatiga:** Cansancio físico y mental, agotamiento o dolor de cabeza después de usar pantallas por mucho tiempo.
    * 🌬️ **Tecnoansiedad:** Sentir tensión, miedo a cometer errores o nerviosismo al usar sistemas informáticos.
    * 📱 **Tecnoadicción:** Necesidad incontrolable de estar conectado, revisar notificaciones constantemente y no poder desconectarse.
    ''')

st.divider()

# --- 2. CUESTIONARIO OPTIMIZADO ---
ESCALA = {
    0: "0 = Nunca",
    1: "1 = Casi nunca",
    2: "2 = A veces",
    3: "3 = Regularmente",
    4: "4 = Frecuentemente",
    5: "5 = Casi siempre",
    6: "6 = Siempre"
}

PREGUNTAS = {
    "Tecnoansiedad": [
        "Siento tensión y ansiedad al trabajar con tecnologías.",
        "Me asusta la idea de cometer errores al usar sistemas informáticos.",
        "Me siento intimidado/a ante los cambios en el software."
    ],
    "Tecnofatiga": [
        "Me siento agotado/a mentalmente por usar tecnologías.",
        "Siento cansancio visual o malestar físico por las pantallas.",
        "Me resulta difícil concentrarme después de horas en dispositivos."
    ],
    "Tecnoineficacia": [
        "Siento que otros son más eficientes que yo usando tecnología.",
        "Dudo de mis capacidades para adaptarme a nuevos programas.",
        "Me cuesta resolver problemas técnicos básicos."
    ],
    "Tecnoadicción": [
        "Tengo dificultades para desconectarme de la tecnología.",
        "Siento la necesidad de revisar notificaciones constantemente.",
        "Me cuesta enfocarme en una tarea sin revisar el teléfono."
    ]
}

# st.form agrupa todas las preguntas
with st.form("formulario_cuestionario"):
    st.subheader("📝 Responde el cuestionario")
    st.markdown("Selecciona con qué frecuencia experimentas cada situación:")
    
    respuestas = {}
    for dimension, lista_preguntas in PREGUNTAS.items():
        st.markdown(f"**{dimension}**")
        respuestas[dimension] = []
        for i, pregunta in enumerate(lista_preguntas):
            val = st.select_slider(
                label=f"{pregunta}",
                options=list(ESCALA.keys()),
                format_func=lambda x: ESCALA[x],
                value=0,
                key=f"{dimension}_{i}"
            )
            respuestas[dimension].append(val)
        st.write("") # Espacio
        
    submitted = st.form_submit_button("📊 Calcular Mis Resultados", type="primary")

# --- 3. MENÚ DE RESULTADOS ---
if submitted:
    st.divider()
    st.header("📊 Menú de Resultados")
    
    # Calculamos el promedio de cada dimensión
    promedios = {dim: np.mean(vals) for dim, vals in respuestas.items()}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tus Puntajes")
        for dim, score in promedios.items():
            if score < 2.0:
                estado = "🟢 Bajo (Saludable)"
            elif score < 4.0:
                estado = "🟡 Moderado (Alerta)"
            else:
                estado = "🔴 Alto (Riesgo)"
            st.markdown(f"**{dim}:** {score:.1f}/6.0  - {estado}")
            
    with col2:
        st.subheader("Gráfico de Perfil")
        # Gráfico de radar (araña)
        categorias = list(promedios.keys())
        valores = list(promedios.values())
        valores += valores[:1] 
        angulos = [n / float(len(categorias)) * 2 * np.pi for n in range(len(categorias))]
        angulos += angulos[:1]

        fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
        ax.plot(angulos, valores, color='#38B2AC', linewidth=2)
        ax.fill(angulos, valores, color='#38B2AC', alpha=0.3)
        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(categorias, fontsize=8)
        ax.set_ylim(0, 6)
        
        st.pyplot(fig)
