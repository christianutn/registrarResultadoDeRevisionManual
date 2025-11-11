"""
Módulo de diálogos UI para la aplicación de gestión de eventos sísmicos.
Contiene todos los componentes de interfaz gráfica basados en PySide6.
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QListWidget, QTextEdit, QMessageBox,
                               QSpacerItem, QSizePolicy, QWidget, QTableWidget,
                               QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class EventSelectorDialog(QDialog):
    """Diálogo para seleccionar un evento sísmico de la lista"""
    
    def __init__(self, datos_eventos_ordenados, eventos_objetos):
        super().__init__()
        self.datos_eventos = datos_eventos_ordenados
        self.eventos_objetos = eventos_objetos
        self.evento_seleccionado = None
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Selector de Eventos Sísmicos")
        self.setFixedSize(850, 550)  # Ajustado para 4 columnas
        self.setStyleSheet("""
            QDialog {
                background: #F8F9FA;
            }
            QLabel {
                color: #2C3E50;
                font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', sans-serif;
            }
            QLabel#subtitle {
                color: #3498DB;
                font-weight: 600;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                gridline-color: #F0F0F0;
                font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', sans-serif;
                font-size: 9pt;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F5F5F5;
            }
            QTableWidget::item:selected {
                background-color: #3498DB;
                color: white;
            }
            QHeaderView::section {
                background-color: #ECF0F1;
                color: #2C3E50;
                padding: 8px;
                border: none;
                border-right: 1px solid #BDC3C7;
                border-bottom: 2px solid #3498DB;
                font-weight: 600;
                font-size: 9pt;
            }
            QPushButton {
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', sans-serif;
                font-weight: 600;
                font-size: 11px;
            }
            QPushButton#seleccionar {
                background-color: #27AE60;
                color: white;
            }
            QPushButton#seleccionar:hover {
                background-color: #229954;
            }
            QPushButton#cancelar {
                background-color: transparent;
                color: #E74C3C;
                border: 2px solid #E74C3C;
            }
            QPushButton#cancelar:hover {
                background-color: #E74C3C;
                color: white;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Título
        title = QLabel("Seleccionar Evento Sísmico")
        title_font = QFont("Segoe UI", 18, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacerItem(QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Subtítulo con contador
        subtitle = QLabel(f"{len(self.datos_eventos)} eventos pendientes")
        subtitle.setObjectName("subtitle")
        subtitle_font = QFont("Segoe UI", 10)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacerItem(QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Tabla de eventos
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels([
            "Fecha y Hora", 
            "Epicentro", 
            "Hipocentro", 
            "Magnitud"
        ])
        self.table_widget.setRowCount(len(self.datos_eventos))
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setSelectionMode(QTableWidget.SingleSelection)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.verticalHeader().setVisible(False)
        
        # Configurar el ajuste de columnas
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Fecha
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Epicentro
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Hipocentro
        header.setSectionResizeMode(3, QHeaderView.Stretch)           # Magnitud
        
        # Llenar la tabla con datos
        for row, datos in enumerate(self.datos_eventos):
            # Fecha y Hora
            fecha_item = QTableWidgetItem(str(datos.get('fecha_hora_ocurrencia', 'N/D')))
            fecha_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row, 0, fecha_item)
            
            # Epicentro
            epic = f"({datos.get('latitud_epicentro')}, {datos.get('longitud_epicentro')})"
            epic_item = QTableWidgetItem(epic)
            epic_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row, 1, epic_item)
            
            # Hipocentro
            hip = f"({datos.get('latitud_hipocentro')}, {datos.get('longitud_hipocentro')})"
            hip_item = QTableWidgetItem(hip)
            hip_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row, 2, hip_item)
            
            # Magnitud
            mag_item = QTableWidgetItem(str(datos.get('valor_magnitud', 'N/D')))
            mag_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row, 3, mag_item)
        
        layout.addWidget(self.table_widget)
        
        layout.addSpacerItem(QSpacerItem(20, 12, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Botones
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        btn_seleccionar = QPushButton("Seleccionar")
        btn_seleccionar.setObjectName("seleccionar")
        btn_seleccionar.setCursor(Qt.PointingHandCursor)
        btn_seleccionar.setMinimumWidth(120)
        btn_seleccionar.clicked.connect(self.on_seleccionar)
        button_layout.addWidget(btn_seleccionar)
        
        button_layout.addSpacing(15)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("cancelar")
        btn_cancelar.setCursor(Qt.PointingHandCursor)
        btn_cancelar.setMinimumWidth(120)
        btn_cancelar.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancelar)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def on_seleccionar(self):
        current_row = self.table_widget.currentRow()
        if current_row >= 0:
            self.evento_seleccionado = self.eventos_objetos[current_row]
            self.accept()
        else:
            QMessageBox.warning(self, "⚠️ Advertencia", 
                              "Por favor seleccione un evento de la tabla.")


class EventDetailsDialog(QDialog):
    """Diálogo para mostrar detalles del evento y acciones"""
    
    def __init__(self, texto_evento, texto_series, pantalla_adm):
        super().__init__()
        self.texto_evento = texto_evento
        self.texto_series = texto_series
        self.pantalla_adm = pantalla_adm
        self.accion_seleccionada = None
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Detalles del Evento Sísmico")
        self.setFixedSize(950, 600)  # Más compacto
        self.setStyleSheet("""
            QDialog {
                background: #F8F9FA;
            }
            QLabel {
                color: #2C3E50;
                font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', sans-serif;
            }
            QLabel#section {
                color: #7F8C8D;
                font-weight: 600;
                font-size: 10px;
                letter-spacing: 0.5px;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 12px;
                font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', sans-serif;
                font-size: 9pt;
                color: #2C3E50;
                line-height: 1.5;
            }
            QPushButton {
                border: none;
                border-radius: 6px;
                padding: 10px 18px;
                font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', sans-serif;
                font-weight: 600;
                font-size: 11px;
            }
            QPushButton#mapa {
                background-color: #3498DB;
                color: white;
            }
            QPushButton#mapa:hover {
                background-color: #2980B9;
            }
            QPushButton#modificar {
                background-color: #F39C12;
                color: white;
            }
            QPushButton#modificar:hover {
                background-color: #E67E22;
            }
            QPushButton#confirmar {
                background-color: #27AE60;
                color: white;
            }
            QPushButton#confirmar:hover {
                background-color: #229954;
            }
            QPushButton#rechazar {
                background-color: #E74C3C;
                color: white;
            }
            QPushButton#rechazar:hover {
                background-color: #C0392B;
            }
            QPushButton#experto {
                background-color: #9B59B6;
                color: white;
            }
            QPushButton#experto:hover {
                background-color: #8E44AD;
            }
            QPushButton#cancelar {
                background-color: transparent;
                color: #95A5A6;
                border: 2px solid #BDC3C7;
            }
            QPushButton#cancelar:hover {
                background-color: #BDC3C7;
                color: white;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Título
        title = QLabel("Detalles del Evento Sísmico")
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacerItem(QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # TextEdit con los datos del evento
        self.text_edit_evento = QTextEdit()
        self.text_edit_evento.setPlainText(self.texto_evento)
        self.text_edit_evento.setReadOnly(True)
        self.text_edit_evento.setMaximumHeight(120)
        layout.addWidget(self.text_edit_evento)
        
        layout.addSpacerItem(QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # TextEdit con las series temporales formateadas
        self.text_edit_series = QTextEdit()
        self.text_edit_series.setHtml(self._format_series_data(self.texto_series))
        self.text_edit_series.setReadOnly(True)
        self.text_edit_series.setMaximumHeight(200)
        layout.addWidget(self.text_edit_series)
        
        layout.addSpacerItem(QSpacerItem(20, 12, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Sección de Opciones de Consulta
        consulta_label = QLabel("OPCIONES")
        consulta_label.setObjectName("section")
        layout.addWidget(consulta_label)
        
        layout.addSpacerItem(QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        consulta_layout = QHBoxLayout()
        consulta_layout.setSpacing(10)
        consulta_layout.addStretch()
        
        btn_mapa = QPushButton("🗺️  Ver mapa")
        btn_mapa.setObjectName("mapa")
        btn_mapa.setCursor(Qt.PointingHandCursor)
        btn_mapa.setMinimumWidth(130)
        btn_mapa.clicked.connect(self.on_ver_mapa)
        consulta_layout.addWidget(btn_mapa)
        
        btn_modificar = QPushButton("✏️  Modificar")
        btn_modificar.setObjectName("modificar")
        btn_modificar.setCursor(Qt.PointingHandCursor)
        btn_modificar.setMinimumWidth(130)
        btn_modificar.clicked.connect(self.on_modificar)
        consulta_layout.addWidget(btn_modificar)
        
        consulta_layout.addStretch()
        layout.addLayout(consulta_layout)
        
        layout.addSpacerItem(QSpacerItem(20, 12, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Sección de Acciones Finales
        acciones_label = QLabel("ACCIONES")
        acciones_label.setObjectName("section")
        layout.addWidget(acciones_label)
        
        layout.addSpacerItem(QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        acciones_layout = QHBoxLayout()
        acciones_layout.setSpacing(10)
        acciones_layout.addStretch()
        
        btn_confirmar = QPushButton("✓  Confirmar")
        btn_confirmar.setObjectName("confirmar")
        btn_confirmar.setCursor(Qt.PointingHandCursor)
        btn_confirmar.setMinimumWidth(120)
        btn_confirmar.clicked.connect(self.on_confirmar)
        acciones_layout.addWidget(btn_confirmar)
        
        btn_rechazar = QPushButton("✗  Rechazar")
        btn_rechazar.setObjectName("rechazar")
        btn_rechazar.setCursor(Qt.PointingHandCursor)
        btn_rechazar.setMinimumWidth(120)
        btn_rechazar.clicked.connect(self.on_rechazar)
        acciones_layout.addWidget(btn_rechazar)
        
        btn_experto = QPushButton("👤  Solicitar experto")
        btn_experto.setObjectName("experto")
        btn_experto.setCursor(Qt.PointingHandCursor)
        btn_experto.setMinimumWidth(160)
        btn_experto.clicked.connect(self.on_experto)
        acciones_layout.addWidget(btn_experto)
        
        btn_cancelar = QPushButton("←  Cancelar")
        btn_cancelar.setObjectName("cancelar")
        btn_cancelar.setCursor(Qt.PointingHandCursor)
        btn_cancelar.setMinimumWidth(110)
        btn_cancelar.clicked.connect(self.reject)
        acciones_layout.addWidget(btn_cancelar)
        
        acciones_layout.addStretch()
        layout.addLayout(acciones_layout)
        
        self.setLayout(layout)
    
    def _format_series_data(self, texto_series):
        """Formatea los datos de series temporales en HTML para mejor presentación"""
        html = "<div style='font-family: Segoe UI, sans-serif; font-size: 9pt; line-height: 1.6;'>"
        
        lines = texto_series.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detectar y formatear líneas de estación
            if line.startswith('Estación:'):
                html += f"<p style='margin: 12px 0 6px 0; font-weight: 700; font-size: 10pt; color: #2C3E50;'>📍 {line}</p>"
            # Detectar y formatear líneas de código
            elif 'Código:' in line and 'Nombre:' in line:
                html += f"<p style='margin: 4px 0 4px 15px; color: #3498DB; font-weight: 600;'>{line}</p>"
            # Detectar cantidad de muestras
            elif 'Cantidad de muestras:' in line:
                html += f"<p style='margin: 2px 0 2px 25px; color: #7F8C8D; font-size: 8.5pt;'>{line}</p>"
            # Ejemplos de muestras
            elif 'Ejemplo muestra' in line:
                html += f"<p style='margin: 2px 0 2px 35px; color: #95A5A6; font-size: 8pt; font-family: Consolas, monospace;'>{line}</p>"
            else:
                html += f"<p style='margin: 2px 0 2px 20px; color: #34495E;'>{line}</p>"
        
        html += "</div>"
        return html
    
    def on_ver_mapa(self):
        self.pantalla_adm.habilitar_opc_mapa()
    
    def on_modificar(self):
        self.pantalla_adm.habilitar_opc_modificar_evento()
    
    def on_confirmar(self):
        self.accion_seleccionada = "Confirmar evento"
        self.accept()
        self.pantalla_adm.tomar_selecc_opc_accion(self.accion_seleccionada)
    
    def on_rechazar(self):
        self.accion_seleccionada = "Rechazar evento"
        self.accept()
        self.pantalla_adm.tomar_selecc_opc_accion(self.accion_seleccionada)
    
    def on_experto(self):
        self.accion_seleccionada = "Solicitar revisión a experto"
        self.accept()
        self.pantalla_adm.tomar_selecc_opc_accion(self.accion_seleccionada)


def mostrar_mensaje_informativo(titulo, mensaje):
    """Función auxiliar para mostrar mensajes informativos"""
    from PySide6.QtWidgets import QMessageBox
    QMessageBox.information(None, titulo, mensaje)


def mostrar_mensaje_error(titulo, mensaje):
    """Función auxiliar para mostrar mensajes de error"""
    from PySide6.QtWidgets import QMessageBox
    QMessageBox.critical(None, titulo, mensaje)
