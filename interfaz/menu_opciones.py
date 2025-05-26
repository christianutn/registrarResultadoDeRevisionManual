import PySimpleGUI as sg

def mostrar_menu_opciones():
    layout = [
        [sg.Text("Seleccione una opción:")],
        [sg.Button("Registrar resultado de revisión manual"), sg.Button("Salir")]
    ]
    window = sg.Window("Menú Principal", layout)
    opcion = None
    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED or event == "Salir":
            opcion = "Salir"
            break
        if event == "Registrar resultado de revisión manual":
            opcion = "Registrar resultado de revisión manual"
            break
    window.close()
    return opcion
