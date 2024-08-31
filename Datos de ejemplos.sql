USE [LavanderiaDB]
GO

INSERT INTO [dbo].[Servicios]
           ([NombreServicio]
           ,[Descripci�n]
           ,[Precio])
     VALUES
           ('Lavado y Planchado de Camisas', 'Lavado y planchado de camisas de algod�n o mezcla.', 15.00),
           ('Lavado de Ropa de Cama', 'Lavado y planchado de s�banas, fundas de almohada y cobertores.', 25.00),
           ('Lavado de Trajes', 'Lavado en seco de trajes completos, incluyendo chaqueta y pantalones.', 40.00),
           ('Limpieza en Seco de Abrigos', 'Limpieza en seco de abrigos y chaquetas de lana o sint�ticas.', 35.00),
           ('Lavado de Prendas Delicadas', 'Lavado y cuidado especial para prendas delicadas como seda o lana.', 20.00),
           ('Servicio de Planchado', 'Planchado de ropa variada, excluyendo lavado.', 10.00),
           ('Limpieza de Alfombras', 'Limpieza profunda de alfombras y tapetes.', 60.00),
           ('Servicio de Recogida y Entrega', 'Recogida y entrega de ropa a domicilio dentro de un radio de 10 km.', 5.00)
GO


INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Direcci�n], [Tel�fono], [Correo])
VALUES ('12345678', 'Juan', 'P�rez', 'Garc�a', 'Av. Siempre Viva 123', '987654321', 'juan.perez@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Direcci�n], [Tel�fono], [Correo])
VALUES ('87654321', 'Mar�a', 'Rodr�guez', 'L�pez', 'Calle Falsa 456', '912345678', 'maria.rodriguez@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Direcci�n], [Tel�fono], [Correo])
VALUES ('11223344', 'Carlos', 'S�nchez', 'Mendoza', 'Jir�n de la Uni�n 789', '923456789', 'carlos.sanchez@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Direcci�n], [Tel�fono], [Correo])
VALUES ('55667788', 'Ana', 'Gonz�lez', 'Torres', 'Pasaje Los Olivos 101', '934567890', 'ana.gonzalez@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Direcci�n], [Tel�fono], [Correo])
VALUES ('99887766', 'Pedro', 'Mart�nez', 'Ram�rez', 'Av. Las Flores 202', '945678901', 'pedro.martinez@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Direcci�n], [Tel�fono], [Correo])
VALUES ('22334455', 'Luisa', 'Fern�ndez', 'D�az', 'Calle Los Cedros 303', '956789012', 'luisa.fernandez@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Direcci�n], [Tel�fono], [Correo])
VALUES ('77889900', 'Miguel', 'Ram�rez', 'Ortiz', 'Av. Principal 404', '967890123', 'miguel.ramirez@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Direcci�n], [Tel�fono], [Correo])
VALUES ('33445566', 'Sof�a', 'Vega', 'Rojas', 'Jir�n Las Amapolas 505', '978901234', 'sofia.vega@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Direcci�n], [Tel�fono], [Correo])
VALUES ('66778899', 'Ra�l', 'Flores', 'Silva', 'Calle Las Rosas 606', '989012345', 'raul.flores@example.com');

INSERT INTO [dbo].[Clientes] ([DNI/RUC], [Nombre], [ApellidoPaterno], [ApellidoMaterno], [Direcci�n], [Tel�fono], [Correo])
VALUES ('44556677', 'Elena', 'Ch�vez', 'Mu�oz', 'Pasaje Las Palmeras 707', '990123456', 'elena.chavez@example.com');
