import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Evaluación RED-TIC - Tecnoestrés", page_icon="💻", layout="wide"
)

st.title("💻 Cuestionario de Tecnoestrés (Modelo RED-TIC)")
st.markdown(
    """
Este cuestionario evalúa la presencia de **tecnoestrés** en tus actividades diarias. 
Responde a cada afirmación seleccionando la frecuencia con la que experimentas cada situación.
"""
)

# --- ESCALA LIKERT ---
ESCALA = {
    0: "0 = Nunca / Casi nunca",
    1: "1 = Algunas veces al año",
    2: "2 = Una vez al mes",
    3: "3 = Algunas veces al mes",
    4: "4 = Una vez a la semana",
    5: "5 = Algunas veces a la semana",
    6: "6 = Siempre / Todos los días",
}

# --- PREGUNTAS POR DIMENSIÓN ---
PREGUNTAS = {
    "Tecnoansiedad": [
        "Siento tensión y ansiedad al trabajar con tecnologías de la información.",
        "Me asusta la idea de cometer errores o perder información al usar sistemas informáticos.",
        "Me siento intimidado/a ante los cambios en el software o herramientas digitales.",
    ],
    "Tecnofatiga": [
        "Al finalizar la jornada me siento agotado/a mentalmente por haber usado tecnologías.",
        "Siento cansancio visual, dolores de cabeza o malestar físico por el uso de pantallas.",
        "Me resulta difícil concentrarme después de horas trabajando con dispositivos electrónicos.",
    ],
    "Tecnoineficacia": [
        "Siento que otros compañeros son mucho más eficientes que yo utilizando las TIC.",
        "Dudo de mis capacidades para adaptarme a los nuevos programas informáticos.",
        "Me cuesta resolver problemas técnicos básicos cuando ocurren en mi equipo.",
    ],
    "Tecnoadicción": [
        "Tengo dificultades para desconectarme de la tecnología fuera del horario laboral/académico.",
        "Siento la necesidad imperiosa de revisar mis notificaciones o correos constantemente.",
        "Me cuesta enfocarme en una tarea sin revisar el teléfono o pestañas secundarias.",
    ],
}

# --- FORMULARIO DE CAPTURA ---
with st.form("red_tic_form"):
    st.subheader("📋 Registro de Evaluación")

    col_user, col_dept = st.columns(2)
    with col_user:
        nombre = st.text_input("Nombre / ID de Usuario", value="Usuario 01")
    with col_dept:
        departamento = st.text_input(
            "Área / Departamento / Escuela", value="General"
        )

    st.divider()

    respuestas = {}
    for dimension, lista_preguntas in PREGUNTAS.items():
        st.markdown(f"### 🔹 Dimension: **{dimension}**")
        respuestas[dimension] = []

        for i, pregunta in enumerate(lista_preguntas):
            val = st.select_slider(
                label=f"**{i+1}.** {pregunta}",
                options=list(ESCALA.keys()),
                format_func=lambda x: ESCALA[x],
                value=0,
                key=f"{dimension}_{i}",
            )
            respuestas[dimension].append(val)

        st.write("")

    submitted = st.form_submit_button(
        "📊 Procesar y Obtener Resultados", type="primary"
    )

# --- PROCESAMIENTO Y RESULTADOS ---
if submitted:
    st.divider()
    st.header("📈 Reporte de Resultados RED-TIC")

    # Cálculo de promedios
    promedios = {dim: np.mean(vals) for dim, vals in respuestas.items()}

    col_res1, col_res2 = st.columns([1, 1])

    with col_res1:
        st.subheader("Niveles por Dimensión (Escala 0 - 6)")
        df_promedios = pd.DataFrame(
            list(promedios.items()), columns=["Dimensión", "Puntaje Promedio"]
        )

        def diagnosticar(score):
            if score < 2.0:
                return "🟢 Bajo / Saludable"
            elif score < 4.0:
                return "🟡 Moderado / Alerta"
            else:
                return "🔴 Alto / Riesgo de Tecnoestrés"

        df_promedios["Nivel de Riesgo"] = df_promedios["Puntaje Promedio"].apply(
            diagnosticar
        )
        st.dataframe(df_promedios.style.format({"Puntaje Promedio": "{:.2f}"}))

    # --- GRÁFICO DE RADAR ---
    with col_res2:
        st.subheader("Perfil de Tecnoestrés")

        categorias = list(promedios.keys())
        valores = list(promedios.values())
        valores += valores[:1]  # Cerrar el polígono

        angulos = [n / float(len(categorias)) * 2 * np.pi for n in range(len(categorias))]
        angulos += angulos[:1]

        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        ax.plot(angulos, valores, linewidth=2, linestyle="solid", color="#d9534f")
        ax.fill(angulos, valores, color="#d9534f", alpha=0.25)

        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(categorias, fontsize=10)
        ax.set_ylim(0, 6)

        st.pyplot(fig)

    # --- RECOMENDACIONES ---
    st.subheader("💡 Recomendaciones y Plan de Acción")
    for dim, score in promedios.items():
        if score >= 4.0:
            if dim == "Tecnoansiedad":
                st.error(
                    "**Alta Tecnoansiedad:** Se recomienda capacitación técnica progresiva y ambientes de prueba seguros sin temor al error."
                )
            elif dim == "Tecnofatiga":
                st.error(
                    "**Alta Tecnofatiga:** Implementa la regla 20-20-20 (descansar la vista cada 20 minutos) y pausas activas durante la jornada."
                )
            elif dim == "Tecnoineficacia":
                st.error(
                    "**Alta Tecnoineficacia:** Refuerza las competencias digitales básicas con tutorías personalizadas."
                )
            elif dim == "Tecnoadicción":
                st.error(
                    "**Alta Tecnoadicción:** Establece protocolos claros de desconexión digital al finalizar el horario lectivo/laboral."
                )
