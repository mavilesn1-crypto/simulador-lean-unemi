"""
SIMULADOR DE MADUREZ LEAN 4.0
Para Streamlit Cloud - Sin código visible para estudiantes

Universidad Estatal de Milagro
Docente: Ing. Andrés Avilés Noles, Ph.D.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Configuración de página
st.set_page_config(
    page_title="Simulador Lean 4.0",
    page_icon="🏭",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1E2761 0%, #028090 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# DATOS
PRINCIPLES = ['Valor', 'Flujo de Valor', 'Flujo Continuo', 'Pull', 'Perfección']

SECTORS = {
    'Banano': [3.8, 3.5, 3.2, 3.0, 3.4],
    'Camarón': [4.0, 3.2, 3.0, 2.8, 3.5],
    'Alimentos procesados': [4.2, 3.8, 3.5, 3.4, 3.9],
    'Plásticos': [3.5, 3.0, 2.8, 2.5, 3.0],
    'Automotriz': [4.5, 4.2, 4.0, 4.3, 4.4],
    'Textil': [3.2, 2.8, 2.5, 2.2, 2.8]
}

LEAN_TOOLS = [
    {'name': '5S', 'classic': 'Orden y limpieza física', 'digital': '5S Digitales con RFID', 'benefit': 'Medio', 'investment': 'Baja'},
    {'name': 'Kanban', 'classic': 'Tarjetas físicas', 'digital': 'e-Kanban con IoT', 'benefit': 'Alto', 'investment': 'Media'},
    {'name': 'VSM', 'classic': 'Dibujo manual', 'digital': 'VSM digital con gemelos', 'benefit': 'Alto', 'investment': 'Alta'},
    {'name': 'Poka-Yoke', 'classic': 'Dispositivos mecánicos', 'digital': 'Poka-Yoke con IA', 'benefit': 'Alto', 'investment': 'Media'},
    {'name': 'SMED', 'classic': 'Cronometraje manual', 'digital': 'SMED con realidad aumentada', 'benefit': 'Alto', 'investment': 'Alta'},
    {'name': 'TPM', 'classic': 'Mantenimiento preventivo', 'digital': 'TPM predictivo con IA', 'benefit': 'Alto', 'investment': 'Alta'}
]

# FUNCIONES
def calculate_maturity_level(avg_score):
    if avg_score >= 3.5:
        return "Nivel 4-5", "🟢 CLASE MUNDIAL", "#27AE60"
    elif avg_score >= 2.5:
        return "Nivel 3", "🟡 EN DESARROLLO", "#F39C12"
    else:
        return "Nivel 1-2", "🔴 INICIAL", "#E74C3C"

def calculate_gaps(scores, benchmark):
    gaps = []
    for i, principle in enumerate(PRINCIPLES):
        gap = benchmark[i] - scores[i]
        status = 'green' if gap <= 0 else 'yellow' if gap <= 0.5 else 'red'
        gaps.append({
            'principle': principle,
            'score': scores[i],
            'benchmark': benchmark[i],
            'gap': gap,
            'status': status
        })
    gaps.sort(key=lambda x: x['gap'], reverse=True)
    return gaps

# HEADER
st.markdown("""
<div class="main-header">
    <h1>🏭 Simulador de Madurez Lean 4.0</h1>
    <h3>Manufactura Esbelta con Inteligencia Artificial</h3>
    <p>Universidad Estatal de Milagro - Ing. Andrés Avilés Noles, Ph.D.</p>
</div>
""", unsafe_allow_html=True)

# INSTRUCCIONES
with st.expander("📋 Instrucciones de uso", expanded=False):
    st.markdown("""
    1. Selecciona el **sector industrial** en el panel lateral
    2. Ajusta los **5 deslizadores** según el nivel de madurez (1 = Inicial, 5 = Excelente)
    3. Observa los **resultados automáticos** en tiempo real
    4. Toma **capturas de pantalla** para tu informe
    5. Responde las **preguntas reflexivas** al final
    """)

# SIDEBAR - CONTROLES
st.sidebar.header("🎛️ Controles de Evaluación")

sector_name = st.sidebar.selectbox(
    "Sector Industrial",
    options=list(SECTORS.keys()),
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("5 Principios Lean")

scores = []
for i, principle in enumerate(PRINCIPLES):
    score = st.sidebar.slider(
        f"{i+1}. {principle}",
        min_value=1.0,
        max_value=5.0,
        value=3.0,
        step=0.1,
        help=f"Califica el nivel de madurez en {principle}"
    )
    scores.append(score)

# CÁLCULOS
benchmark = SECTORS[sector_name]
avg_score = np.mean(scores)
level, classification, color = calculate_maturity_level(avg_score)
gaps_data = calculate_gaps(scores, benchmark)

# RESULTADOS PRINCIPALES
st.header("📊 Resultados de la Evaluación")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Score Global", f"{avg_score:.2f} / 5.0")

with col2:
    st.metric("Clasificación", classification)

with col3:
    st.metric("Nivel de Madurez", level)

# GRÁFICO RADAR
st.subheader("📈 Perfil de Madurez Lean")

fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=scores,
    theta=PRINCIPLES,
    fill='toself',
    name='Tu Evaluación',
    line=dict(color='#028090', width=3),
    fillcolor='rgba(2, 128, 144, 0.3)'
))

fig_radar.add_trace(go.Scatterpolar(
    r=benchmark,
    theta=PRINCIPLES,
    fill='toself',
    name=f'Benchmark {sector_name}',
    line=dict(color='#F39C12', width=2, dash='dash'),
    fillcolor='rgba(243, 156, 18, 0.1)'
))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
    showlegend=True,
    height=500
)

st.plotly_chart(fig_radar, use_container_width=True)

# TABLA DE BRECHAS
st.subheader("📋 Análisis de Brechas - Priorización de Mejoras")

df_gaps = pd.DataFrame(gaps_data)
df_gaps['status_emoji'] = df_gaps['status'].map({
    'green': '🟢 EXCELENTE',
    'yellow': '🟡 MEJORABLE',
    'red': '🔴 PRIORITARIO'
})

st.dataframe(
    df_gaps[['principle', 'score', 'benchmark', 'gap', 'status_emoji']].rename(columns={
        'principle': 'Principio',
        'score': 'Tu Score',
        'benchmark': 'Benchmark',
        'gap': 'Brecha',
        'status_emoji': 'Estado'
    }),
    use_container_width=True,
    hide_index=True
)

# RECOMENDACIONES
st.subheader("💡 Recomendaciones Prioritarias")

recomendaciones = {
    'Valor': "Realizar sesiones de Voice of Customer (VOC) y mapear la cadena de valor desde perspectiva del cliente",
    'Flujo de Valor': "Implementar VSM (Value Stream Mapping) para identificar desperdicios en cada etapa del proceso",
    'Flujo Continuo': "Reducir tamaños de lote, implementar células de manufactura y balancear líneas de producción",
    'Pull': "Implementar sistema Kanban para producir según demanda real y reducir inventarios",
    'Perfección': "Establecer programa Kaizen con ciclos PDCA y capacitar en herramientas de mejora continua"
}

for i, gap in enumerate(gaps_data[:3], 1):
    with st.container():
        st.markdown(f"**{i}. {gap['principle']}** (Brecha: {gap['gap']:.2f})")
        st.info(recomendaciones.get(gap['principle'], 'Revisar procesos y procedimientos'))

# COMPARADOR DE HERRAMIENTAS
st.header("🔄 Comparador: Lean Clásico vs Lean 4.0")

df_tools = pd.DataFrame(LEAN_TOOLS)

st.dataframe(
    df_tools[['name', 'classic', 'digital', 'benefit', 'investment']].rename(columns={
        'name': 'Herramienta',
        'classic': 'Versión Clásica',
        'digital': 'Versión Digital (4.0)',
        'benefit': 'Beneficio',
        'investment': 'Inversión'
    }),
    use_container_width=True,
    hide_index=True
)

# PREGUNTAS REFLEXIVAS
st.header("🤔 Preguntas Reflexivas - Entregable")

with st.expander("Ver preguntas completas", expanded=False):
    st.markdown("""
    ### PARTE 1: Análisis de Sensibilidad
    1. **Experimentación:** Varía cada principio independientemente. ¿Cuál tiene mayor impacto?
    2. **Comparación sectorial:** Evalúa en 3 sectores diferentes. ¿Cómo cambia tu posición?
    
    ### PARTE 2: Priorización Estratégica
    3. **Caso real:** Con tus resultados, ¿en qué principio invertirías primero? Justifica.
    
    ### PARTE 3: Transformación Digital
    4. **Potencial en Ecuador:** ¿Qué herramienta 4.0 tiene mayor potencial? Argumenta.
    5. **Ética profesional:** ¿Qué riesgos éticos tiene automatizar decisiones con IA?
    
    ### PARTE 4: Conexión con los 8 Desperdicios
    6. **Análisis sistémico:** Relaciona tu brecha más grande con los tipos de Muda.
    
    ---
    
    **📤 Entregable:** Documento PDF de 3-5 páginas con:
    - Capturas de pantalla (mínimo 3 escenarios)
    - Respuestas argumentadas a las 6 preguntas
    - Conclusiones (200-300 palabras)
    
    **Criterios:** Profundidad 40% | Terminología 25% | Argumentación 20% | Presentación 15%
    """)

# FOOTER
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>Universidad Estatal de Milagro</strong> - Ingeniería Industrial<br>
    Manufactura Esbelta con Inteligencia Artificial<br>
    <em>"IA propone → Estudiante decide"</em></p>
</div>
""", unsafe_allow_html=True)
