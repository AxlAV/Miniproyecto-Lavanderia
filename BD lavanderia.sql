ALTER DATABASE LavanderiaDB
SET SINGLE_USER
WITH ROLLBACK IMMEDIATE;


-- Cambiar a la base de datos master
USE master;

-- Eliminar la base de datos LavanderiaDB
DROP DATABASE LavanderiaDB;

CREATE DATABASE LavanderiaDB;
GO
USE LavanderiaDB;
GO


CREATE TABLE Clientes (
    ClienteID INT PRIMARY KEY IDENTITY(1,1),
    [DNI/RUC] VARCHAR(20) NOT NULL,
    Nombre VARCHAR(100) NOT NULL,
    ApellidoPaterno VARCHAR(100),
    ApellidoMaterno VARCHAR(100),
    Direcci�n VARCHAR(255),
    Tel�fono VARCHAR(15),
    Correo VARCHAR(100),
    FechaRegistro DATETIME DEFAULT GETDATE()
);


CREATE TABLE Facturas (
    FacturasID INT PRIMARY KEY IDENTITY(1,1),
    ClienteID INT FOREIGN KEY REFERENCES Clientes(ClienteID),
    FechaFactura DATETIME DEFAULT GETDATE(),
    MontoTotal DECIMAL(18,2),
    Estado VARCHAR(50)
);

CREATE TABLE Pagos (
    PagosID INT PRIMARY KEY IDENTITY(1,1),
    FacturasID INT FOREIGN KEY REFERENCES Facturas(FacturasID),
    FechaPago DATETIME DEFAULT GETDATE(),
    MontoPago DECIMAL(18,2),
    M�todoPago VARCHAR(50)
);

CREATE TABLE Servicios (
    ServiciosID INT PRIMARY KEY IDENTITY(1,1),
    NombreServicio VARCHAR(100) NOT NULL,
    Descripci�n TEXT,
    Precio DECIMAL(18,2)
);

CREATE TABLE DetalleFacturas (
    DetalleFacturasID INT PRIMARY KEY IDENTITY(1,1),
    FacturasID INT FOREIGN KEY REFERENCES Facturas(FacturasID),
    ServiciosID INT FOREIGN KEY REFERENCES Servicios(ServiciosID),
    Cantidad INT NOT NULL,
    PrecioUnitario DECIMAL(18,2),
    Total AS (Cantidad * PrecioUnitario)
);

