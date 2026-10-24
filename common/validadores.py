"""Funciones de validación reutilizables para los problemas del proyecto."""


def validarRangoNumerico(valor, minimo, maximo):
    """Valida que `valor` sea numérico y esté dentro del rango [minimo, maximo].

    Args:
        valor: Valor a validar.
        minimo: Límite inferior permitido (inclusive).
        maximo: Límite superior permitido (inclusive).

    Returns:
        bool: True si el valor cumple con el rango.

    Raises:
        TypeError: Si `valor` no es numérico.
        ValueError: Si el valor está fuera del rango permitido.
    """
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TypeError(
            f"El valor '{valor}' debe ser numérico para validar su rango."
        )
    if valor < minimo or valor > maximo:
        raise ValueError(
            f"El valor {valor} está fuera del rango permitido "
            f"[{minimo}, {maximo}]."
        )
    return True


def validarNoVacio(valor, campo):
    """Valida que `valor` no sea None ni una cadena vacía o de solo espacios.

    Args:
        valor: Valor a validar.
        campo: Nombre del campo, usado en el mensaje de error.

    Returns:
        bool: True si el valor no está vacío.

    Raises:
        ValueError: Si el valor es None o queda vacío tras quitar espacios.
    """
    if valor is None:
        raise ValueError(f"El campo '{campo}' no puede ser nulo.")
    if isinstance(valor, str) and valor.strip() == "":
        raise ValueError(f"El campo '{campo}' no puede estar vacío.")
    return True
