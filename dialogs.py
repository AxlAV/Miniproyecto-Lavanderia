from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QLabel

class EditUserDialog(QDialog):
    def __init__(self, user_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Usuario")
        self.setFixedSize(400, 300)

        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.dni_ruc_input = QLineEdit(self.user_data['dni_ruc'])  # Añadir campo DNI/RUC
        self.name_input = QLineEdit(self.user_data['nombre'])
        self.paterno_input = QLineEdit(self.user_data['apellido_paterno'])
        self.materno_input = QLineEdit(self.user_data['apellido_materno'])
        self.address_input = QLineEdit(self.user_data['direccion'])
        self.phone_input = QLineEdit(self.user_data['telefono'])
        self.email_input = QLineEdit(self.user_data['correo'])

        layout.addRow("DNI/RUC:", self.dni_ruc_input)  # Añadir a la interfaz
        layout.addRow("Nombre:", self.name_input)
        layout.addRow("Apellido Paterno:", self.paterno_input)
        layout.addRow("Apellido Materno:", self.materno_input)
        layout.addRow("Dirección:", self.address_input)
        layout.addRow("Teléfono:", self.phone_input)
        layout.addRow("Correo:", self.email_input)

        button_box = QVBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)
        
        layout.addRow("", button_box)

        self.setLayout(layout)

    def get_user_data(self):
        return {
            'dni_ruc': self.dni_ruc_input.text(),  # Añadir al método get_user_data
            'nombre': self.name_input.text(),
            'apellido_paterno': self.paterno_input.text(),
            'apellido_materno': self.materno_input.text(),
            'direccion': self.address_input.text(),
            'telefono': self.phone_input.text(),
            'correo': self.email_input.text()
        }

class UserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nuevo Usuario")
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.dni_ruc_input = QLineEdit()  # Añadir campo DNI/RUC
        self.name_input = QLineEdit()
        self.paterno_input = QLineEdit()
        self.materno_input = QLineEdit()
        self.address_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        layout.addRow("DNI/RUC:", self.dni_ruc_input)  # Añadir a la interfaz
        layout.addRow("Nombre:", self.name_input)
        layout.addRow("Apellido Paterno:", self.paterno_input)
        layout.addRow("Apellido Materno:", self.materno_input)
        layout.addRow("Dirección:", self.address_input)
        layout.addRow("Teléfono:", self.phone_input)
        layout.addRow("Correo:", self.email_input)

        button_box = QVBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)
        
        layout.addRow("", button_box)

        self.setLayout(layout)

    def get_user_data(self):
        return {
            'dni_ruc': self.dni_ruc_input.text(),  # Añadir al método get_user_data
            'nombre': self.name_input.text(),
            'apellido_paterno': self.paterno_input.text(),
            'apellido_materno': self.materno_input.text(),
            'direccion': self.address_input.text(),
            'telefono': self.phone_input.text(),
            'correo': self.email_input.text()
        }
