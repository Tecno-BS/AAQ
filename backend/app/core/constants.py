"""
Constantes de AAQ
Inicialmente, se encuentran los tipos de estudio cuantitativos, del archivo ABSTRACT SOLCUCIONES BS PAG.docx

"""

STUDY_TYPES : tuple[str, ...] = (
    "Estudio de adopción",
    "Árboles de Decisión",
    "Elasticidad de marca",
    "ESTRUQTURAL (Estudios basados en segmentación psicovolumétrica)",
    "Quid BS – Estudio ómnibus",
    "Shopper",
    "Audio tipos o Test marca auditiva",
    "Contacto (Touch Point)",
    "Ev. Etiquetas y Empaques",
    "Evaluación Página web",
    "IBE ADTEST (PRE TEST PUBLICITARIO)",
    "Logo Test",
    "Postest publicitario",
    "DIP – TRACKING DE DESEMPEÑO E IMPACTO PUBLICITARIO",
    "Brand Name Test",
    "BET – Salud de marca",
    "Diagnóstico y estrategia de marca",
    "Evaluación postulados de posicionamiento",
    "CX Apps",
    "Fuga predictiva",
    "Fuga reactiva",
    "PDA III: Estudio de satisfacción y fidelización",
    "Expedia",
    "NECEXP: Exploración de necesidades y expectativas",
    "EPAC (Evaluación de potencial y aceptación de concepto)",
    "Pruebas organolépticas",
    "Análisis Semiótico",
    "Exploratorio de categorías",
    "ZMET",
    "Brand Fusion",
)

def is_valid_study_type(value: str) -> bool:
    """Valida que el tipo de estudio esté en la lista oficial."""
    return value in STUDY_TYPES