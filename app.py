import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Evaluación de Tecnoestrés", page_icon="🧠", layout="wide")
st.title("🧠 Evaluación de Tecnoestrés")
st.write("Aplicación con el cuestionario RED-TIC y el árbol de decisiones de las dimensiones Escepticismo, Fatiga, Ansiedad e Ineficacia.")
st.info("Esta herramienta es educativa y orientativa; no sustituye una evaluación psicológica profesional.")

# Cambia estos marcadores por datos oficiales de tu institución antes de publicar la aplicación.
CONTACTOS_APOYO = {
    "Soporte técnico": "Agregar correo o teléfono institucional",
    "Orientación académica": "Agregar correo o teléfono institucional",
    "Atención psicológica": "Agregar correo o teléfono institucional",
}

ESCALA = {
    0: "0 — Nada / Nunca",
    1: "1 — Casi nada / Un par de veces al año",
    2: "2 — Raramente / Una vez al mes",
    3: "3 — Algunas veces / Un par de veces al mes",
    4: "4 — Bastante / Una vez a la semana",
    5: "5 — Con frecuencia / Un par de veces a la semana",
    6: "6 — Siempre / Todos los días",
}

# Los 16 ítems RED-TIC, organizados en cuatro dimensiones.
DIMENSIONES = {
    "Escepticismo": [
        "Con el paso del tiempo, las tecnologías me interesan cada vez menos.",
        "Cada vez me siento menos implicado en el uso de las TIC.",
        "Soy más cínico respecto de la contribución de las tecnologías en mi trabajo.",
        "Dudo del significado del trabajo con estas tecnologías.",
    ],
    "Fatiga": [
        "Me resulta difícil relajarme después de un día de trabajo utilizándolas.",
        "Cuando termino de trabajar con TIC, me siento agotado/a.",
        "Estoy tan cansado/a cuando acabo trabajar con ellas que no puedo hacer nada más.",
        "Es difícil concentrarme después de trabajar con tecnologías.",
    ],
    "Ansiedad": [
        "Me siento tenso y ansioso al trabajar con tecnologías.",
        "Me asusta pensar que puedo destruir una gran cantidad de información por el uso inadecuado de las mismas.",
        "Dudo a la hora de utilizar TIC por miedo a cometer errores.",
        "El trabajar con ellas me hace sentir incómodo, irritable e impaciente.",
    ],
    "Ineficacia": [
        "En mi opinión, soy ineficaz utilizando tecnologías.",
        "Es difícil trabajar con tecnologías de la información y de la comunicación.",
        "La gente dice que soy ineficaz utilizando tecnologías.",
        "Estoy inseguro de acabar bien mis tareas cuando utilizo las TIC.",
    ],
}


def si_no(pregunta, key):
    """Pregunta binaria sin respuesta preseleccionada para evitar respuestas accidentales."""
    return st.radio(pregunta, ["Sí", "No"], index=None, horizontal=True, key=key)


def arbol_escepticismo():
    st.markdown("#### A. Escepticismo")
    rechazo = si_no("¿Una experiencia negativa provocó rechazo a la tecnología?", "a_rechazo")
    if rechazo is None:
        return None
    if rechazo == "No":
        return ["Usar una alternativa."]

    falla = si_no("¿La causa fue una falla del sistema?", "a_falla")
    if falla is None:
        return None
    recomendacion_inicial = "Recibir soporte técnico." if falla == "No" else "Buscar orientación."

    apoyo = si_no("¿Recibe apoyo para resolverlo?", "a_apoyo")
    if apoyo is None:
        return None
    recomendacion_final = "Reducir uso innecesario." if apoyo == "No" else "Cambiar rutina de uso."
    return [recomendacion_inicial, recomendacion_final]


def arbol_fatiga():
    st.markdown("#### B. Fatiga")
    horas = si_no("¿Usas las TIC durante muchas horas?", "b_horas")
    if horas is None:
        return None
    if horas == "Sí":
        pausas = si_no("¿Realiza pausas durante la jornada?", "b_pausas")
        if pausas is None:
            return None
        return ["Organizar tareas."] if pausas == "Sí" else ["Establecer pausas."]

    multitarea = si_no("¿Trabaja con muchas tareas a la vez?", "b_multitarea")
    if multitarea is None:
        return None
    if multitarea == "No":
        return ["Reducir tiempo continuo.", "Alternar actividad."]
    return ["Reducir tiempo continuo.", "Cambiar rutina de uso."]


def arbol_ansiedad():
    st.markdown("#### C. Ansiedad")
    errores = si_no("¿Ha tenido errores al usar la tecnología?", "c_errores")
    if errores is None:
        return None
    if errores == "Sí":
        tension = si_no("¿Los errores generan tensión o miedo?", "c_tension")
        if tension is None:
            return None
        return ["Solicitar apoyo."] if tension == "Sí" else ["Recibir capacitación."]

    otra_causa = si_no("¿Existe otra causa de rechazo?", "c_otra_causa")
    if otra_causa is None:
        return None
    if otra_causa == "No":
        return ["Practicar antes de usar.", "Usar instrucciones."]
    return ["Practicar antes de usar.", "Cambiar rutina de uso."]


def arbol_ineficacia():
    st.markdown("#### D. Ineficacia")
    conocimientos = si_no("¿Considera insuficientes sus conocimientos?", "d_conocimientos")
    if conocimientos is None:
        return None
    if conocimientos == "Sí":
        capacitacion = si_no("¿Ha recibido capacitación adecuada?", "d_capacitacion")
        if capacitacion is None:
            return None
        return ["Recibir capacitación."] if capacitacion == "No" else ["Solicitar asistencia."]

    tutoriales = si_no("¿Usa tutoriales o guías?", "d_tutoriales")
    if tutoriales is None:
        return None
    if tutoriales == "No":
        return ["Consultar manual.", "Practicar con el sistema."]
    return ["Consultar manual.", "Cambiar rutina de uso."]


# Estado compartido entre pestañas de Streamlit.
if "respuestas_redtic" not in st.session_state:
    st.session_state.respuestas_redtic = None
if "promedios_redtic" not in st.session_state:
    st.session_state.promedios_redtic = None
if "recomendaciones_arbol" not in st.session_state:
    st.session_state.recomendaciones_arbol = {}
if "total_pt" not in st.session_state:
    st.session_state.total_pt = None

p_tab, a_tab, r_tab, c_tab = st.tabs([
    "1. Cuestionario RED-TIC", "2. Árbol de decisiones", "3. Resultados", "4. Apoyo y contacto"
])

with p_tab:
    st.header("Cuestionario RED-TIC")
    st.write("Contesta los 16 ítems. Selecciona la respuesta que mejor refleje tu experiencia con las tecnologías.")
    with st.form("form_redtic"):
        respuestas = {}
        n = 1
        for dimension, items in DIMENSIONES.items():
            st.subheader(dimension)
            for item in items:
                respuestas[n] = st.select_slider(
                    f"{n}. {item}", options=list(ESCALA.keys()), value=0,
                    format_func=lambda valor: ESCALA[valor], key=f"redtic_{n}"
                )
                n += 1
        enviar = st.form_submit_button("Calcular resultados del cuestionario", type="primary")

    if enviar:
        promedios = {}
        inicio = 1
        for dimension in DIMENSIONES:
            promedios[dimension] = sum(respuestas[i] for i in range(inicio, inicio + 4)) / 4
            inicio += 4
        st.session_state.respuestas_redtic = respuestas
        st.session_state.promedios_redtic = promedios
        # Fórmula PT indicada en la copia de manual consultada: suma de los 16 ítems / 4.
        st.session_state.total_pt = sum(respuestas.values()) / 4
        st.success("Se calcularon los resultados.")
        for dimension, promedio in promedios.items():
            st.write(f"**{dimension}:** {promedio:.2f} de 6")
        st.write(f"**Puntuación total PT (según la fórmula del manual consultado):** {st.session_state.total_pt:.2f}")
        st.caption("Se muestran puntuaciones, no diagnósticos. Confirma la fórmula y los puntos de corte con la versión exacta del manual que utilizará tu proyecto.")

with a_tab:
    st.header("Árbol de decisiones")
    st.write("Esta sección incluye las preguntas del diagrama. Las preguntas de seguimiento aparecen según las respuestas anteriores, para respetar las rutas del árbol.")
    dimension = st.selectbox("Selecciona la rama que deseas recorrer:", ["A. Escepticismo", "B. Fatiga", "C. Ansiedad", "D. Ineficacia"], key="rama_seleccionada")
    st.caption("Recorre una rama a la vez. Puedes regresar y elegir otra para guardar también su recomendación.")

    if dimension == "A. Escepticismo":
        recomendaciones = arbol_escepticismo()
        nombre = "Escepticismo"
    elif dimension == "B. Fatiga":
        recomendaciones = arbol_fatiga()
        nombre = "Fatiga"
    elif dimension == "C. Ansiedad":
        recomendaciones = arbol_ansiedad()
        nombre = "Ansiedad"
    else:
        recomendaciones = arbol_ineficacia()
        nombre = "Ineficacia"

    if st.button("Guardar recomendación de esta rama", type="primary"):
        if recomendaciones is None:
            st.error("Contesta todas las preguntas que se muestran en esta ruta antes de guardar la recomendación.")
        else:
            st.session_state.recomendaciones_arbol[nombre] = recomendaciones
            st.success("Recomendación guardada.")

    if st.session_state.recomendaciones_arbol:
        st.subheader("Recomendaciones guardadas")
        for dim, lista in st.session_state.recomendaciones_arbol.items():
            st.markdown(f"**{dim}:**")
            for recomendacion in lista:
                st.write(f"- {recomendacion}")

with r_tab:
    st.header("Resultados del cuestionario")
    if st.session_state.promedios_redtic is None:
        st.info("Completa primero el cuestionario en la pestaña 1.")
    else:
        promedios = st.session_state.promedios_redtic
        cols = st.columns(4)
        for col, (dim, valor) in zip(cols, promedios.items()):
            col.metric(dim, f"{valor:.2f} / 6")
        st.subheader("Gráfico de puntuaciones por dimensión")
        fig, ax = plt.subplots(figsize=(8, 4.5))
        etiquetas = list(promedios.keys())
        valores = list(promedios.values())
        barras = ax.bar(etiquetas, valores)
        ax.set_ylim(0, 6)
        ax.set_ylabel("Promedio de respuestas (0–6)")
        ax.set_title("Puntuación promedio por dimensión RED-TIC")
        ax.grid(axis="y", linestyle="--", alpha=0.35)
        ax.bar_label(barras, fmt="%.2f", padding=3)
        plt.xticks(rotation=15, ha="right")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        tabla = pd.DataFrame({"Dimensión": etiquetas, "Promedio (0–6)": [round(v, 2) for v in valores]})
        st.dataframe(tabla, use_container_width=True, hide_index=True)
        if st.session_state.recomendaciones_arbol:
            st.subheader("Recomendaciones del árbol")
            for dim, lista in st.session_state.recomendaciones_arbol.items():
                st.markdown(f"**{dim}:**")
                for recomendacion in lista:
                    st.write(f"- {recomendacion}")
        else:
            st.info("Aún no has guardado recomendaciones del árbol de decisiones.")
        st.caption("El gráfico resume las respuestas al cuestionario. No es un diagnóstico ni reemplaza el recorrido del árbol de decisiones.")

with c_tab:
    st.header("Apoyo y contacto")
    st.write("Si necesitas ayuda con las herramientas tecnológicas o te preocupa tu resultado, puedes contactar al área correspondiente de tu institución.")
    st.warning("Los siguientes contactos son marcadores de ejemplo. Sustitúyelos por contactos reales antes de entregar o publicar el proyecto.")
    for area, contacto in CONTACTOS_APOYO.items():
        st.markdown(f"**{area}:** {contacto}")
    if st.session_state.promedios_redtic is not None:
        elevadas = [dim for dim, valor in st.session_state.promedios_redtic.items() if valor >= 4]
        if elevadas:
            st.subheader("Orientación sugerida")
            st.write("En esta aplicación, estas dimensiones tienen un promedio de 4 o más: " + ", ".join(elevadas) + ".")
            st.write("Este umbral es provisional y orientativo, no un punto de corte clínico validado. Revisa también las recomendaciones del árbol.")
        else:
            st.write("Ninguna dimensión alcanza el umbral provisional de 4 en esta aplicación. Puedes solicitar apoyo si aun así lo necesitas.")

st.divider()
st.caption("Los ítems RED-TIC deben cotejarse con la versión exacta del manual utilizada en el proyecto. Las preguntas y rutas del árbol corresponden al diagrama proporcionado.")
