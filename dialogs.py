from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QHeaderView, QLabel, QPushButton, QVBoxLayout, QMessageBox ,QHBoxLayout ,QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt6.QtCore import Qt
from utils import is_valid_dni, is_valid_phone, is_valid_email
from conn import connect_to_db
from functools import partial
from PyQt6.QtCore import pyqtSignal

class EditUserDialog(QDialog):
    def __init__(self, user_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Usuario")
        self.setFixedSize(400, 300)
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.dni_ruc_input = QLineEdit(self.user_data['dni_ruc'])
        self.name_input = QLineEdit(self.user_data['nombre'])
        self.paterno_input = QLineEdit(self.user_data['apellido_paterno'])
        self.materno_input = QLineEdit(self.user_data['apellido_materno'])
        self.address_input = QLineEdit(self.user_data['direccion'])
        self.phone_input = QLineEdit(self.user_data['telefono'])
        self.email_input = QLineEdit(self.user_data['correo'])

        layout.addRow("DNI/RUC:", self.dni_ruc_input)
        layout.addRow("Nombre:", self.name_input)
        layout.addRow("Apellido Paterno:", self.paterno_input)
        layout.addRow("Apellido Materno:", self.materno_input)
        layout.addRow("Dirección:", self.address_input)
        layout.addRow("Teléfono:", self.phone_input)
        layout.addRow("Correo:", self.email_input)

        button_box = QVBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.on_save)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)
        
        layout.addRow("", button_box)

        self.setLayout(layout)

    def on_save(self):
        if self.validate_inputs():
            self.accept()  # Cierra el diálogo y devuelve QDialog.DialogCode.Accepted
        else:
            # Mantener el diálogo abierto si hay errores de validación
            pass

    def validate_inputs(self):
        valid = True
        errors = []
        
        if not is_valid_dni(self.dni_ruc_input.text()):
            errors.append("DNI/RUC inválido.")
            valid = False
        if not is_valid_phone(self.phone_input.text()):
            errors.append("Teléfono inválido.")
            valid = False
        if not is_valid_email(self.email_input.text()):
            errors.append("Correo electrónico inválido.")
            valid = False
        
        if not valid:
            QMessageBox.warning(self, "Errores de Validación", "\n".join(errors))
        
        return valid

    def get_user_data(self):
        return {
            'dni_ruc': self.dni_ruc_input.text(),
            'nombre': self.name_input.text(),
            'apellido_paterno': self.paterno_input.text(),
            'apellido_materno': self.materno_input.text(),
            'direccion': self.address_input.text(),
            'telefono': self.phone_input.text(),
            'correo': self.email_input.text()
        }

    def closeEvent(self, event):
        # Asegúrate de que el diálogo se maneje correctamente al cerrarse con la "X"
        if self.result() == QDialog.DialogCode.Rejected:
            self.reject()  # Asegúrate de rechazar el diálogo si se cierra con la "X"
        event.accept()

    
class UserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nuevo Usuario")
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.dni_ruc_input = QLineEdit()
        self.name_input = QLineEdit()
        self.paterno_input = QLineEdit()
        self.materno_input = QLineEdit()
        self.address_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        layout.addRow("DNI/RUC:", self.dni_ruc_input)
        layout.addRow("Nombre:", self.name_input)
        layout.addRow("Apellido Paterno:", self.paterno_input)
        layout.addRow("Apellido Materno:", self.materno_input)
        layout.addRow("Dirección:", self.address_input)
        layout.addRow("Teléfono:", self.phone_input)
        layout.addRow("Correo:", self.email_input)

        button_box = QVBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.on_save)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)
        
        layout.addRow("", button_box)

        self.setLayout(layout)

    def on_save(self):
        if self.validate_inputs():
            self.save_user()
            self.accept()  # Cierra el diálogo si se guarda correctamente
        else:
            QMessageBox.warning(self, "Error", "Por favor, corrige los errores antes de guardar.")

    def validate_inputs(self):
        valid = True
        errors = []
        
        if not is_valid_dni(self.dni_ruc_input.text()):
            errors.append("DNI/RUC inválido.")
            valid = False
        if not is_valid_phone(self.phone_input.text()):
            errors.append("Teléfono inválido.")
            valid = False
        if not is_valid_email(self.email_input.text()):
            errors.append("Correo electrónico inválido.")
            valid = False
        
        if not valid:
            QMessageBox.warning(self, "Errores de Validación", "\n".join(errors))
        
        return valid

    def save_user(self):
        # Guardar datos del usuario en la base de datos
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO Clientes ([DNI/RUC], Nombre, ApellidoPaterno, ApellidoMaterno, Dirección, Teléfono, Correo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            user_data = (
                self.dni_ruc_input.text(),
                self.name_input.text(),
                self.paterno_input.text(),
                self.materno_input.text(),
                self.address_input.text(),
                self.phone_input.text(),
                self.email_input.text()
            )
            cursor.execute(query, user_data)
            connection.commit()
            connection.close()


class SearchClientDialog(QDialog):
    client_selected = pyqtSignal(str, str)  # Señal para pasar DNI/RUC y nombre completo

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Buscar Cliente")
        self.setFixedSize(400, 300)
        self.init_ui()
        self.load_all_clients()  # Cargar todos los clientes al iniciar el diálogo

    def init_ui(self):
        layout = QVBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar cliente por DNI/RUC o nombre...")
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.search_clients)
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["DNI/RUC", "Nombre completo", "Seleccionar"])
        self.results_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.results_table.cellClicked.connect(self.select_client)
        layout.addWidget(self.results_table)

        self.setLayout(layout)

    def load_all_clients(self):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT [DNI/RUC], CONCAT(Nombre, ' ', ApellidoPaterno, ' ', ApellidoMaterno) AS nombre_completo
            FROM Clientes
            """
            cursor.execute(query)
            clients = cursor.fetchall()
            self.results_table.setRowCount(0)
            for row, client in enumerate(clients):
                self.results_table.insertRow(row)
                self.results_table.setItem(row, 0, QTableWidgetItem(client[0]))
                self.results_table.setItem(row, 1, QTableWidgetItem(client[1]))
                select_button = QPushButton("Seleccionar")
                self.results_table.setCellWidget(row, 2, select_button)
                select_button.clicked.connect(lambda checked, client=client: self.select_client(client))
            connection.close()

    def search_clients(self):
        search_text = self.search_input.text()
        if not search_text:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingresa un término de búsqueda.")
            return

        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT [DNI/RUC], CONCAT(Nombre, ' ', ApellidoPaterno, ' ', ApellidoMaterno) AS nombre_completo
            FROM Clientes
            WHERE [DNI/RUC] LIKE ? 
            OR CONCAT(Nombre, ' ', ApellidoPaterno, ' ', ApellidoMaterno) LIKE ?
            """
            search_pattern = f'%{search_text}%'
            cursor.execute(query, (search_pattern, search_pattern))
            clients = cursor.fetchall()
            self.results_table.setRowCount(0)
            for row, client in enumerate(clients):
                self.results_table.insertRow(row)
                self.results_table.setItem(row, 0, QTableWidgetItem(client[0]))
                self.results_table.setItem(row, 1, QTableWidgetItem(client[1]))
                select_button = QPushButton("Seleccionar")
                self.results_table.setCellWidget(row, 2, select_button)
                select_button.clicked.connect(lambda checked, client=client: self.select_client(client))
            connection.close()

    def select_client(self, client):
        self.client_selected.emit(client[0], client[1])  # Emitir la señal con DNI/RUC y nombre completo
        self.accept()


class FacturaDetailsDialog(QDialog):
    def __init__(self, factura_id, dni_ruc, parent=None):
        super().__init__(parent)
        self.factura_id = factura_id
        self.dni_ruc = dni_ruc
        self.init_ui()
        self.load_invoice_details()

    def init_ui(self):
        self.setWindowTitle("Detalles de la Factura")
        self.setFixedSize(800, 600)  # Ajusta el tamaño del diálogo según sea necesario

        # Crear layout principal
        main_layout = QVBoxLayout()

        # Crear layout para ID factura y DNI/RUC
        top_layout = QHBoxLayout()
        id_label = QLabel(f"ID Factura: {self.factura_id}")
        dni_ruc_label = QLabel(f"DNI/RUC: {self.dni_ruc}")

        # Crear etiqueta para nombre completo
        self.nombre_completo_label = QLabel("Nombre completo: Cargando...")

        top_layout.addWidget(id_label)
        top_layout.addWidget(dni_ruc_label)
        top_layout.addWidget(self.nombre_completo_label)

        main_layout.addLayout(top_layout)

        # Crear tabla para detalles de la factura
        self.details_table = QTableWidget()
        self.details_table.setColumnCount(4)
        self.details_table.setHorizontalHeaderLabels(["Servicio", "Cantidad", "Precio Unitario", "Total"])

        # Configurar el ajuste de columnas
        header = self.details_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Servicio
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Cantidad
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Precio Unitario
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Total

        # Agregar la tabla al layout principal
        main_layout.addWidget(self.details_table)

        # Crear botones de cancelar y pagar
        buttons_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        pay_button = QPushButton("Pagar")
        pay_button.clicked.connect(self.pay_invoice)

        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(pay_button)

        main_layout.addLayout(buttons_layout)

        # Establecer el layout en el diálogo
        self.setLayout(main_layout)

    def load_invoice_details(self):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            
            # Obtener nombre completo del cliente
            query = """
            SELECT c.Nombre + ' ' + c.ApellidoPaterno + ' ' + c.ApellidoMaterno AS NombreCompleto
            FROM Clientes c
            JOIN Facturas f ON c.ClienteID = f.ClienteID
            WHERE f.FacturasID = ?
            """
            cursor.execute(query, (self.factura_id,))
            result = cursor.fetchone()
            if result:
                self.nombre_completo_label.setText(f"Nombre completo: {result[0]}")
            
            # Obtener detalles de la factura
            query = """
            SELECT f.Descripcion
            FROM Facturas f
            WHERE f.FacturasID = ?
            """
            cursor.execute(query, (self.factura_id,))
            descripcion = cursor.fetchone()[0]
            services = self.parse_description(descripcion)
            
            # Limpiar la tabla antes de agregar datos
            self.details_table.setRowCount(0)
            
            for service_id, quantity in services:
                # Obtener el nombre del servicio y el precio unitario
                query = """
                SELECT NombreServicio, Precio
                FROM Servicios
                WHERE ServiciosID = ?
                """
                cursor.execute(query, (service_id,))
                service_data = cursor.fetchone()
                if service_data:
                    service_name = service_data[0]
                    unit_price = service_data[1]
                    
                    # Calcular total
                    total = quantity * unit_price
                    
                    # Insertar fila en la tabla
                    row_position = self.details_table.rowCount()
                    self.details_table.insertRow(row_position)
                    self.details_table.setItem(row_position, 0, QTableWidgetItem(service_name))
                    self.details_table.setItem(row_position, 1, QTableWidgetItem(str(quantity)))
                    self.details_table.setItem(row_position, 2, QTableWidgetItem(f"{unit_price:.2f}"))
                    self.details_table.setItem(row_position, 3, QTableWidgetItem(f"{total:.2f}"))

            connection.close()

    def parse_description(self, description):
        # Parsear la descripción para obtener pares (service_id, quantity)
        services = []
        items = description.split(',')
        for item in items:
            service_id, quantity = item.split('-')
            services.append((int(service_id), int(quantity)))
        return services

    def pay_invoice(self):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()

            # Obtener el monto total de la factura
            query = """
            SELECT MontoTotal
            FROM Facturas
            WHERE FacturasID = ?
            """
            cursor.execute(query, (self.factura_id,))
            result = cursor.fetchone()
            if result:
                monto_pago = result[0]

                # Actualizar el estado de la factura
                query = """
                UPDATE Facturas
                SET Estado = 'Pagado'
                WHERE FacturasID = ?
                """
                cursor.execute(query, (self.factura_id,))

                # Insertar el pago en la tabla Pagos
                query = """
                INSERT INTO Pagos (FacturasID, MontoPago, MétodoPago)
                VALUES (?, ?, 'Efectivo')
                """
                cursor.execute(query, (self.factura_id, monto_pago))
                
                connection.commit()
                connection.close()
                
                QMessageBox.information(self, "Éxito", "Factura marcada como pagada y registro de pago creado.")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "No se encontró el monto total para la factura.")
        else:
            QMessageBox.warning(self, "Error", "No se pudo conectar a la base de datos.")



class AddServiceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Agregar Servicio")
        self.setFixedSize(400, 200)
        
        # Crear layout principal
        layout = QVBoxLayout()

        # Crear campos de entrada
        self.name_input = QLineEdit()
        self.description_input = QLineEdit()
        self.price_input = QLineEdit()

        # Crear etiquetas
        name_label = QLabel("Nombre del servicio:")
        description_label = QLabel("Descripción:")
        price_label = QLabel("Precio:")

        # Crear botones
        buttons_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancelar")
        add_button = QPushButton("Agregar")

        # Conectar señales
        cancel_button.clicked.connect(self.reject)
        add_button.clicked.connect(self.add_service)

        # Agregar widgets al layout
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(description_label)
        layout.addWidget(self.description_input)
        layout.addWidget(price_label)
        layout.addWidget(self.price_input)
        
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(add_button)
        layout.addLayout(buttons_layout)

        # Establecer el layout en el diálogo
        self.setLayout(layout)

    def add_service(self):
        # Obtener los valores de los campos
        name = self.name_input.text()
        description = self.description_input.text()
        price_text = self.price_input.text()

        # Validar la entrada
        if not name or not description or not price_text:
            QMessageBox.warning(self, "Advertencia", "Por favor, completa todos los campos.")
            return

        try:
            price = float(price_text)
        except ValueError:
            QMessageBox.warning(self, "Error", "El precio debe ser un número válido.")
            return

        # Insertar el nuevo servicio en la base de datos
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO Servicios (NombreServicio, Descripcion, Precio)
            VALUES (?, ?, ?)
            """
            cursor.execute(query, (name, description, price))
            connection.commit()
            connection.close()
            QMessageBox.information(self, "Éxito", "Servicio agregado con éxito")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "No se pudo conectar a la base de datos")