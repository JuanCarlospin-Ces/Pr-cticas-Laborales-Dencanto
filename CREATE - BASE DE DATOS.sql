CREATE SCHEMA IF NOT EXISTS `Gestion de viaje` CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci ;

USE `Gestion de viaje`;

-- ------------------------------------------
-- CREACIÓN DE ENTIDADES FUERTES
-- ------------------------------------------

CREATE TABLE IF NOT EXISTS Persona (

    DNI CHAR(9) NOT NULL CHECK (DNI REGEXP '^[0-9]{8}[A-Z]$'),
    Nombre VARCHAR(47) NOT NULL,
    Apellido1 VARCHAR(47) NOT NULL,
    Apellido2 VARCHAR(47) NOT NULL,
    `Fecha de nacimiento` DATE NOT NULL,
    Ciudad_Origen VARCHAR(47) NOT NULL,

    PRIMARY KEY (DNI)
);

CREATE TABLE IF NOT EXISTS Grupo(

    `Identificador de grupo` VARCHAR(10) NOT NULL,
    `Numero de integrantes` INT,

    PRIMARY KEY (`Identificador de grupo`)
);

CREATE TABLE IF NOT EXISTS Destino(

    Ciudad VARCHAR(47) NOT NULL,
    Alojamiento VARCHAR(47) NOT NULL,

    PRIMARY KEY (Ciudad)
);

CREATE TABLE IF NOT EXISTS Curso(

    Tipo VARCHAR(47) NOT NULL,
    Escuela VARCHAR(47) NOT NULL,

    PRIMARY KEY (Escuela)
    
);

-- ------------------------------------------
-- CREACIÓN DE AGREGACIONES 
-- ------------------------------------------

CREATE TABLE IF NOT EXISTS ubicado(

    `Fecha Inicio Curso` DATE NOT NULL,
    `Fecha Fin Curso` DATE NOT NULL,
    Escuela VARCHAR(47) NOT NULL,
    Ciudad VARCHAR(47) NOT NULL,

    PRIMARY KEY(Ciudad,Escuela),
    
    FOREIGN KEY(Ciudad) REFERENCES Destino (Ciudad),
    FOREIGN KEY(Escuela) REFERENCES Curso (Escuela)

);

-- ------------------------------------------
-- CREACIÓN DE CONEXIONES 
-- ------------------------------------------

CREATE TABLE IF NOT EXISTS viaja(

    Precio DECIMAL(10,2) NOT NULL,
    `Fecha Salida` DATE NOT NULL,
    `Fecha Vuelta` DATE NOT NULL,
    `Identificador de grupo` VARCHAR(10) NOT NULL,
    Escuela VARCHAR(47) NOT NULL,
    Ciudad VARCHAR(47) NOT NULL,
    
    PRIMARY KEY(`Fecha Salida`,`Fecha Vuelta`,`Identificador de grupo`,Escuela,Ciudad),

    FOREIGN KEY(`Identificador de grupo`) REFERENCES Grupo (`Identificador de grupo`),
    FOREIGN KEY(Escuela,Ciudad) REFERENCES ubicado (Escuela, Ciudad)
);

CREATE TABLE IF NOT EXISTS pertenece(

    DNI CHAR(9) NOT NULL CHECK (DNI REGEXP '^[0-9]{8}[A-Z]$'),
    `Identificador de grupo` VARCHAR(10) NOT NULL,
    
    PRIMARY KEY (DNI, `Identificador de grupo`),
    
    FOREIGN KEY (DNI) REFERENCES Persona (DNI),
    FOREIGN KEY (`Identificador de grupo`) REFERENCES Grupo (`Identificador de grupo`)
    
);