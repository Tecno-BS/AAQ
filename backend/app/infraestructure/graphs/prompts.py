"""Prompts para el pipeline cognitivo."""

VALIDATE_CONTEXT = """Eres un analista metodológico experto. Valida si el siguiente contexto de estudio cuantitativo tiene la información mínima necesaria para un análisis riguroso.

Contexto:
- Perfil: {profile}
- Antecedentes: {background}
- Pregunta de negocio: {business_question}
- Tipo de estudio: {study_type}
- Muestra: {sample}
- Umbral de significación: {significance_threshold}

Responde ÚNICAMENTE con una de estas dos palabras:
- VALID si el contexto es suficiente (tiene perfil, antecedentes, pregunta de negocio y tipo de estudio claros).
- INVALID si falta información crítica.

Tu respuesta (VALID o INVALID):"""


CLASSIFY_CHART = """Clasifica el siguiente tipo de gráfica. Responde con UNA palabra en minúsculas: bar, line, pie, scatter, histogram, area, other.

Contexto del estudio: {context_summary}
Nombre del archivo: {filename}

Tipo:"""


ANALYZE_CHART = """Eres un analista cuantitativo experto. Analiza la siguiente gráfica en el contexto del estudio de investigación.

Contexto del estudio:
- Perfil: {profile}
- Pregunta de negocio: {business_question}
- Tipo de estudio: {study_type}

La gráfica corresponde a: {chart_info}

Proporciona un análisis estructurado en JSON con estas claves (todas obligatorias):
- "explanation": string con la interpretación de la gráfica (2-4 oraciones)
- "hypotheses": lista de strings con hipótesis generadas a partir de los datos (al menos 1, máximo 5)
- "business_impact": string describiendo el impacto en negocio o decisiones (1-3 oraciones)

Responde SOLO con el JSON válido, sin markdown ni texto adicional."""


GENERATE_HYPOTHESES = """Consolida las siguientes hipótesis generadas por el análisis de múltiples gráficas en un conjunto coherente y sin duplicados.

Hipótesis por gráfica:
{hypotheses_per_chart}

Contexto: {business_question}

Genera una lista consolidada de hipótesis (5-10 como máximo), priorizadas por relevancia para la pregunta de negocio.
Responde con un JSON: {{ "hypotheses": ["hipótesis 1", "hipótesis 2", ...] }}"""


SYNTHESIZE_FINDINGS = """Agrupa estas hipótesis en hallazgos clave (key findings) concisos y accionables.

Hipótesis consolidadas:
{hypotheses}

Genera 3-7 hallazgos clave. Responde con un JSON: {{ "key_findings": ["hallazgo 1", "hallazgo 2", ...] }}"""


EXECUTIVE_SUMMARY = """Escribe un resumen ejecutivo (2-4 párrafos) basado en estos hallazgos.

Hallazgos clave:
{key_findings}

Contexto: {profile}, pregunta de negocio: {business_question}

El resumen debe ser claro, orientado a decisores y destacar las implicaciones principales."""


RECOMMENDATIONS = """Genera recomendaciones estratégicas y estrategias a partir de estos hallazgos.

Hallazgos clave:
{key_findings}

Resumen ejecutivo (extracto): {executive_summary}

Responde con un JSON:
{{
  "recommendations": ["recomendación 1", "recomendación 2", ...],
  "strategies": ["estrategia 1", "estrategia 2", ...]
}}

Entre 3-7 recomendaciones y 2-5 estrategias."""