from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QLabel, QPushButton, QVBoxLayout, QMessageBox ,QHBoxLayout ,QTableWidget, QTableWidgetItem, QAbstractItemView
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
        self.setWindowTitle("Detalles de la Factura")
        self.setFixedSize(400, 200)  # Ajusta el tamaño según tus necesidades

        self.factura_id = factura_id
        self.dni_ruc = dni_ruc

        layout = QVBoxLayout()

        # Layout para los detalles
        details_layout = QHBoxLayout()
        
        # Etiquetas y campos de texto
        id_label = QLabel(f"ID Factura: {factura_id}")
        dni_ruc_label = QLabel(f"DNI/RUC: {dni_ruc}")
        self.name_label = QLabel("Nombre Cliente: Cargando...")

        details_layout.addWidget(id_label)
        details_layout.addStretch()
        details_layout.addWidget(dni_ruc_label)

        layout.addLayout(details_layout)
        layout.addWidget(self.name_label)

        # Botón para cerrar el diálogo
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)

        # Cargar el nombre completo del cliente
        self.load_client_name()

    def load_client_name(self):
        try:
            connection = connect_to_db()  # Asegúrate de que esta función esté definida
            if connection:
                cursor = connection.cursor()
                # Consulta para obtener el nombre completo del cliente
                query = """
                SELECT c.Nombre
                FROM Clientes c
                JOIN Facturas f ON c.ClienteID = f.ClienteID
                WHERE f.FacturasID = ?
                """
                cursor.execute(query, (self.factura_id,))
                client_name = cursor.fetchone()
                if client_name:
                    self.name_label.setText(f"Nombre Cliente: {client_name[0]}")
                else:
                    self.name_label.setText("Nombre Cliente: No encontrado")
                connection.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el nombre del cliente: {e}")
