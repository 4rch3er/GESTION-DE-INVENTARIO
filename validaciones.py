def solicitar_texto(mensaje):
    """Solicita un texto al usuario y valida que no esté vacío."""
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            return entrada
        print("Este campo no puede estar vacío. Inténtalo de nuevo.")

def solicitar_entero(mensaje):
    """Solicita un número entero al usuario y valida que sea correcto."""
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            try:
                return int(entrada)
            except ValueError:
                print("Error: Por favor, ingresa un número entero válido.")
        else:
            print("Este campo no puede estar vacío. Inténtalo de nuevo.")

def solicitar_flotante(mensaje):
    """Solicita un número flotante al usuario y valida que sea correcto."""
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            try:
                return float(entrada)
            except ValueError:
                print("Error: Por favor, ingresa un número válido.")
        else:
            print("Este campo no puede estar vacío. Inténtalo de nuevo.")
