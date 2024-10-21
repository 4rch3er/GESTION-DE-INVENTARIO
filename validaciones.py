def solicitar_texto(mensaje):
    """Solicita un texto al usuario y valida que no esté vacío."""
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            return entrada
        print("Este campo no puede estar vacío. Inténtalo de nuevo.")


def solicitar_entero(mensaje):
    """Solicita un número entero positivo al usuario y valida que sea correcto."""
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            try:
                valor = int(entrada)
                if valor >= 0:
                    return valor
                else:
                    print("Error: Por favor, ingresa un número entero positivo.")
            except ValueError:
                print("Error: Por favor, ingresa un número entero válido.")
        else:
            print("Este campo no puede estar vacío. Inténtalo de nuevo.")

def solicitar_flotante(mensaje):
    """Solicita un número flotante positivo al usuario y valida que sea correcto."""
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            try:
                valor = float(entrada)
                if valor >= 0:
                    return valor
                else:
                    print("Error: Por favor, ingresa un número positivo.")
            except ValueError:
                print("Error: Por favor, ingresa un número válido.")
       


