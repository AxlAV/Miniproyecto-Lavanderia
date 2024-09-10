import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QGuiApplication, QIcon
from conn import connect_to_db
from datetime import datetime

class EditUserDialog(QDialog):
    def __init__(self, user_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Usuario")
        self.setFixedSize(300, 300)

        # Crear el layout del diálogo
        layout = QFormLayout()

        # Crear campos de entrada
        self.nombre_input = QLineEdit(user_data['nombre'])
        self.apellido_paterno_input = QLineEdit(user_data['apellido_paterno'])
        self.apellido_materno_input = QLineEdit(user_data['apellido_materno'])
        self.direccion_input = QLineEdit(user_data['direccion'])
        self.telefono_input = QLineEdit(user_data['telefono'])
        self.correo_input = QLineEdit(user_data['correo'])

        layout.addRow("Nombre:", self.nombre_input)
        layout.addRow("Apellido Paterno:", self.apellido_paterno_input)
        layout.addRow("Apellido Materno:", self.apellido_materno_input)
        layout.addRow("Dirección:", self.direccion_input)
        layout.addRow("Teléfono:", self.telefono_input)
        layout.addRow("Correo electrónico:", self.correo_input)

        # Botones de aceptar y cancelar
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def get_user_data(self):
        return {
            'nombre': self.nombre_input.text(),
            'apellido_paterno': self.apellido_paterno_input.text(),
            'apellido_materno': self.apellido_materno_input.text(),
            'direccion': self.direccion_input.text(),
            'telefono': self.telefono_input.text(),
            'correo': self.correo_input.text()
        }

class UserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Usuario")
        self.setFixedSize(300, 300)

        # Crear el layout del diálogo
        layout = QFormLayout()

        # Crear campos de entrada
        self.nombre_input = QLineEdit()
        self.apellido_paterno_input = QLineEdit()
        self.apellido_materno_input = QLineEdit()
        self.direccion_input = QLineEdit()
        self.telefono_input = QLineEdit()
        self.correo_input = QLineEdit()

        layout.addRow("Nombre:", self.nombre_input)
        layout.addRow("Apellido Paterno:", self.apellido_paterno_input)
        layout.addRow("Apellido Materno:", self.apellido_materno_input)
        layout.addRow("Dirección:", self.direccion_input)
        layout.addRow("Teléfono:", self.telefono_input)
        layout.addRow("Correo electrónico:", self.correo_input)

        # Botones de aceptar y cancelar
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def get_user_data(self):
        return {
            'nombre': self.nombre_input.text(),
            'apellido_paterno': self.apellido_paterno_input.text(),
            'apellido_materno': self.apellido_materno_input.text(),
            'direccion': self.direccion_input.text(),
            'telefono': self.telefono_input.text(),
            'correo': self.correo_input.text()
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Factura lavandería")
        self.setGeometry(100, 100, 800, 600)

        # Crear un QStackedWidget para gestionar múltiples layouts
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Crear layouts
        self.create_main_layout()
        self.create_clientes_layout()

        # Inicialmente mostrar el layout principal
        self.stacked_widget.setCurrentIndex(0)

    def create_main_layout(self):
        # Crear el layout principal
        main_layout = QVBoxLayout()

        # Crear los botones
        buttons_info = [
            ("Clientes", 200, 60),
            ("Facturas", 200, 60),
            ("Pagos", 200, 60),
            ("Servicios", 200, 60),
            ("Reportes", 200, 60),
            ("Configuración y Seguridad", 200, 60)
        ]

        for text, width, height in buttons_info:
            button = QPushButton(text)
            button.setFixedSize(width, height)
            button.setStyleSheet("font-size: 16px;")
            button.clicked.connect(self.handle_button_click)
            main_layout.addWidget(button)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.stacked_widget.addWidget(main_widget)

    def create_clientes_layout(self):
        # Crear el layout de clientes
        clientes_layout = QVBoxLayout()

        # Crear el buscador y el botón de búsqueda
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar usuario...")
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.search_users)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        clientes_layout.addLayout(search_layout)

        # Crear la tabla de usuarios
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(7)  # Número de columnas
        self.user_table.setHorizontalHeaderLabels(["Nombre", "Apellido Paterno", "Apellido Materno", "Dirección", "Teléfono", "Correo", "Fecha de Registro"])
        self.user_table.horizontalHeader().setStretchLastSection(True)  # Ajustar tamaño de la última columna
        self.user_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # Hacer que las celdas no sean editables
        self.user_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)  # Seleccionar filas completas
        clientes_layout.addWidget(self.user_table)

        # Crear botones de acción (Eliminar, Editar) y el botón de añadir usuario
        actions_layout = QHBoxLayout()
        delete_button = QPushButton(QIcon("img/delete_icon.png"), "Eliminar")  # Asumiendo que tienes un ícono para eliminar
        delete_button.clicked.connect(self.delete_user)
        edit_button = QPushButton(QIcon("img/edit_icon.png"), "Editar")  # Asumiendo que tienes un ícono para editar
        edit_button.clicked.connect(self.edit_user)
        actions_layout.addWidget(delete_button)
        actions_layout.addWidget(edit_button)

        add_user_button = QPushButton("Crear Nuevo Usuario")
        add_user_button.clicked.connect(self.create_user)
        actions_layout.addWidget(add_user_button)

        clientes_layout.addLayout(actions_layout)

        # Crear un widget para el layout de clientes
        clientes_widget = QWidget()
        clientes_widget.setLayout(clientes_layout)
        self.stacked_widget.addWidget(clientes_widget)

        # Cargar los clientes desde la base de datos al iniciar el layout
        self.load_clientes()

    def format_date(self, date_obj):
        if isinstance(date_obj, datetime):
            # Formatear la fecha en el formato deseado
            return date_obj.strftime("%d-%m-%Y %H:%M:%S")
        return date_obj  # Si no es un objeto datetime, devolverlo tal cual

    def load_clientes(self):
        # Conectar a la base de datos y cargar los clientes
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT Nombre, ApellidoPaterno, ApellidoMaterno, Dirección, Teléfono, Correo, FechaRegistro
            FROM Clientes
            """
            cursor.execute(query)
            clientes = cursor.fetchall()
            self.user_table.setRowCount(0)  # Limpiar la tabla antes de añadir nuevos datos
            
            for cliente in clientes:
                row_position = self.user_table.rowCount()
                self.user_table.insertRow(row_position)
                for col, data in enumerate(cliente):
                    if col == 6 and isinstance(data, datetime):  # Formatear la fecha de registro si es un objeto datetime
                        data = self.format_date(data)
                    item = QTableWidgetItem(str(data))
                    self.user_table.setItem(row_position, col, item)
            
            connection.close()

    def search_users(self):
        search_text = self.search_input.text()
        if not search_text:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingresa un término de búsqueda.")
            return
        
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT Nombre, ApellidoPaterno, ApellidoMaterno, Dirección, Teléfono, Correo, FechaRegistro
            FROM Clientes
            WHERE Nombre LIKE ?
            """
            cursor.execute(query, f'%{search_text}%')
            clientes = cursor.fetchall()
            
            self.user_table.setRowCount(0)  # Limpiar la tabla antes de añadir nuevos datos
            for cliente in clientes:
                row_position = self.user_table.rowCount()
                self.user_table.insertRow(row_position)
                for col, data in enumerate(cliente):
                    if col == 6 and isinstance(data, datetime):  # Formatear la fecha de registro si es un objeto datetime
                        data = self.format_date(data)
                    item = QTableWidgetItem(str(data))
                    self.user_table.setItem(row_position, col, item)
            
            connection.close()

    def delete_user(self):
        selected_items = self.user_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un usuario para eliminar.")
            return
        
        selected_row = self.user_table.currentRow()
        user_name = self.user_table.item(selected_row, 0).text()

        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Clientes WHERE Nombre = ?", user_name)
            connection.commit()
            connection.close()

            self.user_table.removeRow(selected_row)
            QMessageBox.information(self, "Éxito", "Usuario eliminado.")

    def edit_user(self):
        selected_row = self.user_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un usuario para editar.")
            return
        
        # Obtener los datos del usuario seleccionado
        user_data = {
            'nombre': self.user_table.item(selected_row, 0).text(),
            'apellido_paterno': self.user_table.item(selected_row, 1).text(),
            'apellido_materno': self.user_table.item(selected_row, 2).text(),
            'direccion': self.user_table.item(selected_row, 3).text(),
            'telefono': self.user_table.item(selected_row, 4).text(),
            'correo': self.user_table.item(selected_row, 5).text()
        }

        dialog = EditUserDialog(user_data, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_user_data()
            try:
                connection = connect_to_db()
                if connection:
                    cursor = connection.cursor()
                    cursor.execute("""
                        UPDATE Clientes 
                        SET Nombre = ?, ApellidoPaterno = ?, ApellidoMaterno = ?, Dirección = ?, Teléfono = ?, Correo = ?
                        WHERE Nombre = ?
                    """, 
                    updated_data['nombre'],
                    updated_data['apellido_paterno'],
                    updated_data['apellido_materno'],
                    updated_data['direccion'],
                    updated_data['telefono'],
                    updated_data['correo'],
                    user_data['nombre'])  # Usar el nombre antiguo para identificar el registro a actualizar

                    connection.commit()
                    connection.close()

                    # Actualizar los datos en la tabla
                    self.user_table.setItem(selected_row, 0, QTableWidgetItem(updated_data['nombre']))
                    self.user_table.setItem(selected_row, 1, QTableWidgetItem(updated_data['apellido_paterno']))
                    self.user_table.setItem(selected_row, 2, QTableWidgetItem(updated_data['apellido_materno']))
                    self.user_table.setItem(selected_row, 3, QTableWidgetItem(updated_data['direccion']))
                    self.user_table.setItem(selected_row, 4, QTableWidgetItem(updated_data['telefono']))
                    self.user_table.setItem(selected_row, 5, QTableWidgetItem(updated_data['correo']))

                    QMessageBox.information(self, "Éxito", "Usuario editado.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al editar el usuario: {e}")


    def create_user(self):
        dialog = UserDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_data = dialog.get_user_data()
            try:
                connection = connect_to_db()
                if connection:
                    cursor = connection.cursor()
                    
                    # Insertar datos en la base de datos
                    cursor.execute(
                        "INSERT INTO Clientes (Nombre, ApellidoPaterno, ApellidoMaterno, Dirección, Teléfono, Correo, FechaRegistro) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        user_data['nombre'],
                        user_data['apellido_paterno'],
                        user_data['apellido_materno'],
                        user_data['direccion'],
                        user_data['telefono'],
                        user_data['correo'],
                        datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # Fecha de registro
                    )
                    connection.commit()
                    connection.close()
                    
                    # Agregar el nuevo usuario a la tabla
                    row_position = self.user_table.rowCount()
                    self.user_table.insertRow(row_position)
                    self.user_table.setItem(row_position, 0, QTableWidgetItem(user_data['nombre']))
                    self.user_table.setItem(row_position, 1, QTableWidgetItem(user_data['apellido_paterno']))
                    self.user_table.setItem(row_position, 2, QTableWidgetItem(user_data['apellido_materno']))
                    self.user_table.setItem(row_position, 3, QTableWidgetItem(user_data['direccion']))
                    self.user_table.setItem(row_position, 4, QTableWidgetItem(user_data['telefono']))
                    self.user_table.setItem(row_position, 5, QTableWidgetItem(user_data['correo']))
                    self.user_table.setItem(row_position, 6, QTableWidgetItem(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))

                    QMessageBox.information(self, "Éxito", "Nuevo usuario creado.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear el usuario: {e}")

    def handle_button_click(self):
        # Cambiar el layout mostrado según el texto del botón
        sender = self.sender()
        if sender.text() == "Clientes":
            self.stacked_widget.setCurrentIndex(1)
        else:
            self.stacked_widget.setCurrentIndex(0)  # Volver al layout principal

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
