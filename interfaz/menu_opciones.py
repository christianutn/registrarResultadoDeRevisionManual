# Modern PySide6 implementation for menu interface
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class MenuDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.opcion = None
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Gestión de Eventos Sísmicos")
        self.setFixedSize(600, 350)  # Tamaño más compacto y fijo
        self.setStyleSheet("""
            QDialog {
                background: #FFFFFF;
            }
            QLabel {
                color: #2C3E50;
            }
            QPushButton {
                border: 2px solid transparent;
                border-radius: 6px;
                padding: 12px 24px;
                font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', sans-serif;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton#registrar {
                background-color: #3498DB;
                color: white;
            }
            QPushButton#registrar:hover {
                background-color: #2980B9;
            }
            QPushButton#salir {
                background-color: transparent;
                color: #E74C3C;
                border: 2px solid #E74C3C;
            }
            QPushButton#salir:hover {
                background-color: #E74C3C;
                color: white;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 35, 40, 35)
        
        # Spacer superior
        layout.addSpacerItem(QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Título
        title = QLabel("Gestión Sísmica")
        title_font = QFont("Segoe UI", 22, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2C3E50;")
        layout.addWidget(title)
        
        layout.addSpacerItem(QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Subtítulo
        subtitle = QLabel("Seleccione una opción")
        subtitle_font = QFont("Segoe UI", 10)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #7F8C8D;")
        layout.addWidget(subtitle)
        
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Botón Registrar
        btn_registrar = QPushButton("Registrar revisión manual")
        btn_registrar.setObjectName("registrar")
        btn_registrar.setCursor(Qt.PointingHandCursor)
        btn_registrar.clicked.connect(self.on_registrar)
        layout.addWidget(btn_registrar, alignment=Qt.AlignCenter)
        
        layout.addSpacerItem(QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Botón Salir
        btn_salir = QPushButton("Salir")
        btn_salir.setObjectName("salir")
        btn_salir.setCursor(Qt.PointingHandCursor)
        btn_salir.clicked.connect(self.on_salir)
        layout.addWidget(btn_salir, alignment=Qt.AlignCenter)
        
        # Spacer inferior
        layout.addSpacerItem(QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        self.setLayout(layout)
    
    def on_registrar(self):
        self.opcion = "Registrar resultado de revisión manual"
        self.accept()
    
    def on_salir(self):
        self.opcion = "Salir"
        self.reject()

def mostrar_menu_opciones():
    dialog = MenuDialog()
    result = dialog.exec()
    return dialog.opcion
