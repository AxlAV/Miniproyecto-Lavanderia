from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QHeaderView, QLabel, QPushButton, QVBoxLayout, QMessageBox ,QHBoxLayout ,QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt6.QtCore import Qt
from utils import is_valid_dni, is_valid_phone, is_valid_email
from conn import connect_to_db
from functools import partial
from PyQt6.QtCore import pyqtSignal

class ReporteFacturasPorClienteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reporte de Facturas por Cliente")
        self.setFixedSize(800, 600)  # Ajustar el tamaño del diálogo

        # Layout principal
        layout = QVBoxLayout()

        # Campo de búsqueda de cliente (DNI/RUC)
        search_layout = QHBoxLayout()
        search_label = QLabel("DNI/RUC del Cliente:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ingrese DNI o RUC del cliente")
        
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.search_facturas)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        
        layout.addLayout(search_layout)

        # Tabla para mostrar las facturas
        self.facturas_table = QTableWidget()
        self.facturas_table.setColumnCount(4)
        self.facturas_table.setHorizontalHeaderLabels(["Número de Factura", "Fecha de Emisión", "Total", "Estado"])
        
        # Configurar la tabla
        header = self.facturas_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Ajustar columnas al ancho
        self.facturas_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        table_layout = QHBoxLayout()
        table_layout.addWidget(self.facturas_table)
        layout.addLayout(table_layout)

        # Área para mostrar el resumen
        self.summary_label = QLabel()
        layout.addWidget(self.summary_label)

        # Botón para cerrar el diálogo
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def search_facturas(self):
        dni_ruc = self.search_input.text()

        if not dni_ruc:
            QMessageBox.warning(self, "Advertencia", "Debe ingresar el DNI o RUC del cliente.")
            return
        
        # Conectar a la base de datos
        connection = connect_to_db()  # Asegúrate de que esta función esté definida y conecte correctamente
        if connection:
            cursor = connection.cursor()

            # Consulta para obtener las facturas asociadas al cliente
            query = """
            SELECT f.FacturasID, f.FechaFactura, f.MontoTotal, f.Estado
            FROM Facturas f
            JOIN Clientes c ON f.ClienteID = c.ClienteID
            WHERE c.[DNI/RUC] = ?
            """
            cursor.execute(query, (dni_ruc,))
            facturas = cursor.fetchall()
            
            if facturas:
                # Limpiar la tabla antes de mostrar los resultados
                self.facturas_table.setRowCount(0)
                
                # Contadores para el resumen
                num_pagadas = 0
                num_pendientes = 0
                
                # Poner los resultados en la tabla
                for factura in facturas:
                    row_position = self.facturas_table.rowCount()
                    self.facturas_table.insertRow(row_position)
                    self.facturas_table.setItem(row_position, 0, QTableWidgetItem(str(factura[0])))
                    self.facturas_table.setItem(row_position, 1, QTableWidgetItem(str(factura[1])))
                    self.facturas_table.setItem(row_position, 2, QTableWidgetItem(f"{factura[2]:.2f}"))
                    self.facturas_table.setItem(row_position, 3, QTableWidgetItem(factura[3]))
                    
                    # Contar el estado de la factura
                    if factura[3] == 'Pagado':
                        num_pagadas += 1
                    elif factura[3] == 'Pendiente':
                        num_pendientes += 1
                
                # Mostrar el resumen
                self.summary_label.setText(f"Facturas Pagadas: {num_pagadas} | Facturas Pendientes: {num_pendientes}")
            else:
                QMessageBox.information(self, "Sin Resultados", "No se encontraron facturas para el cliente especificado.")
                self.summary_label.setText("No se encontraron facturas.")
            
            connection.close()
        else:
            QMessageBox.warning(self, "Error", "No se pudo conectar a la base de datos.")



class ReporteServiciosMasSolicitadosDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reporte de Servicios Más Solicitados")
        self.setFixedSize(800, 600)  # Ajustar el tamaño del diálogo

        # Layout principal
        layout = QVBoxLayout()

        # Campo para seleccionar el periodo
        periodo_layout = QHBoxLayout()
        periodo_label = QLabel("Periodo:")
        self.periodo_combo = QComboBox()
        self.periodo_combo.addItems(["Semanal", "Mensual", "Anual"])

        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.search_servicios)

        periodo_layout.addWidget(periodo_label)
        periodo_layout.addWidget(self.periodo_combo)
        periodo_layout.addWidget(search_button)
        
        layout.addLayout(periodo_layout)

        # Tabla para mostrar los servicios
        self.servicios_table = QTableWidget()
        self.servicios_table.setColumnCount(3)
        self.servicios_table.setHorizontalHeaderLabels(["Nombre del Servicio", "Cantidad Solicitada", "Ingreso Total"])
        
        # Configurar la tabla
        header = self.servicios_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Ajustar columnas al ancho
        self.servicios_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        table_layout = QHBoxLayout()
        table_layout.addWidget(self.servicios_table)
        layout.addLayout(table_layout)

        # Botón para cerrar el diálogo
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def search_servicios(self):
        periodo = self.periodo_combo.currentText()

        # Aquí deberás implementar la lógica para definir el rango de fechas según el período seleccionado
        start_date, end_date = self.get_date_range(periodo)

        # Conectar a la base de datos
        connection = connect_to_db()  # Asegúrate de que esta función esté definida y conecte correctamente
        if connection:
            cursor = connection.cursor()

            # Consulta para obtener los servicios más solicitados en el período seleccionado
            query = """
            SELECT s.NombreServicio, COUNT(*) AS CantidadSolicitada, SUM(f.MontoTotal) AS IngresoTotal
            FROM DetalleFacturas df
            JOIN Servicios s ON df.ServiciosID = s.ServiciosID
            JOIN Facturas f ON df.FacturasID = f.FacturasID
            WHERE f.FechaFactura BETWEEN ? AND ?
            GROUP BY s.NombreServicio
            ORDER BY CantidadSolicitada DESC
            """
            cursor.execute(query, (start_date, end_date))
            servicios = cursor.fetchall()
            
            if servicios:
                # Limpiar la tabla antes de mostrar los resultados
                self.servicios_table.setRowCount(0)
                
                # Poner los resultados en la tabla
                for servicio in servicios:
                    row_position = self.servicios_table.rowCount()
                    self.servicios_table.insertRow(row_position)
                    self.servicios_table.setItem(row_position, 0, QTableWidgetItem(servicio[0]))
                    self.servicios_table.setItem(row_position, 1, QTableWidgetItem(str(servicio[1])))
                    self.servicios_table.setItem(row_position, 2, QTableWidgetItem(f"{servicio[2]:.2f}"))
            else:
                QMessageBox.information(self, "Sin Resultados", "No se encontraron servicios en el período especificado.")
            
            connection.close()
        else:
            QMessageBox.warning(self, "Error", "No se pudo conectar a la base de datos.")

    def get_date_range(self, periodo):
        from datetime import datetime, timedelta

        today = datetime.today()
        if periodo == "Semanal":
            start_date = today - timedelta(weeks=1)
        elif periodo == "Mensual":
            start_date = today - timedelta(days=30)
        elif periodo == "Anual":
            start_date = today - timedelta(days=365)
        else:
            start_date = today
        end_date = today

        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
