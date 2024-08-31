import sys, re
from PyQt6.QtWidgets import QApplication, QComboBox, QInputDialog, QStackedWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QWidget, QMessageBox, QDialog, QAbstractItemView, QMenu
from PyQt6.QtGui import QIcon, QAction, QClipboard
from PyQt6.QtCore import Qt
from datetime import datetime
from dialogs import EditUserDialog, UserDialog
from utils import *
from conn import connect_to_db

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Factura lavandería")
        self.setFixedSize(1200, 800)
        # Obtener el tamaño de la pantalla y la ventana
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()

        # Calcular la posición centrada
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        # Ajustar la posición de la ventana
        self.move(x, y)
        self.setGeometry(x, y, 1200, 800)

        # Crear un QStackedWidget para gestionar múltiples layouts
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Crear layouts
        self.create_main_layout()
        self.create_clientes_layout()
        self.create_facturas_layout()

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
        self.user_table.setColumnCount(8)
        self.user_table.setHorizontalHeaderLabels([
            "DNI/RUC", "Nombre", "Apellido Paterno", "Apellido Materno", 
            "Dirección", "Teléfono", "Correo", "Fecha de Registro"
        ])
        self.user_table.horizontalHeader().setStretchLastSection(True)  # Ajustar tamaño de la última columna
        self.user_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # Hacer que las celdas no sean editables
        self.user_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)  # Seleccionar filas completas
        
        # Habilitar la ordenación al hacer clic en las cabeceras
        self.user_table.setSortingEnabled(True)
        clientes_layout.addWidget(self.user_table)

        # Boton eliminar usuario
        actions_layout = QHBoxLayout()
        delete_button = QPushButton(QIcon("img/delete_icon.png"), "Eliminar")  
        delete_button.setStyleSheet("font-size: 16px; height: 50px;")
        delete_button.clicked.connect(self.delete_user)
        actions_layout.addWidget(delete_button)

        # Boton editar usuario
        edit_button = QPushButton(QIcon("img/edit_icon.png"), "Editar")  
        edit_button.setStyleSheet("font-size: 16px; height: 50px;")
        edit_button.clicked.connect(self.edit_user)
        actions_layout.addWidget(edit_button)

        # Boton crear nuevo usuario
        add_user_button = QPushButton(QIcon("img/create_icon.png"), "Crear Nuevo Usuario")
        add_user_button.setStyleSheet("font-size: 16px; height: 50px;")
        add_user_button.clicked.connect(self.create_user)
        actions_layout.addWidget(add_user_button)

        # Asegurar que los botones ocupen el mismo espacio en el layout horizontal
        actions_layout.setSpacing(0)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setStretch(0, 1)
        actions_layout.setStretch(1, 1)
        actions_layout.setStretch(2, 1)

        clientes_layout.addLayout(actions_layout)

        # Crear un widget para el layout de clientes
        clientes_widget = QWidget()
        clientes_widget.setLayout(clientes_layout)
        self.stacked_widget.addWidget(clientes_widget)

        # Cargar los clientes desde la base de datos al iniciar el layout
        self.load_clientes()

        # Conectar el menú contextual para copiar celdas
        self.user_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.user_table.customContextMenuRequested.connect(self.show_context_menu)

    def create_facturas_layout(self):
        # Crear el layout para la factura
        facturas_layout = QVBoxLayout()

        # Crear el buscador de clientes
        search_layout = QHBoxLayout()
        self.client_search_input = QLineEdit()
        self.client_search_input.setPlaceholderText("Buscar cliente por DNI/RUC o nombre...")
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.search_client)
        search_layout.addWidget(self.client_search_input)
        search_layout.addWidget(search_button)
        facturas_layout.addLayout(search_layout)

        # Crear el combo box para seleccionar servicios
        self.service_combo = QComboBox()
        self.service_combo.addItem("Seleccione un servicio")
        # Populate with services from the database
        self.load_services()
        facturas_layout.addWidget(self.service_combo)

        # Botón para añadir servicio
        add_service_button = QPushButton("Agregar Servicio")
        add_service_button.clicked.connect(self.add_service_to_invoice)
        facturas_layout.addWidget(add_service_button)

        # Crear la tabla de servicios seleccionados
        self.services_table = QTableWidget()
        self.services_table.setColumnCount(4)
        self.services_table.setHorizontalHeaderLabels(["Servicio", "Cantidad", "Precio Unitario", "Total"])
        self.services_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # No editable
        self.services_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        facturas_layout.addWidget(self.services_table)

        # Botón para guardar factura
        save_invoice_button = QPushButton("Guardar Factura")
        save_invoice_button.clicked.connect(self.save_invoice)
        facturas_layout.addWidget(save_invoice_button)

        # Crear un widget para el layout de facturas
        facturas_widget = QWidget()
        facturas_widget.setLayout(facturas_layout)
        self.stacked_widget.addWidget(facturas_widget)

        
    def show_context_menu(self, pos):
        context_menu = QMenu()
        copy_action = QAction("Copiar", self)
        copy_action.triggered.connect(self.copy_cell)
        context_menu.addAction(copy_action)
        context_menu.exec(self.user_table.viewport().mapToGlobal(pos))

    def copy_cell(self):
        selected_item = self.user_table.currentItem()
        if selected_item:
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_item.text())
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona una celda para copiar.")

    def load_clientes(self):
        # Conectar a la base de datos y cargar los clientes
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT [DNI/RUC], Nombre, ApellidoPaterno, ApellidoMaterno, Dirección, Teléfono, Correo, FechaRegistro
            FROM Clientes
            """
            cursor.execute(query)
            clientes = cursor.fetchall()
            self.user_table.setRowCount(0)  # Limpiar la tabla antes de añadir nuevos datos
            
            for cliente in clientes:
                row_position = self.user_table.rowCount()
                self.user_table.insertRow(row_position)
                for col, data in enumerate(cliente):
                    if col == 7 and isinstance(data, datetime):  # Formatear la fecha de registro si es un objeto datetime
                        data = format_date(data)
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
            OR [DNI/RUC] LIKE ?
            OR ApellidoPaterno LIKE ?
            OR ApellidoMaterno LIKE ?
            OR Dirección LIKE ?
            OR Teléfono LIKE ?
            OR Correo LIKE ?
            """
            search_pattern = f'%{search_text}%'
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
            clientes = cursor.fetchall()
            
            self.user_table.setRowCount(0)  # Limpiar la tabla antes de añadir nuevos datos
            for cliente in clientes:
                row_position = self.user_table.rowCount()
                self.user_table.insertRow(row_position)
                for col, data in enumerate(cliente):
                    if col == 6 and isinstance(data, datetime):  # Formatear la fecha de registro si es un objeto datetime
                        data = format_date(data)
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

        # Mostrar cuadro de diálogo de confirmación
        reply = QMessageBox.question(
            self, 
            "Confirmar eliminación", 
            f"¿Estás seguro de que deseas eliminar al usuario '{user_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Clientes WHERE Nombre = ?", user_name)
                connection.commit()
                connection.close()

                self.user_table.removeRow(selected_row)
                QMessageBox.information(self, "Éxito", "Usuario eliminado.")
        else:
            QMessageBox.information(self, "Cancelado", "El usuario no ha sido eliminado.")

    def edit_user(self):
        selected_row = self.user_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un usuario para editar.")
            return
        
        # Obtener los datos del usuario seleccionado
        user_data = {
            'dni_ruc': self.user_table.item(selected_row, 0).text(),
            'nombre': self.user_table.item(selected_row, 1).text(),
            'apellido_paterno': self.user_table.item(selected_row, 2).text(),
            'apellido_materno': self.user_table.item(selected_row, 3).text(),
            'direccion': self.user_table.item(selected_row, 4).text(),
            'telefono': self.user_table.item(selected_row, 5).text(),
            'correo': self.user_table.item(selected_row, 6).text()
        }

        dialog = EditUserDialog(user_data, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_user_data()

            # Validar DNI/RUC
            if not is_valid_dni(updated_data['dni_ruc']):
                QMessageBox.warning(self, "Advertencia", "El DNI/RUC debe contener solo números y un máximo de 20 caracteres.")
                return
            
            # Validar el teléfono y el correo
            if not is_valid_phone(updated_data['telefono']):
                QMessageBox.warning(self, "Advertencia", "El teléfono debe contener solo números.")
                return
            
            if not is_valid_email(updated_data['correo']):
                QMessageBox.warning(self, "Advertencia", "El correo debe tener la estructura '___@___.com'.")
                return

            try:
                connection = connect_to_db()
                if connection:
                    cursor = connection.cursor()
                    cursor.execute("""
                        UPDATE Clientes 
                        SET [DNI/RUC] = ?, Nombre = ?, ApellidoPaterno = ?, ApellidoMaterno = ?, Dirección = ?, Teléfono = ?, Correo = ?
                        WHERE [DNI/RUC] = ?
                    """, 
                    updated_data['dni_ruc'],
                    updated_data['nombre'],
                    updated_data['apellido_paterno'],
                    updated_data['apellido_materno'],
                    updated_data['direccion'],
                    updated_data['telefono'],
                    updated_data['correo'],
                    user_data['dni_ruc'])  # Usar el DNI/RUC antiguo para identificar el registro a actualizar

                    connection.commit()
                    connection.close()

                    # Actualizar los datos en la tabla
                    self.user_table.setItem(selected_row, 0, QTableWidgetItem(updated_data['dni_ruc']))
                    self.user_table.setItem(selected_row, 1, QTableWidgetItem(updated_data['nombre']))
                    self.user_table.setItem(selected_row, 2, QTableWidgetItem(updated_data['apellido_paterno']))
                    self.user_table.setItem(selected_row, 3, QTableWidgetItem(updated_data['apellido_materno']))
                    self.user_table.setItem(selected_row, 4, QTableWidgetItem(updated_data['direccion']))
                    self.user_table.setItem(selected_row, 5, QTableWidgetItem(updated_data['telefono']))
                    self.user_table.setItem(selected_row, 6, QTableWidgetItem(updated_data['correo']))

                    QMessageBox.information(self, "Éxito", "Usuario editado.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al editar el usuario: {e}")



    def create_user(self):
        dialog = UserDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_data = dialog.get_user_data()

            # Validar DNI/RUC
            if not is_valid_dni(user_data['dni_ruc']):
                QMessageBox.warning(self, "Advertencia", "El DNI/RUC debe contener solo números y un máximo de 20 caracteres.")
                return

            # Validar el teléfono y el correo
            if not is_valid_phone(user_data['telefono']):
                QMessageBox.warning(self, "Advertencia", "El teléfono debe contener solo números.")
                return
            
            if not is_valid_email(user_data['correo']):
                QMessageBox.warning(self, "Advertencia", "El correo debe tener la estructura '___@___.com'.")
                return

            try:
                connection = connect_to_db()
                if connection:
                    cursor = connection.cursor()
                    
                    # Insertar datos en la base de datos
                    cursor.execute(
                        "INSERT INTO Clientes ([DNI/RUC], Nombre, ApellidoPaterno, ApellidoMaterno, Dirección, Teléfono, Correo) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        user_data['dni_ruc'],
                        user_data['nombre'],
                        user_data['apellido_paterno'],
                        user_data['apellido_materno'],
                        user_data['direccion'],
                        user_data['telefono'],
                        user_data['correo']
                    )
                    connection.commit()
                    connection.close()

                    # Añadir el nuevo usuario a la tabla
                    row_position = self.user_table.rowCount()
                    self.user_table.insertRow(row_position)
                    self.user_table.setItem(row_position, 0, QTableWidgetItem(user_data['dni_ruc']))
                    self.user_table.setItem(row_position, 1, QTableWidgetItem(user_data['nombre']))
                    self.user_table.setItem(row_position, 2, QTableWidgetItem(user_data['apellido_paterno']))
                    self.user_table.setItem(row_position, 3, QTableWidgetItem(user_data['apellido_materno']))
                    self.user_table.setItem(row_position, 4, QTableWidgetItem(user_data['direccion']))
                    self.user_table.setItem(row_position, 5, QTableWidgetItem(user_data['telefono']))
                    self.user_table.setItem(row_position, 6, QTableWidgetItem(user_data['correo']))
                    
                    QMessageBox.information(self, "Éxito", "Usuario creado.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear el usuario: {e}")

    def search_client(self):
        search_text = self.client_search_input.text()
        if not search_text:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingresa un término de búsqueda.")
            return

        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT ClienteID, [DNI/RUC], Nombre
            FROM Clientes
            WHERE [DNI/RUC] LIKE ? OR Nombre LIKE ?
            """
            cursor.execute(query, f'%{search_text}%', f'%{search_text}%')
            clients = cursor.fetchall()
            
            # Implement a way to select a client from search results
            # For now, assuming we are just printing the results
            for client in clients:
                print(client)  # Replace this with a suitable way to select a client
            
            connection.close()

    def load_services(self):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = "SELECT ServiciosID, NombreServicio FROM Servicios" 
            cursor.execute(query)
            services = cursor.fetchall()
            self.service_combo.clear()  # Clear existing items
            self.service_combo.addItem("Seleccione un servicio")
            for service in services:
                self.service_combo.addItem(service[1], userData=service[0])
            connection.close()


    def add_service_to_invoice(self):
        service_id = self.service_combo.currentData()
        service_name = self.service_combo.currentText()
        quantity, ok = QInputDialog.getInt(self, "Cantidad", "Ingrese la cantidad:", 1, 1, 100, 1)
        if ok and service_id:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT Precio FROM Servicios WHERE ServicioID = ?", service_id)
                price = cursor.fetchone()[0]
                total = quantity * price
                row_position = self.services_table.rowCount()
                self.services_table.insertRow(row_position)
                self.services_table.setItem(row_position, 0, QTableWidgetItem(service_name))
                self.services_table.setItem(row_position, 1, QTableWidgetItem(str(quantity)))
                self.services_table.setItem(row_position, 2, QTableWidgetItem(f"{price:.2f}"))
                self.services_table.setItem(row_position, 3, QTableWidgetItem(f"{total:.2f}"))
                connection.close()


    def save_invoice(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor()
                client_id = 1  # Replace this with the actual client ID
                total_amount = sum(float(self.services_table.item(row, 3).text()) for row in range(self.services_table.rowCount()))
                cursor.execute("INSERT INTO Facturas (ClienteID, MontoTotal) VALUES (?, ?)", client_id, total_amount)
                factura_id = cursor.lastrowid
                
                for row in range(self.services_table.rowCount()):
                    service_name = self.services_table.item(row, 0).text()
                    quantity = int(self.services_table.item(row, 1).text())
                    price = float(self.services_table.item(row, 2).text())
                    # Retrieve the service ID based on the service name or another approach
                    cursor.execute("SELECT ServicioID FROM Servicios WHERE NombreServicio = ?", service_name)
                    service_id = cursor.fetchone()[0]
                    cursor.execute("INSERT INTO FacturaServicios (FacturaID, ServicioID, Cantidad, PrecioUnitario) VALUES (?, ?, ?, ?)",
                                factura_id, service_id, quantity, price)
                
                connection.commit()
                connection.close()
                QMessageBox.information(self, "Éxito", "Factura guardada.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar la factura: {e}")


    def handle_button_click(self):
        # Obtener el botón que fue clickeado
        sender = self.sender()

        if sender.text() == "Clientes":
            self.stacked_widget.setCurrentIndex(1) 
        elif sender.text() == "Facturas":
            self.stacked_widget.setCurrentIndex(2) 
            pass
        elif sender.text() == "Pagos":
            # Cambiar al índice correspondiente al layout de Pagos
            pass
        elif sender.text() == "Servicios":
            # Cambiar al índice correspondiente al layout de Servicios
            pass
        elif sender.text() == "Reportes":
            # Cambiar al índice correspondiente al layout de Reportes
            pass
        elif sender.text() == "Configuración y Seguridad":
            # Cambiar al índice correspondiente al layout de Configuración y Seguridad
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
