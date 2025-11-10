import sys
import os
import csv

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel, QAbstractItemView
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, csv_path=None):
        super().__init__()
        self.setWindowTitle('Administrador de Eventos - PySide6')
        self.resize(900, 600)

        self.csv_path = csv_path or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'eventos_sismicos.csv')

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        header = QLabel('Eventos pendientes de revisión')
        header.setStyleSheet('font-size:18px; font-weight:600; padding:8px;')
        layout.addWidget(header)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['Fecha/Hora', 'Epicentro (lat,lon)', 'Hipocentro (lat,lon)', 'Magnitud'])
        # Usar constantes de QAbstractItemView para compatibilidad
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.table, stretch=1)

        btn_layout = QHBoxLayout()
        self.btn_block = QPushButton('🔒 Bloquear evento')
        self.btn_details = QPushButton('🔍 Ver detalles')
        self.btn_confirm = QPushButton('✅ Confirmar')
        self.btn_reject = QPushButton('❌ Rechazar')
        self.btn_expert = QPushButton('🔔 Solicitar experto')

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
        for i, r in enumerate(rows):
            fecha = r.get('fecha_hora_ocurrencia', '')
            epic = f"{r.get('latitud_epicentro','')} , {r.get('longitud_epicentro','')}"
            hipo = f"{r.get('latitud_hipocentro','')} , {r.get('longitud_hipocentro','')}"
            mag = r.get('valor_magnitud','')
            self.table.setItem(i, 0, QTableWidgetItem(fecha))
            self.table.setItem(i, 1, QTableWidgetItem(epic))
            self.table.setItem(i, 2, QTableWidgetItem(hipo))
            self.table.setItem(i, 3, QTableWidgetItem(mag))

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
            QMessageBox.information(self, 'Seleccionar', 'Seleccione un evento primero.')
            return
        # Aquí se podría llamar a GestorSismo.tomar_elecc_evento_sismico
        QMessageBox.information(self, 'Bloqueado', f"Evento en {s['fecha']} bloqueado (simulado).")
        # Visual feedback
        from PySide6.QtGui import QColor
        for c in range(self.table.columnCount()):
            item = self.table.item(s['row'], c)
            if item:
                item.setBackground(QColor('lightgray'))

    def view_details(self):
        s = self.selected_row()
        if not s:
            QMessageBox.information(self, 'Seleccionar', 'Seleccione un evento primero.')
            return
        detalle = f"Fecha: {s['fecha']}\nEpicentro: {s['epic']}\nHipocentro: {s['hipo']}\nMagnitud: {s['mag']}"
        QMessageBox.information(self, 'Detalles del evento', detalle)

    def confirm_event(self):
        s = self.selected_row()
        if not s:
            QMessageBox.information(self, 'Seleccionar', 'Seleccione un evento primero.')
            return
        # Aquí se podría validar con GestorSismo antes de cambiar estado
        QMessageBox.information(self, 'Confirmado', f"Evento {s['fecha']} confirmado (simulado).")

    def reject_event(self):
        s = self.selected_row()
        if not s:
            QMessageBox.information(self, 'Seleccionar', 'Seleccione un evento primero.')
            return
        QMessageBox.information(self, 'Rechazado', f"Evento {s['fecha']} rechazado (simulado).")

    def request_expert(self):
        s = self.selected_row()
        if not s:
            QMessageBox.information(self, 'Seleccionar', 'Seleccione un evento primero.')
            return
        QMessageBox.information(self, 'Solicitado', f"Se solicitó revisión experta para {s['fecha']} (simulado).")


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
