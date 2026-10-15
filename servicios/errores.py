class ErrorNegocio(Exception):
    """Error esperado (validación, mapa, conectividad) con su código HTTP."""

    def __init__(self, mensaje, codigo=400):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo
