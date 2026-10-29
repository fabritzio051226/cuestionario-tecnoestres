import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURACIÓN E INTRODUCCIÓN ---
st.set_page_config(
    page_title="Cuestionario RED-TIC",
    page_icon="💻",
    layout="centered"
)

st.title("💻 Evaluación de Tecnoestrés (RED-TIC)")

st.markdown("### 📚 ¿Qué es el Tecnoestrés y cuáles son sus tipos?")
st.markdown("""
El **Tecnoestrés** es un estado psicológico negativo relacionado con el uso de las
Tecnologías de la Información y la Comunicación (TIC). Puede aparecer cuando sentimos
que las demandas tecnológicas superan nuestra capacidad para manejarlas.

**Se divide en 4 dimensiones principales:**
* 🧩 **Escepticismo:** sentir rechazo o desconfianza hacia la tecnología.
* 🔋 **Fatiga:** sentir cansancio después de utilizar tecnologías.
* 🌬️ **Ansiedad:** sentir tensión o miedo al utilizar tecnologías.
* 🎯 **Ineficacia:** dudar de la propia capacidad para utilizar tecnologías.
""")

st.divider()

# --- 2. ESCALAS Y PREGUNTAS ---
ESCALA_LIKERT = {
    0: "0 = Nada / Nunca",
    1: "1 = Casi nada",
    2: "2 = Raramente",
    3: "3 = Algunas veces",
    4: "4 = Bastante",
    5: "5 = Con frecuencia",
    6: "6 = Siempre"
}
ESCALA_BINARIA = ["Seleccionar...", "No", "Sí"]

# Los 16 ítems RED-TIC, agrupados en las cuatro dimensiones.
PREGUNTAS_REDTIC = {
    "Escepticismo": [
        "Con el paso del tiempo, las tecnologías me interesan cada vez menos.",
        "Cada vez me siento menos implicado en el uso de las TIC.",
        "Soy más cínico respecto de la contribución de las tecnologías en mi trabajo.",
        "Dudo del significado del trabajo con estas tecnologías."
    ],
    "Fatiga": [
        "Me resulta difícil relajarme después de un día de trabajo utilizándolas.",
        "Cuando termino de trabajar con TIC, me siento agotado/a.",
        "Estoy tan cansado/a cuando acabo trabajar con ellas que no puedo hacer nada más.",
        "Es difícil concentrarme después de trabajar con tecnologías."
    ],
    "Ansiedad": [
        "Me siento tenso y ansioso al trabajar con tecnologías.",
        "Me asusta pensar que puedo destruir una gran cantidad de información por el uso inadecuado de las mismas.",
        "Dudo a la hora de utilizar TIC por miedo a cometer errores.",
        "El trabajar con ellas me hace sentir incómodo, irritable e impaciente."
    ],
    "Ineficacia": [
        "En mi opinión, soy ineficaz utilizando tecnologías.",
        "Es difícil trabajar con tecnologías de la información y de la comunicación.",
        "La gente dice que soy ineficaz utilizando tecnologías.",
        "Estoy inseguro de acabar bien mis tareas cuando utilizo las TIC."
    ]
}

# Todas las preguntas Sí/No del árbol de la imagen están en esta página.
# Se muestran juntas para que la persona no tenga que navegar entre pestañas.
PREGUNTAS_ARBOL = {
    "Escepticismo": [
        "¿Una experiencia negativa provocó rechazo a la tecnología?",
        "¿La causa fue una falla del sistema?",
        "¿Recibe apoyo para resolverlo?"
    ],
    "Fatiga": [
        "¿Usas las TIC durante muchas horas?",
        "¿Realiza pausas durante la jornada?",
        "¿Trabaja con muchas tareas a la vez?"
    ],
    "Ansiedad": [
        "¿Ha tenido errores al usar la tecnología?",
        "¿Los errores generan tensión o miedo?",
        "¿Existe otra causa de rechazo?"
    ],
    "Ineficacia": [
        "¿Considera insuficientes sus conocimientos?",
        "¿Ha recibido capacitación adecuada?",
        "¿Usa tutoriales o guías?"
    ]
}

st.markdown("### 📝 1. Cuestionario RED-TIC")
st.write(
    "Responde los 16 enunciados según tu experiencia. Después contesta las preguntas "
    "Sí/No del árbol de decisiones que aparece más abajo."
)

with st.form("formulario_cuestionario"):
    respuestas_likert = {}
    numero_item = 1

    for dimension, lista_preguntas in PREGUNTAS_REDTIC.items():
        st.markdown(f"#### {dimension}")
        respuestas_likert[dimension] = []
        for pregunta in lista_preguntas:
            val = st.select_slider(
                f"{numero_item}. {pregunta}",
                options=list(ESCALA_LIKERT.keys()),
                value=0,
                format_func=lambda x: ESCALA_LIKERT[x],
                key=f"redtic_{numero_item}"
            )
            respuestas_likert[dimension].append(val)
            numero_item += 1
        st.divider()

    st.markdown("### 🌳 2. Preguntas del árbol de decisiones")
    st.write(
        "Contesta todas las preguntas de cada dimensión. Algunas solo se utilizan "
        "si la respuesta anterior activa esa parte del árbol."
    )

    respuestas_binarias = {}
    for dimension, lista_preguntas in PREGUNTAS_ARBOL.items():
        st.markdown(f"#### {dimension}")
        respuestas_binarias[dimension] = []
        for i, pregunta in enumerate(lista_preguntas):
            val = st.radio(
                pregunta,
                options=ESCALA_BINARIA,
                horizontal=True,
                index=0,
                key=f"arbol_{dimension}_{i}"
            )
            respuestas_binarias[dimension].append(val)
        st.divider()

    submitted = st.form_submit_button(
        "📊 Calcular resultados y recomendaciones",
        type="primary"
    )

# --- 3. FUNCIONES PARA APLICAR EL ÁRBOL DE LA IMAGEN ---
def obtener_recomendaciones(respuestas):
    recomendaciones = {}

    # A. Escepticismo
    esc = respuestas["Escepticismo"]
    rechazo, falla, apoyo = esc
    if rechazo == "No":
        recomendaciones["Escepticismo"] = "Usar una alternativa."
    elif rechazo == "Sí":
        if falla == "No":
            recomendacion_inicial = "Recibir soporte técnico."
        elif falla == "Sí":
            recomendacion_inicial = "Buscar orientación."
        else:
            recomendacion_inicial = None

        if recomendacion_inicial is not None:
            if apoyo == "No":
                recomendaciones["Escepticismo"] = "Reducir uso innecesario."
            elif apoyo == "Sí":
                recomendaciones["Escepticismo"] = "Cambiar rutina de uso."
            else:
                recomendaciones["Escepticismo"] = recomendacion_inicial
        else:
            recomendaciones["Escepticismo"] = "Falta responder si la causa fue una falla del sistema."

    # B. Fatiga
    fat = respuestas["Fatiga"]
    muchas_horas, pausas, multitarea = fat
    if muchas_horas == "Sí":
        if pausas == "No":
            recomendaciones["Fatiga"] = "Establecer pausas."
        elif pausas == "Sí":
            recomendaciones["Fatiga"] = "Organizar tareas."
        else:
            recomendaciones["Fatiga"] = "Falta responder si realiza pausas durante la jornada."
    elif muchas_horas == "No":
        if multitarea == "No":
            recomendaciones["Fatiga"] = "Alternar actividad."
        elif multitarea == "Sí":
            recomendaciones["Fatiga"] = "Cambiar rutina de uso."
        else:
            recomendaciones["Fatiga"] = "Reducir tiempo continuo. Falta responder si trabaja con muchas tareas a la vez."
    else:
        recomendaciones["Fatiga"] = "Falta responder si usa las TIC durante muchas horas."

    # C. Ansiedad
    ans = respuestas["Ansiedad"]
    errores, tension, otra_causa = ans
    if errores == "Sí":
        if tension == "No":
            recomendaciones["Ansiedad"] = "Recibir capacitación."
        elif tension == "Sí":
            recomendaciones["Ansiedad"] = "Solicitar apoyo."
        else:
            recomendaciones["Ansiedad"] = "Falta responder si los errores generan tensión o miedo."
    elif errores == "No":
        if otra_causa == "No":
            recomendaciones["Ansiedad"] = "Usar instrucciones."
        elif otra_causa == "Sí":
            recomendaciones["Ansiedad"] = "Cambiar rutina de uso."
        else:
            recomendaciones["Ansiedad"] = "Practicar antes de usar. Falta responder si existe otra causa de rechazo."
    else:
        recomendaciones["Ansiedad"] = "Falta responder si ha tenido errores al usar la tecnología."

    # D. Ineficacia
    inef = respuestas["Ineficacia"]
    conocimientos, capacitacion, tutoriales = inef
    if conocimientos == "Sí":
        if capacitacion == "No":
            recomendaciones["Ineficacia"] = "Recibir capacitación."
        elif capacitacion == "Sí":
            recomendaciones["Ineficacia"] = "Solicitar asistencia."
        else:
            recomendaciones["Ineficacia"] = "Falta responder si ha recibido capacitación adecuada."
    elif conocimientos == "No":
        if tutoriales == "No":
            recomendaciones["Ineficacia"] = "Practicar con el sistema."
        elif tutoriales == "Sí":
            recomendaciones["Ineficacia"] = "Cambiar rutina de uso."
        else:
            recomendaciones["Ineficacia"] = "Consultar manual. Falta responder si usa tutoriales o guías."
    else:
        recomendaciones["Ineficacia"] = "Falta responder si considera insuficientes sus conocimientos."

    return recomendaciones


# --- 4. RESULTADOS ---
if submitted:
    st.header("📊 Resultados y plan de acción")

    # Validación de las respuestas Sí/No necesarias para recorrer cada rama.
    errores_formulario = []
    for dimension, respuestas in respuestas_binarias.items():
        for pregunta, respuesta in zip(PREGUNTAS_ARBOL[dimension], respuestas):
            # Algunas preguntas de seguimiento pueden no aplicar a esa ruta.
            # No bloqueamos todo el formulario: las recomendaciones indicarán si falta un dato.
            pass

    promedios = {
        dim: float(np.mean(valores))
        for dim, valores in respuestas_likert.items()
    }

    st.subheader("Tus puntajes por dimensión")
    col1, col2 = st.columns([1, 1])

    with col1:
        for dim, score in promedios.items():
            if score < 2.0:
                estado = "🟢 Bajo"
            elif score < 4.0:
                estado = "🟡 Moderado"
            else:
                estado = "🔴 Alto"
            st.markdown(f"**{dim}:** {score:.1f}/6.0 — {estado}")

    with col2:
        categorias = list(promedios.keys())
        valores = list(promedios.values())
        valores_cerrados = valores + valores[:1]
        angulos = [n / float(len(categorias)) * 2 * np.pi for n in range(len(categorias))]
        angulos_cerrados = angulos + angulos[:1]

        fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
        ax.plot(angulos_cerrados, valores_cerrados, linewidth=2)
        ax.fill(angulos_cerrados, valores_cerrados, alpha=0.25)
        ax.set_xticks(angulos)
        ax.set_xticklabels(categorias, fontsize=8)
        ax.set_ylim(0, 6)
        ax.set_title("Gráfico de perfil")
        st.pyplot(fig)
        plt.close(fig)

    tabla = pd.DataFrame({
        "Dimensión": list(promedios.keys()),
        "Promedio (0–6)": [round(v, 2) for v in promedios.values()]
    })
    st.dataframe(tabla, use_container_width=True, hide_index=True)

    st.caption(
        "Los niveles bajo, moderado y alto son una clasificación orientativa usada en esta "
        "interfaz; no deben presentarse como diagnóstico clínico ni como puntos de corte "
        "oficiales sin verificar la versión del manual utilizada."
    )

    st.divider()
    st.subheader("💡 Plan de acción personalizado")
    st.write("Las recomendaciones siguen las rutas del árbol de decisiones de la imagen.")

    recomendaciones = obtener_recomendaciones(respuestas_binarias)
    for dimension, recomendacion in recomendaciones.items():
        st.info(f"**{dimension}:** {recomendacion}")

    # --- 5. CONTACTO DE APOYO CUANDO HAY RESULTADOS ALTOS ---
    dimensiones_altas = [dim for dim, score in promedios.items() if score >= 4.0]

    if dimensiones_altas:
        st.divider()
        st.subheader("📞 Contacto de apoyo")
        st.warning(
            "Una o más dimensiones obtuvieron un promedio de 4.0 o superior. "
            "Este aviso es orientativo, no es un diagnóstico. Si necesitas ayuda, "
            "puedes contactar a las áreas de apoyo de tu institución."
        )
        st.markdown("**Dimensiones que conviene revisar:** " + ", ".join(dimensiones_altas))
        st.markdown("""
        - **Soporte técnico:** agrega aquí el correo o teléfono real del área de soporte.
        - **Orientación académica:** agrega aquí el contacto real de tu institución.
        - **Atención psicológica:** agrega aquí el contacto oficial, si tu institución lo ofrece.
        """)
        st.caption(
            "Antes de entregar o publicar la aplicación, reemplaza estos textos por los "
            "datos reales de contacto. No se han inventado correos ni teléfonos."
        )

    st.success("La evaluación terminó. Puedes revisar tus puntajes y las recomendaciones anteriores.")

st.divider()
st.caption(
    "La aplicación es informativa y educativa. El cuestionario RED-TIC y el árbol de decisiones "
    "son elementos distintos: el primero recoge respuestas de frecuencia y el segundo orienta "
    "recomendaciones según respuestas Sí/No."
)
