from datetime import datetime
import re

def format_date(date_obj):
    """
    Formatea un objeto datetime en una cadena de texto.
    """
    if isinstance(date_obj, datetime):
        return date_obj.strftime("%d-%m-%Y %H:%M:%S")
    return date_obj

def is_valid_phone(phone):
    return phone.isdigit()  # Verifica que el teléfono contenga solo números

def is_valid_email(email):
    # Verifica que el correo tenga la estructura "___@___.com"
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,3}$'
    return re.match(email_pattern, email) is not None

def is_valid_dni(dni_ruc):
    return dni_ruc.isdigit() and len(dni_ruc) <= 20

