import sys, re
from PyQt6.QtWidgets import QApplication, QComboBox, QHeaderView, QLabel, QStyledItemDelegate, QInputDialog, QStackedWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QWidget, QMessageBox, QDialog, QAbstractItemView, QMenu
from PyQt6.QtGui import QIcon, QAction, QClipboard
from PyQt6.QtCore import Qt
from datetime import datetime
from dialogs import *
from reportes import *
from utils import *
from conn import connect_to_db
from functools import partial

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Factura lavandería")
        self.setFixedSize(1200, 800)  # Fija el tamaño de la ventana

        # Obtener el tamaño de la pantalla
        screen_geometry = QApplication.primaryScreen().availableGeometry()

        # Calcular la posición centrada
        x = (screen_geometry.width() - 1200) // 2
        y = (screen_geometry.height() - 800) // 2

        # Ajustar la posición de la ventana
        self.move(x, y)

        # Crear un QStackedWidget para gestionar múltiples layouts
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Crear layouts
        self.create_main_layout()
        self.create_clientes_layout()
        self.create_facturas_layout()
        self.create_pagos_layout()
        self.create_servicios_layout()
        self.create_reportes_layout()

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

    #=========================================================================CLIENTES=========================================================================
    def create_clientes_layout(self):
        # Crear el layout de clientes
        clientes_layout = QVBoxLayout()

        # Crear el buscador y los botones de búsqueda, refrescar y regresar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar usuario...")
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.search_users)
        
        # Botón refrescar
        refresh_button = QPushButton("Refrescar")
        refresh_button.clicked.connect(self.refresh_clientes)  # Conectar al método para refrescar

        # Botón regresar
        regresar_button = QPushButton("Regresar")
        regresar_button.clicked.connect(self.regresar)  # Conectar al método de regresar
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(refresh_button)  # Agregar el botón "Refrescar"
        search_layout.addWidget(regresar_button)  # Agregar el botón "Regresar"
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

        # Botón eliminar usuario
        actions_layout = QHBoxLayout()
        delete_button = QPushButton(QIcon("img/delete_icon.png"), "Eliminar")  
        delete_button.setStyleSheet("font-size: 16px; height: 50px;")
        delete_button.clicked.connect(self.delete_user)
        actions_layout.addWidget(delete_button)

        # Botón editar usuario
        edit_button = QPushButton(QIcon("img/edit_icon.png"), "Editar")  
        edit_button.setStyleSheet("font-size: 16px; height: 50px;")
        edit_button.clicked.connect(self.edit_user)
        actions_layout.addWidget(edit_button)

        # Botón crear nuevo usuario
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

    def refresh_clientes(self):
        # Método para refrescar la lista de clientes
        self.load_clientes()


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
        
        # Mostrar el diálogo hasta que el usuario lo cierre con éxito o cancele
        while True:
            if dialog.exec() == QDialog.DialogCode.Accepted:
                user_data = dialog.get_user_data()

                # Validar DNI/RUC
                if not is_valid_dni(user_data['dni_ruc']):
                    QMessageBox.warning(self, "Advertencia", "El DNI/RUC debe contener solo números y un máximo de 20 caracteres.")
                    continue  # Volver a mostrar el diálogo para corrección
                
                # Validar el teléfono y el correo
                if not is_valid_phone(user_data['telefono']):
                    QMessageBox.warning(self, "Advertencia", "El teléfono debe contener solo números.")
                    continue  # Volver a mostrar el diálogo para corrección
                
                if not is_valid_email(user_data['correo']):
                    QMessageBox.warning(self, "Advertencia", "El correo debe tener la estructura '***@***.com'.")
                    continue  # Volver a mostrar el diálogo para corrección

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
                        break  # Salir del bucle si todo ha sido exitoso

                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al crear el usuario: {e}")
                    break  # Salir del bucle en caso de error

    #=========================================================================FACTURAS=========================================================================
    def create_facturas_layout(self):
        # Crear el layout para la factura
        facturas_layout = QVBoxLayout()

        # Crear el buscador de clientes
        search_layout = QHBoxLayout()
        self.dni_ruc_display = QLineEdit()
        self.dni_ruc_display.setPlaceholderText("DNI/RUC")
        self.dni_ruc_display.setReadOnly(True)  # No editable

        self.nombre_display = QLineEdit()
        self.nombre_display.setPlaceholderText("Nombre completo")
        self.nombre_display.setReadOnly(True)  # No editable

        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.open_search_dialog)

        regresar_button = QPushButton("Regresar")
        regresar_button.clicked.connect(self.regresar)
        
        search_layout.addWidget(self.dni_ruc_display)
        search_layout.addWidget(self.nombre_display)
        search_layout.addWidget(search_button)
        search_layout.addWidget(regresar_button)  # Añadir el botón regresar a la derecha
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

        # Configurar el ajuste de columnas
        header = self.services_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Servicio
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Cantidad
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Precio Unitario
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Total

        # Hacer solo la columna de cantidad editable
        self.services_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # No editable por defecto
        self.services_table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.services_table.setItemDelegateForColumn(1, QStyledItemDelegate())  # Editable solo en la columna de cantidad

        self.services_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.services_table.itemChanged.connect(self.recalculate_total)
        facturas_layout.addWidget(self.services_table)

        # Botón para eliminar servicio
        remove_service_button = QPushButton("Eliminar Servicio")
        remove_service_button.clicked.connect(self.remove_selected_service)
        facturas_layout.addWidget(remove_service_button)

        # Botón para guardar factura
        save_invoice_button = QPushButton("Guardar Factura")
        save_invoice_button.clicked.connect(self.save_invoice)
        facturas_layout.addWidget(save_invoice_button)

        # Crear un widget para el layout de facturas
        facturas_widget = QWidget()
        facturas_widget.setLayout(facturas_layout)
        self.stacked_widget.addWidget(facturas_widget)

    def regresar(self):
        # Función que maneja el botón regresar
        self.stacked_widget.setCurrentIndex(0)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_table_column_widths()

    def adjust_table_column_widths(self):
        total_width = self.services_table.width()
        service_col_width = int(0.5 * total_width)  # 50% for the service column
        other_col_width = int((total_width - service_col_width) / 3)  # Distribute the remaining width

        self.services_table.setColumnWidth(0, service_col_width)
        self.services_table.setColumnWidth(1, other_col_width)
        self.services_table.setColumnWidth(2, other_col_width)
        self.services_table.setColumnWidth(3, other_col_width)

    def open_search_dialog(self):
        search_dialog = SearchClientDialog(self.dni_ruc_display, self.nombre_display, self)
        search_dialog.exec()

    
    def open_search_dialog(self):
        dialog = SearchClientDialog(self)
        dialog.client_selected.connect(self.update_client_display)
        dialog.exec()

    def update_client_display(self, dni_ruc, nombre_completo):
        self.dni_ruc_display.setText(dni_ruc)
        self.nombre_display.setText(nombre_completo)

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
        selected_service_id = self.service_combo.currentData()  # Get the selected service ID
        selected_service_name = self.service_combo.currentText()  # Get the selected service name

        # Verifica si se ha seleccionado un servicio
        if selected_service_id is None:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un servicio.")
            return

        unit_price = self.get_service_price(selected_service_id)  # Get service unit price

        if unit_price is not None:
            row_position = self.services_table.rowCount()
            self.services_table.insertRow(row_position)

            # Add service name
            self.services_table.setItem(row_position, 0, QTableWidgetItem(selected_service_name))

            # Add default quantity
            quantity_item = QTableWidgetItem("1")
            quantity_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.services_table.setItem(row_position, 1, quantity_item)

            # Add unit price
            unit_price_item = QTableWidgetItem(f"{unit_price:.2f}")
            unit_price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.services_table.setItem(row_position, 2, unit_price_item)

            # Add total
            total_item = QTableWidgetItem(f"{unit_price:.2f}")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.services_table.setItem(row_position, 3, total_item)

            # Disconnect existing signals to avoid multiple connections
            self.services_table.itemChanged.disconnect(self.recalculate_total)

            # Connect itemChanged signal to recalculate total
            self.services_table.itemChanged.connect(self.recalculate_total)



    def get_service_price(self, service_id):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = "SELECT Precio FROM Servicios WHERE ServiciosID = ?"
            cursor.execute(query, (service_id,))
            price = cursor.fetchone()[0]
            connection.close()
            return price
        return 0

    def recalculate_total(self, item):
        if item.column() == 1:  # Solo recalcular si la columna editada es la de cantidad
            row = item.row()
            quantity_item = self.services_table.item(row, 1)
            unit_price_item = self.services_table.item(row, 2)
            
            try:
                quantity = float(quantity_item.text())
                unit_price = float(unit_price_item.text())
                total = quantity * unit_price
                total_item = self.services_table.item(row, 3)
                total_item.setText(f"{total:.2f}")
            except (ValueError, AttributeError):
                # Handle cases where conversion fails or item is None
                pass



    def remove_selected_service(self):
        selected_row = self.services_table.currentRow()
        if selected_row >= 0:
            self.services_table.removeRow(selected_row)


    def save_invoice(self):
        # Obtener el DNI/RUC del cliente
        dni_ruc = self.dni_ruc_display.text()
        
        # Obtener el ClienteID basado en el DNI/RUC
        cliente_id = self.get_client_id_by_dni_ruc(dni_ruc)
        if cliente_id is None:
            QMessageBox.warning(self, "Error", "Cliente no encontrado")
            return

        # Construir la descripción de la factura
        descripcion = []
        total_amount = 0.0
        for row in range(self.services_table.rowCount()):
            service_name_item = self.services_table.item(row, 0)
            quantity_item = self.services_table.item(row, 1)
            total_item = self.services_table.item(row, 3)

            if service_name_item and quantity_item and total_item:
                service_name = service_name_item.text()
                quantity = quantity_item.text()
                total = total_item.text()

                # Obtener el ID del servicio basándose en el nombre
                service_id = self.get_service_id_by_name(service_name)
                if service_id is not None:
                    descripcion.append(f"{service_id}-{quantity}")
                    total_amount += float(total)

        descripcion_str = ",".join(descripcion)

        # Insertar la nueva factura en la base de datos
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO Facturas (ClienteID, Descripcion, MontoTotal, Estado)
            VALUES (?, ?, ?, ?)
            """
            estado = "Pendiente"  # O el estado que corresponda
            cursor.execute(query, (cliente_id, descripcion_str, total_amount, estado))
            connection.commit()
            connection.close()

            QMessageBox.information(self, "Éxito", "Factura guardada con éxito")
            self.reset_invoice_form()  # Opcional: restablecer el formulario de la factura

    def get_service_id_by_name(self, service_name):
        """
        Obtiene el ID del servicio basado en su nombre.
        """
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = "SELECT ServiciosID FROM Servicios WHERE NombreServicio = ?"
            cursor.execute(query, (service_name,))
            result = cursor.fetchone()
            connection.close()
            if result:
                return result[0]
        return None


    def get_client_id_by_dni_ruc(self, dni_ruc):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            # Usar comillas dobles para nombres de columna con caracteres especiales
            query = 'SELECT ClienteID FROM Clientes WHERE "DNI/RUC" = ?'
            cursor.execute(query, (dni_ruc,))
            result = cursor.fetchone()
            connection.close()
            if result:
                return result[0]
        return None

    def reset_invoice_form(self):
        # Limpiar el formulario de la factura
        self.dni_ruc_display.clear()
        self.nombre_display.clear()
        self.services_table.setRowCount(0)


    #=========================================================================PAGOS=========================================================================
    def create_pagos_layout(self):
        # Crear el layout principal para pagos
        pagos_layout = QVBoxLayout()

        # Crear el layout para el campo de búsqueda
        search_layout = QHBoxLayout()
        
        # Campo de búsqueda para FacturaID
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por FacturaID")
        
        # Botón de búsqueda
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.search_factura)
        
        # Botón de regresar
        regresar_button = QPushButton("Regresar")
        regresar_button.clicked.connect(self.regresar)
        
        search_layout.addWidget(QLabel("Buscar:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(regresar_button)  # Añadir el botón regresar a la derecha
        
        pagos_layout.addLayout(search_layout)

        # Crear la tabla para mostrar las facturas
        self.pagos_table = QTableWidget()
        self.pagos_table.setColumnCount(5)
        self.pagos_table.setHorizontalHeaderLabels(["FacturaID", "DNI/RUC", "Monto Total", "Fecha", "Estado"])
        
        # Configurar la tabla
        header = self.pagos_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Ajustar columnas al ancho
        self.pagos_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        pagos_layout.addWidget(self.pagos_table)

        # Botón para ver detalles de la factura seleccionada
        detalles_button = QPushButton("Detalles")
        detalles_button.clicked.connect(self.show_factura_details)
        pagos_layout.addWidget(detalles_button)

        # Crear un widget para el layout de pagos
        pagos_widget = QWidget()
        pagos_widget.setLayout(pagos_layout)
        self.stacked_widget.addWidget(pagos_widget)

        # Cargar todas las facturas al inicializar el layout
        self.load_all_facturas()

    def load_all_facturas(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor()
                query = """
                SELECT f.FacturasID, c.[DNI/RUC], f.MontoTotal, f.FechaFactura, f.Estado
                FROM Facturas f
                JOIN Clientes c ON f.ClienteID = c.ClienteID
                """
                cursor.execute(query)
                results = cursor.fetchall()
                self.update_pagos_table(results)
                connection.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar facturas: {str(e)}")

    def search_factura(self):
        factura_id = self.search_input.text()
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT f.FacturasID, c.[DNI/RUC], f.MontoTotal, f.FechaFactura, f.Estado
            FROM Facturas f
            JOIN Clientes c ON f.ClienteID = c.ClienteID
            WHERE f.FacturasID = ?
            """
            cursor.execute(query, (factura_id,))
            results = cursor.fetchall()
            self.update_pagos_table(results)
            connection.close()
        
    def show_factura_details(self):
        selected_row = self.pagos_table.currentRow()
        if selected_row >= 0:
            factura_id_item = self.pagos_table.item(selected_row, 0)
            dni_ruc_item = self.pagos_table.item(selected_row, 1)
            
            if factura_id_item and dni_ruc_item:
                factura_id = factura_id_item.text()
                dni_ruc = dni_ruc_item.text()

                # Crear y mostrar el diálogo con los detalles
                dialog = FacturaDetailsDialog(factura_id, dni_ruc, self)
                dialog.exec()
            else:
                QMessageBox.warning(self, "Error", "No se encontraron detalles para la factura seleccionada.")
        self.load_all_facturas()

    def update_pagos_table(self, results):
        # Limpiar la tabla antes de añadir nuevos datos
        self.pagos_table.setRowCount(0)

        # Agregar los datos a la tabla
        for row_num, row_data in enumerate(results):
            self.pagos_table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.pagos_table.setItem(row_num, col_num, QTableWidgetItem(str(data)))



    #=========================================================================SERVICIOS=========================================================================
    def create_servicios_layout(self):
        # Crear el layout principal para servicios
        servicios_layout = QVBoxLayout()

        # Crear el layout para el campo de búsqueda
        search_layout = QHBoxLayout()
        
        # Campo de búsqueda para servicios
        self.search_service_input = QLineEdit()
        self.search_service_input.setPlaceholderText("Buscar servicios")
        
        # Botón de búsqueda
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.search_services)
        
        # Botón de regresar
        regresar_button = QPushButton("Regresar")
        regresar_button.clicked.connect(self.regresar)
        
        search_layout.addWidget(QLabel("Buscar:"))
        search_layout.addWidget(self.search_service_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(regresar_button)  # Añadir el botón regresar a la derecha
        
        servicios_layout.addLayout(search_layout)

        # Crear la tabla para mostrar los servicios
        self.servicios_table = QTableWidget()
        self.servicios_table.setColumnCount(4)
        self.servicios_table.setHorizontalHeaderLabels(["Código", "Nombre del Servicio", "Descripción", "Precio"])
        
        # Configurar la tabla
        header = self.servicios_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Ajustar columnas al ancho
        self.servicios_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        servicios_layout.addWidget(self.servicios_table)

        # Crear el layout para los botones de eliminar y agregar
        button_layout = QHBoxLayout()
        
        # Botón para eliminar servicio
        eliminar_button = QPushButton("Eliminar")
        eliminar_button.clicked.connect(self.delete_service)
        button_layout.addWidget(eliminar_button)
        
        # Botón para agregar servicio
        agregar_button = QPushButton("Agregar")
        agregar_button.clicked.connect(self.add_service)
        button_layout.addWidget(agregar_button)
        
        servicios_layout.addLayout(button_layout)

        # Crear un widget para el layout de servicios
        servicios_widget = QWidget()
        servicios_widget.setLayout(servicios_layout)
        self.stacked_widget.addWidget(servicios_widget)

        # Cargar todos los servicios al inicializar el layout
        self.load_all_services()

    def search_services(self):
        # Implementar la lógica de búsqueda de servicios
        search_text = self.search_service_input.text()
        # Aquí puedes agregar la lógica para filtrar los servicios según el texto de búsqueda
        # y actualizar la tabla con los resultados

    def delete_service(self):
        # Implementar la lógica para eliminar el servicio seleccionado
        selected_row = self.servicios_table.currentRow()
        if selected_row >= 0:
            service_id = self.servicios_table.item(selected_row, 0).text()
            # Lógica para eliminar el servicio con el ID `service_id` de la base de datos
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor()
                query = "DELETE FROM Servicios WHERE ServiciosID = ?"
                cursor.execute(query, (service_id,))
                connection.commit()
                connection.close()
                self.load_all_services()  # Recargar la lista de servicios después de eliminar
            else:
                QMessageBox.warning(self, "Error", "No se pudo conectar a la base de datos")
        else:
            QMessageBox.warning(self, "Advertencia", "Selecciona un servicio para eliminar")

    def add_service(self):
        dialog = AddServiceDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_all_services()  # Recargar la lista de servicios después de agregar uno nuevo

    def load_all_services(self):
        # Implementar la lógica para cargar todos los servicios en la tabla
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT ServiciosID, NombreServicio, Descripcion, Precio
            FROM Servicios
            """
            cursor.execute(query)
            services = cursor.fetchall()
            
            # Limpiar la tabla antes de agregar datos
            self.servicios_table.setRowCount(0)
            
            for service in services:
                row_position = self.servicios_table.rowCount()
                self.servicios_table.insertRow(row_position)
                self.servicios_table.setItem(row_position, 0, QTableWidgetItem(str(service[0])))
                self.servicios_table.setItem(row_position, 1, QTableWidgetItem(service[1]))
                self.servicios_table.setItem(row_position, 2, QTableWidgetItem(service[2]))
                self.servicios_table.setItem(row_position, 3, QTableWidgetItem(f"{service[3]:.2f}"))
            
            connection.close()

    #=========================================================================SERVICIOS=========================================================================

    def create_reportes_layout(self):
        # Crear el layout principal para reportes
        reportes_layout = QVBoxLayout()
        
        # Centrar los botones verticalmente
        reportes_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Crear un estilo general para los botones
        button_style = """
            QPushButton {
                height: 50px;        /* Altura de los botones */
                width: 350px;        /* Ancho de los botones */
                font-size: 16px;     /* Tamaño de letra */
                padding: 10px;       /* Espaciado interno */
            }
        """

        # Crear botones para cada reporte
        reporte_cliente_button = QPushButton("Reporte por Cliente")
        reporte_cliente_button.setStyleSheet(button_style)
        reporte_cliente_button.clicked.connect(self.show_reporte_cliente)
        
        reporte_servicios_button = QPushButton("Reporte de Servicios más Solicitados")
        reporte_servicios_button.setStyleSheet(button_style)
        reporte_servicios_button.clicked.connect(self.show_reporte_servicios)
        
        reporte_pendientes_button = QPushButton("Reporte de Facturas Pendientes de Pago")
        reporte_pendientes_button.setStyleSheet(button_style)
        reporte_pendientes_button.clicked.connect(self.show_reporte_pendientes)
        
        reporte_facturacion_button = QPushButton("Reporte de Facturación por Periodo")
        reporte_facturacion_button.setStyleSheet(button_style)
        reporte_facturacion_button.clicked.connect(self.show_reporte_facturacion_periodo)
        
        reporte_clientes_frecuentes_button = QPushButton("Reporte de Clientes Frecuentes")
        reporte_clientes_frecuentes_button.setStyleSheet(button_style)
        reporte_clientes_frecuentes_button.clicked.connect(self.show_reporte_clientes_frecuentes)
        
        regresar_button = QPushButton("Regresar")
        regresar_button.setStyleSheet(button_style)
        regresar_button.clicked.connect(self.regresar)

        # Añadir los botones al layout
        reportes_layout.addWidget(reporte_cliente_button)
        reportes_layout.addWidget(reporte_servicios_button)
        reportes_layout.addWidget(reporte_pendientes_button)
        reportes_layout.addWidget(reporte_facturacion_button)
        reportes_layout.addWidget(reporte_clientes_frecuentes_button)
        reportes_layout.addWidget(regresar_button)

        # Añadir un espacio vertical entre los botones
        reportes_layout.setSpacing(20)

        # Crear un widget para el layout de reportes
        reportes_widget = QWidget()
        reportes_widget.setLayout(reportes_layout)

        # Añadir el widget de reportes al stacked_widget
        self.stacked_widget.addWidget(reportes_widget)


    def show_reporte_cliente(self):
        # Abrir el diálogo de reporte por cliente
        dialog = ReporteFacturasPorClienteDialog(self)
        dialog.exec()

    def show_reporte_servicios(self):
        # Crear una instancia del diálogo de reporte de servicios más solicitados
        dialog = ReporteServiciosMasSolicitadosDialog(self)
        
        # Mostrar el diálogo
        dialog.exec()

    def show_reporte_pendientes(self):
        # Mostrar reporte de facturas pendientes de pago
        pass

    def show_reporte_facturacion_periodo(self):
        # Mostrar reporte de facturación por periodo (mensual/anual)
        pass

    def show_reporte_clientes_frecuentes(self):
        # Mostrar reporte de clientes frecuentes
        pass

    def regresar(self):
        # Lógica para regresar a la pantalla anterior
        self.stacked_widget.setCurrentIndex(self.previous_index)  # Ejemplo




    #regresar al layout principal
    def regresar(self):
        # Función que maneja el botón regresar
        self.stacked_widget.setCurrentIndex(0)


    def handle_button_click(self):
        # Obtener el botón que fue clickeado
        sender = self.sender()

        if sender.text() == "Clientes":
            self.stacked_widget.setCurrentIndex(1) 
        elif sender.text() == "Facturas":
            self.stacked_widget.setCurrentIndex(2)
        elif sender.text() == "Pagos":
            self.stacked_widget.setCurrentIndex(3)
        elif sender.text() == "Servicios":
            self.stacked_widget.setCurrentIndex(4)
        elif sender.text() == "Reportes":
            self.stacked_widget.setCurrentIndex(5)
        elif sender.text() == "Configuración y Seguridad":
            # Cambiar al índice correspondiente al layout de Configuración y Seguridad
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
