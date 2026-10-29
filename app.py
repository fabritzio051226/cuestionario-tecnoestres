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

# --- RECURSOS GENERALES DE APOYO ---
# Son enlaces públicos; verifica que sigan disponibles antes de publicar la aplicación.
RECURSOS_AYUDA_TECNOLOGICA = [
    ("Centro de ayuda de Microsoft", "https://support.microsoft.com/es-es"),
    ("Centro de ayuda de Google", "https://support.google.com/?hl=es"),
]
RECURSO_PSICOLOGIA = ("Directorio de psicólogos en línea de Doctoralia",
                      "https://www.doctoralia.com.mx/psicologo/online")

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
    "Primero, indica con qué frecuencia has experimentado cada situación relacionada con "
    "el uso de la tecnología. Después, responde unas preguntas breves sobre tu experiencia "
    "para recibir recomendaciones que se ajusten mejor a tus respuestas."
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

    st.markdown("### 🧭 2. Preguntas sobre tu experiencia con la tecnología")
    st.write(
        "Responde Sí o No a las preguntas de cada dimensión. Estas respuestas permiten "
        "identificar situaciones concretas y ofrecer sugerencias prácticas relacionadas "
        "con tus necesidades."
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
    st.subheader("🧭 ¿Qué significan tus puntuaciones?")
    st.write(
        "Esta sección interpreta los promedios del cuestionario y ofrece sugerencias "
        "generales para las dimensiones con puntuaciones más elevadas. Después encontrarás "
        "un plan de acción diferente, basado en tus respuestas a las preguntas sobre situaciones concretas."
    )

    # Estas interpretaciones usan los rangos provisionales de la interfaz:
    # Bajo < 2; Moderado >= 2 y < 4; Alto >= 4.
    # No son puntos de corte clínicos oficiales.
    consejos_por_dimension = {
        "Escepticismo": {
            "Alto": (
                "Tu puntuación indica que las respuestas relacionadas con el interés, la "
                "confianza o el valor que atribuyes al uso de las tecnologías fueron relativamente "
                "elevadas. Puede ayudarte identificar qué herramientas o experiencias generan "
                "esa sensación, revisar si existe una dificultad concreta y buscar una alternativa, "
                "instrucciones o soporte técnico cuando sea necesario."
            ),
            "Moderado": (
                "Algunas respuestas sugieren cierta pérdida de interés o confianza en las tecnologías. "
                "Puedes identificar qué situaciones te resultan frustrantes y buscar formas más sencillas "
                "de realizar esas tareas."
            ),
            "Bajo": (
                "Tus respuestas reflejan una menor presencia de experiencias relacionadas con esta dimensión. "
                "Mantén las prácticas que te ayudan a utilizar las tecnologías de manera útil y cómoda."
            ),
        },
        "Fatiga": {
            "Alto": (
                "Tus respuestas reflejan una presencia relativamente elevada de cansancio o dificultad "
                "para recuperarte después de utilizar tecnologías. Intenta distribuir las tareas, hacer "
                "pausas breves, alternar actividades y evitar mantener varias tareas digitales al mismo tiempo."
            ),
            "Moderado": (
                "Tus respuestas sugieren que el cansancio relacionado con el uso de tecnologías puede aparecer "
                "en algunas situaciones. Prueba a organizar las actividades por prioridad, hacer pausas y "
                "observar qué tareas te resultan más agotadoras."
            ),
            "Bajo": (
                "Tus respuestas reflejan una menor presencia de experiencias relacionadas con la fatiga. "
                "Procura mantener un ritmo de trabajo equilibrado y descansar cuando lo necesites."
            ),
        },
        "Ansiedad": {
            "Alto": (
                "Tus respuestas indican una presencia relativamente elevada de tensión, preocupación o miedo "
                "al utilizar tecnologías. Puede ayudarte practicar con funciones poco a poco, consultar "
                "instrucciones antes de realizar tareas difíciles y pedir capacitación o ayuda cuando la necesites."
            ),
            "Moderado": (
                "Tus respuestas sugieren que algunas tareas tecnológicas pueden generarte preocupación o "
                "inseguridad. Intenta practicar en un entorno seguro, utilizar guías y pedir ayuda si una tarea "
                "no te queda clara."
            ),
            "Bajo": (
                "Tus respuestas reflejan una menor presencia de experiencias relacionadas con la ansiedad "
                "al utilizar tecnologías. Continúa usando instrucciones y medidas preventivas cuando sean útiles."
            ),
        },
        "Ineficacia": {
            "Alto": (
                "Tus respuestas indican dudas relativamente elevadas sobre tu capacidad para utilizar tecnologías "
                "o completar tareas con ellas. Puedes comenzar con funciones básicas, consultar tutoriales "
                "confiables, practicar paso a paso y solicitar capacitación o asistencia cuando sea necesario."
            ),
            "Moderado": (
                "Tus respuestas sugieren que podrías tener dudas en algunas tareas tecnológicas. Practicar con "
                "una función a la vez, consultar manuales y dividir una tarea en pasos pequeños puede ayudarte "
                "a ganar confianza."
            ),
            "Bajo": (
                "Tus respuestas reflejan una menor presencia de dudas relacionadas con esta dimensión. "
                "Continúa desarrollando tus habilidades y consulta guías cuando te encuentres con herramientas nuevas."
            ),
        },
    }

    for dimension, score in promedios.items():
        if score < 2.0:
            nivel = "Bajo"
        elif score < 4.0:
            nivel = "Moderado"
        else:
            nivel = "Alto"

        with st.expander(f"{dimension}: {nivel} ({score:.1f}/6)", expanded=(nivel == "Alto")):
            st.write(consejos_por_dimension[dimension][nivel])

    st.caption(
        "Los niveles y consejos se utilizan como orientación general en esta aplicación. "
        "Los rangos bajo, moderado y alto son provisionales y no deben interpretarse como "
        "puntos de corte oficiales ni como diagnóstico psicológico."
    )

    st.divider()
    st.subheader("💡 Plan de acción según tus respuestas")
    st.write(
        "Estas recomendaciones se basan en las situaciones específicas que señalaste "
        "en las preguntas de Sí/No y complementan la interpretación de tus puntuaciones."
    )
    recomendaciones = obtener_recomendaciones(respuestas_binarias)
    for dimension, recomendacion in recomendaciones.items():
        st.info(f"**{dimension}:** {recomendacion}")

    # --- 5. OPCIONES DE APOYO CUANDO HAY RESULTADOS ALTOS ---
    dimensiones_altas = [dim for dim, score in promedios.items() if score >= 4.0]

    if dimensiones_altas:
        st.divider()
        st.subheader("🤝 ¿Necesitas ayuda? Encuentra apoyo")
        st.warning(
            "Una o más dimensiones obtuvieron un promedio de 4.0 o superior. "
            "Este aviso es orientativo y no es un diagnóstico. Puedes consultar "
            "las opciones de apoyo según la dificultad que estés experimentando."
        )
        st.markdown("**Dimensiones que conviene revisar:** " + ", ".join(dimensiones_altas))

        st.markdown("### 💻 1. Ayuda tecnológica")
        st.write(
            "Si tienes problemas con una aplicación, un programa o una herramienta digital, "
            "puedes consultar los centros de ayuda oficiales para buscar instrucciones y soluciones."
        )
        for nombre, url in RECURSOS_AYUDA_TECNOLOGICA:
            st.markdown(f"- [{nombre}]({url})")

        st.markdown("### ⏱️ 2. Bienestar y organización del uso digital")
        st.write(
            "Si sientes cansancio o sobrecarga, intenta distribuir las tareas, hacer pausas "
            "breves y evitar realizar muchas actividades al mismo tiempo. Si el problema se "
            "relaciona con una herramienta específica, busca también orientación o capacitación."
        )

        st.markdown("### 🧠 3. Apoyo psicológico profesional")
        st.write(
            "Si la ansiedad o el malestar persisten, te afectan en tus actividades diarias o "
            "sientes que necesitas hablar con alguien, puedes buscar un profesional de psicología. "
            "No es obligatorio acudir a uno por obtener una puntuación alta; es una opción de apoyo."
        )
        nombre_psicologia, url_psicologia = RECURSO_PSICOLOGIA
        st.markdown(f"- [Buscar profesionales: {nombre_psicologia}]({url_psicologia})")
        st.caption(
            "Los enlaces dirigen a sitios externos. Revisa la formación, las credenciales, "
            "la modalidad y el costo antes de elegir un servicio. El cuestionario no determina "
            "por sí solo si una persona necesita tratamiento psicológico."
        )

    st.success("La evaluación terminó. Puedes revisar tus puntajes y las recomendaciones anteriores.")

st.divider()

# --- 6. ACERCA DE ESTA EVALUACIÓN ---
st.subheader("ℹ️ Acerca de esta evaluación")

st.markdown("""
**¿Por qué hay dos grupos de preguntas?**

**1. Conocer tus experiencias con la tecnología**

Primero respondes 16 enunciados sobre la frecuencia con la que experimentas distintas
situaciones al utilizar tecnologías. Tus respuestas permiten calcular resultados en cuatro
dimensiones: escepticismo, fatiga, ansiedad e ineficacia.

**2. Comprender mejor tu situación y ofrecer recomendaciones**

Después respondes preguntas breves sobre situaciones concretas, como dificultades técnicas,
pausas durante el uso de la tecnología, errores o necesidades de capacitación. Estas respuestas
se utilizan para ofrecer recomendaciones prácticas relacionadas con cada dimensión.

**Finalidad de la herramienta**

La evaluación ofrece información y orientación inicial sobre experiencias relacionadas con el
uso de la tecnología. Los resultados no constituyen un diagnóstico psicológico ni determinan,
por sí solos, si una persona necesita tratamiento profesional.
""")
