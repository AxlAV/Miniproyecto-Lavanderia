-- Eliminar la base de datos si ya existe
ALTER DATABASE LavanderiaDB
SET SINGLE_USER
WITH ROLLBACK IMMEDIATE;

USE master;
DROP DATABASE IF EXISTS LavanderiaDB;
GO

-- Crear la base de datos
CREATE DATABASE LavanderiaDB;
GO

USE LavanderiaDB;
GO

-- Crear la tabla Clientes
CREATE TABLE Clientes (
    ClienteID INT PRIMARY KEY IDENTITY(1,1),
    [DNI/RUC] VARCHAR(20) NOT NULL,
    Nombre VARCHAR(100) NOT NULL,
    ApellidoPaterno VARCHAR(100),
    ApellidoMaterno VARCHAR(100),
    Dirección VARCHAR(255),
    Teléfono VARCHAR(15),
    Correo VARCHAR(100),
    FechaRegistro DATETIME DEFAULT GETDATE()
);
GO

-- Crear la tabla Facturas
CREATE TABLE Facturas (
    FacturasID INT PRIMARY KEY IDENTITY(1,1),
    ClienteID INT,
    FechaFactura DATETIME DEFAULT GETDATE(),
    MontoTotal DECIMAL(18,2),
    Estado VARCHAR(50),
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID)
);
GO

-- Crear la tabla Pagos
CREATE TABLE Pagos (
    PagosID INT PRIMARY KEY IDENTITY(1,1),
    FacturasID INT,
    FechaPago DATETIME DEFAULT GETDATE(),
    MontoPago DECIMAL(18,2),
    MétodoPago VARCHAR(50),
    FOREIGN KEY (FacturasID) REFERENCES Facturas(FacturasID)
);
GO

-- Crear la tabla Servicios
CREATE TABLE Servicios (
    ServiciosID INT PRIMARY KEY IDENTITY(1,1),
    NombreServicio VARCHAR(100) NOT NULL,
    Descripción TEXT,
    Precio DECIMAL(18,2)
);
GO

-- Crear la tabla DetalleFacturas
CREATE TABLE DetalleFacturas (
    DetalleFacturasID INT PRIMARY KEY IDENTITY(1,1),
    FacturasID INT,
    ServiciosID INT,
    Cantidad INT NOT NULL,
    PrecioUnitario DECIMAL(18,2),
    Total AS (Cantidad * PrecioUnitario),
    FOREIGN KEY (FacturasID) REFERENCES Facturas(FacturasID),
    FOREIGN KEY (ServiciosID) REFERENCES Servicios(ServiciosID)
);
GO
