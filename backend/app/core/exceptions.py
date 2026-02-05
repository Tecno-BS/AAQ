class AAQException(Exception):
    """Excepción base del proyecto AAQ."""
    pass


class StudyNotFoundError(AAQException):
    """El estudio no existe."""
    pass


class InvalidStudyStateError(AAQException):
    """El estudio está en un estado inválido para la operación."""
    pass


class NoChartsUploadedError(AAQException):
    """No hay gráficas subidas en el estudio."""
    pass


class ReportNotFoundError(AAQException):
    """El reporte no existe."""
    pass