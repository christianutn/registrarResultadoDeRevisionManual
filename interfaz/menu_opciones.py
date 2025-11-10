import PySimpleGUI as sg


def mostrar_menu_opciones():
    """Muestra un menú principal con estilo más moderno.

    Retorna el nombre de la opción seleccionada o "Salir".
    """
    # Tema y opciones visuales
    # Aplicar tema de forma compatible con distintas versiones de PySimpleGUI
    if hasattr(sg, 'theme'):
        sg.theme('DarkBlue3')
    elif hasattr(sg, 'ChangeLookAndFeel'):
        try:
            sg.ChangeLookAndFeel('DarkBlue3')
        except Exception:
            pass
    else:
        # no-op si la versión de PySimpleGUI no expone métodos de tema
        pass

    header_font = ("Segoe UI", 16, "bold")
    normal_font = ("Segoe UI", 11)

    layout = [
        [sg.Text("Sistema de Revisión Manual", font=header_font, justification='center', expand_x=True)],
        [sg.Text("Seleccione una opción:", font=normal_font, pad=(0, (10, 0)))],
        [
            sg.Button("📝  Registrar resultado de revisión manual", key="-REGISTRAR-", font=normal_font, size=(30, 1), button_color=("white", "#2a9d8f")),
            sg.Button("❌  Salir", key="-SALIR-", font=normal_font, size=(10, 1), button_color=("white", "#e76f51"))
        ]
    ]

    window = sg.Window("Menú Principal", layout, element_justification='center', margins=(20, 15), modal=True)
    opcion = None
    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED or event == "-SALIR-":
            opcion = "Salir"
            break
        if event == "-REGISTRAR-":
            opcion = "Registrar resultado de revisión manual"
            break
    window.close()
    return opcion
