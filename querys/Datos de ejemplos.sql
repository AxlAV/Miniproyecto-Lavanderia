USE [LavanderiaDB]
GO

INSERT INTO [dbo].[Servicios]
           ([NombreServicio]
           ,[Descripción]
           ,[Precio])
     VALUES
           ('Lavado y Planchado de Camisas', 'Lavado y planchado de camisas de algodón o mezcla.', 15.00),
           ('Lavado de Ropa de Cama', 'Lavado y planchado de sábanas, fundas de almohada y cobertores.', 25.00),
           ('Lavado de Trajes', 'Lavado en seco de trajes completos, incluyendo chaqueta y pantalones.', 40.00),
           ('Limpieza en Seco de Abrigos', 'Limpieza en seco de abrigos y chaquetas de lana o sintéticas.', 35.00),
           ('Lavado de Prendas Delicadas', 'Lavado y cuidado especial para prendas delicadas como seda o lana.', 20.00),
           ('Servicio de Planchado', 'Planchado de ropa variada, excluyendo lavado.', 10.00),
           ('Limpieza de Alfombras', 'Limpieza profunda de alfombras y tapetes.', 60.00),
           ('Servicio de Recogida y Entrega', 'Recogida y entrega de ropa a domicilio dentro de un radio de 10 km.', 5.00)
GO


INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Dirección], [Teléfono], [Correo])
VALUES ('12345678', 'Juan', 'Pérez', 'García', 'Av. Siempre Viva 123', '987654321', 'juan.perez@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Dirección], [Teléfono], [Correo])
VALUES ('87654321', 'María', 'Rodríguez', 'López', 'Calle Falsa 456', '912345678', 'maria.rodriguez@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Dirección], [Teléfono], [Correo])
VALUES ('11223344', 'Carlos', 'Sánchez', 'Mendoza', 'Jirón de la Unión 789', '923456789', 'carlos.sanchez@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Dirección], [Teléfono], [Correo])
VALUES ('55667788', 'Ana', 'González', 'Torres', 'Pasaje Los Olivos 101', '934567890', 'ana.gonzalez@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Dirección], [Teléfono], [Correo])
VALUES ('99887766', 'Pedro', 'Martínez', 'Ramírez', 'Av. Las Flores 202', '945678901', 'pedro.martinez@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Dirección], [Teléfono], [Correo])
VALUES ('22334455', 'Luisa', 'Fernández', 'Díaz', 'Calle Los Cedros 303', '956789012', 'luisa.fernandez@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Dirección], [Teléfono], [Correo])
VALUES ('77889900', 'Miguel', 'Ramírez', 'Ortiz', 'Av. Principal 404', '967890123', 'miguel.ramirez@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Dirección], [Teléfono], [Correo])
VALUES ('33445566', 'Sofía', 'Vega', 'Rojas', 'Jirón Las Amapolas 505', '978901234', 'sofia.vega@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Dirección], [Teléfono], [Correo])
VALUES ('66778899', 'Raúl', 'Flores', 'Silva', 'Calle Las Rosas 606', '989012345', 'raul.flores@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Dirección], [Teléfono], [Correo])
VALUES ('44556677', 'Elena', 'Chávez', 'Muñoz', 'Pasaje Las Palmeras 707', '990123456', 'elena.chavez@example.com');
