import sys
import os
import csv

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel, QAbstractItemView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer


class MainWindow(QMainWindow):
    def __init__(self, csv_path=None):
        super().__init__()
        self.setWindowTitle('Administrador de Eventos Sísmicos')
        self.resize(1000, 650)

        # Aplicar tema minimalista
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                gridline-color: #f0f0f0;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 12px 8px;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QHeaderView::section {
                background-color: #fafafa;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: 600;
                font-size: 12px;
                color: #616161;
            }
            QPushButton {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 500;
                color: #424242;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border-color: #bdbdbd;
            }
            QPushButton:pressed {
                background-color: #eeeeee;
            }
            QPushButton#confirmBtn {
                background-color: #4caf50;
                color: white;
                border: none;
            }
            QPushButton#confirmBtn:hover {
                background-color: #45a049;
            }
            QPushButton#rejectBtn {
                background-color: #f44336;
                color: white;
                border: none;
            }
            QPushButton#rejectBtn:hover {
                background-color: #da190b;
            }
            QPushButton#expertBtn {
                background-color: #ff9800;
                color: white;
                border: none;
            }
            QPushButton#expertBtn:hover {
                background-color: #fb8c00;
            }
            QLabel#headerLabel {
                font-size: 24px;
                font-weight: 300;
                color: #212121;
                padding: 16px 8px;
            }
        """)

        self.csv_path = csv_path or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'eventos_sismicos.csv')

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        central.setLayout(layout)

        # Header con icono
        header_layout = QHBoxLayout()
        header = QLabel('📊 Eventos Sísmicos Pendientes')
        header.setObjectName('headerLabel')
        header_layout.addWidget(header)
        header_layout.addStretch()
        
        # Badge con contador
        self.count_label = QLabel('0 eventos')
        self.count_label.setStyleSheet("""
            background-color: #2196f3;
            color: white;
            border-radius: 12px;
            padding: 6px 16px;
            font-size: 12px;
            font-weight: 600;
        """)
        header_layout.addWidget(self.count_label)
        layout.addLayout(header_layout)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['📅 Fecha/Hora', '📍 Epicentro', '🌐 Hipocentro', '📏 Magnitud'])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        
        # Configurar anchos de columnas
        self.table.setColumnWidth(0, 200)  # Fecha/Hora - más ancho para mostrar completo
        self.table.setColumnWidth(1, 180)  # Epicentro
        self.table.setColumnWidth(2, 180)  # Hipocentro
        self.table.setColumnWidth(3, 100)  # Magnitud
        
        # Aumentar altura de filas para mejor espaciado
        self.table.verticalHeader().setDefaultSectionSize(45)
        self.table.verticalHeader().setVisible(False)  # Ocultar números de fila
        
        # La última columna se estira para ocupar el espacio restante
        self.table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.table, stretch=1)

        # Botones con iconos
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        self.btn_block = QPushButton('🔒 Bloquear')
        self.btn_details = QPushButton('🔍 Detalles')
        
        self.btn_confirm = QPushButton('✅ Confirmar')
        self.btn_confirm.setObjectName('confirmBtn')
        
        self.btn_reject = QPushButton('❌ Rechazar')
        self.btn_reject.setObjectName('rejectBtn')
        
        self.btn_expert = QPushButton('👨‍🔬 Solicitar Experto')
        self.btn_expert.setObjectName('expertBtn')

        btn_layout.addWidget(self.btn_block)
        btn_layout.addWidget(self.btn_details)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.btn_confirm)
        btn_layout.addWidget(self.btn_reject)
        btn_layout.addWidget(self.btn_expert)
        layout.addLayout(btn_layout)

        # Conectar señales
        self.btn_block.clicked.connect(self.block_event)
        self.btn_details.clicked.connect(self.view_details)
        self.btn_confirm.clicked.connect(self.confirm_event)
        self.btn_reject.clicked.connect(self.reject_event)
        self.btn_expert.clicked.connect(self.request_expert)

        # Cargar datos
        self.load_csv()

    def load_csv(self):
        if not os.path.exists(self.csv_path):
            QMessageBox.warning(self, 'CSV no encontrado', f'No se encontró el archivo: {self.csv_path}')
            return
        rows = []
        with open(self.csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(r)

        self.table.setRowCount(len(rows))
        
        # Actualizar contador
        self.count_label.setText(f'{len(rows)} eventos')
        
        for i, r in enumerate(rows):
            fecha = r.get('fecha_hora_ocurrencia', '')
            epic = f"{r.get('latitud_epicentro','')} , {r.get('longitud_epicentro','')}"
            hipo = f"{r.get('latitud_hipocentro','')} , {r.get('longitud_hipocentro','')}"
            mag = r.get('valor_magnitud','')
            
            # Agregar items con alineación centrada
            item_fecha = QTableWidgetItem(fecha)
            item_fecha.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            
            item_epic = QTableWidgetItem(epic)
            item_epic.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            
            item_hipo = QTableWidgetItem(hipo)
            item_hipo.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            
            item_mag = QTableWidgetItem(mag)
            item_mag.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            
            self.table.setItem(i, 0, item_fecha)
            self.table.setItem(i, 1, item_epic)
            self.table.setItem(i, 2, item_hipo)
            self.table.setItem(i, 3, item_mag)

    def selected_row(self):
        sel = self.table.selectedItems()
        if not sel:
            return None
        row = sel[0].row()
        data = {
            'fecha': self.table.item(row, 0).text(),
            'epic': self.table.item(row, 1).text(),
            'hipo': self.table.item(row, 2).text(),
            'mag': self.table.item(row, 3).text(),
            'row': row
        }
        return data

    def block_event(self):
        s = self.selected_row()
        if not s:
            self.show_warning('Seleccione un evento de la tabla.')
            return
        
        msg = QMessageBox(self)
        msg.setWindowTitle('Confirmar Bloqueo')
        msg.setText(f"¿Desea bloquear el evento del {s['fecha']}?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setIcon(QMessageBox.NoIcon)
        
        if msg.exec() == QMessageBox.Yes:
            # Aquí se podría llamar a GestorSismo.tomar_elecc_evento_sismico
            for c in range(self.table.columnCount()):
                item = self.table.item(s['row'], c)
                if item:
                    item.setBackground(QColor('#ffecb3'))
            
            self.show_success('Evento bloqueado correctamente')

    def view_details(self):
        s = self.selected_row()
        if not s:
            self.show_warning('Seleccione un evento de la tabla.')
            return
        
        msg = QMessageBox(self)
        msg.setWindowTitle('📋 Detalles del Evento Sísmico')
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"""
        <h3 style='color: #1976d2;'>Información del Evento</h3>
        <table style='margin-top: 10px;'>
            <tr><td style='padding: 5px; font-weight: 600;'>📅 Fecha:</td><td style='padding: 5px;'>{s['fecha']}</td></tr>
            <tr><td style='padding: 5px; font-weight: 600;'>📍 Epicentro:</td><td style='padding: 5px;'>{s['epic']}</td></tr>
            <tr><td style='padding: 5px; font-weight: 600;'>🌐 Hipocentro:</td><td style='padding: 5px;'>{s['hipo']}</td></tr>
            <tr><td style='padding: 5px; font-weight: 600;'>📏 Magnitud:</td><td style='padding: 5px;'>{s['mag']}</td></tr>
        </table>
        """)
        msg.exec()

    def confirm_event(self):
        s = self.selected_row()
        if not s:
            self.show_warning('Seleccione un evento de la tabla.')
            return
        
        msg = QMessageBox(self)
        msg.setWindowTitle('Confirmar Evento')
        msg.setText(f"¿Está seguro de confirmar el evento del {s['fecha']}?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setIcon(QMessageBox.NoIcon)
        
        if msg.exec() == QMessageBox.Yes:
            # Aquí se podría validar con GestorSismo antes de cambiar estado
            for c in range(self.table.columnCount()):
                item = self.table.item(s['row'], c)
                if item:
                    item.setBackground(QColor('#c8e6c9'))
            
            self.show_success('Evento confirmado correctamente')

    def reject_event(self):
        s = self.selected_row()
        if not s:
            self.show_warning('Seleccione un evento de la tabla.')
            return
        
        msg = QMessageBox(self)
        msg.setWindowTitle('Rechazar Evento')
        msg.setText(f"¿Está seguro de rechazar el evento del {s['fecha']}?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setIcon(QMessageBox.NoIcon)
        
        if msg.exec() == QMessageBox.Yes:
            for c in range(self.table.columnCount()):
                item = self.table.item(s['row'], c)
                if item:
                    item.setBackground(QColor('#ffcdd2'))
            
            self.show_success('Evento rechazado')

    def request_expert(self):
        s = self.selected_row()
        if not s:
            self.show_warning('Seleccione un evento de la tabla.')
            return
        
        msg = QMessageBox(self)
        msg.setWindowTitle('Solicitar Revisión Experta')
        msg.setText(f"¿Desea solicitar revisión experta para el evento del {s['fecha']}?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setIcon(QMessageBox.NoIcon)
        
        if msg.exec() == QMessageBox.Yes:
            for c in range(self.table.columnCount()):
                item = self.table.item(s['row'], c)
                if item:
                    item.setBackground(QColor('#ffe0b2'))
            
            self.show_success('Solicitud enviada al experto')
    
    def show_success(self, message):
        """Muestra un mensaje de éxito minimalista"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('✅ Éxito')
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QPushButton {
                min-width: 80px;
                padding: 8px;
            }
        """)
        msg.exec()
    
    def show_warning(self, message):
        """Muestra un mensaje de advertencia minimalista"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('⚠️ Advertencia')
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QPushButton {
                min-width: 80px;
                padding: 8px;
            }
        """)
        msg.exec()


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
