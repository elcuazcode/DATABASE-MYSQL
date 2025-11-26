-- Crear tabla de autores
CREATE TABLE autores (
    id_autor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    nacionalidad VARCHAR(50),
    fecha_nacimiento DATE,
    CONSTRAINT nombre_completo UNIQUE (nombre, apellido)
);

-- Crear tabla de libros
CREATE TABLE libros (
    id_libro INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    id_autor INT NOT NULL,
    isbn VARCHAR(13) UNIQUE,
    editorial VARCHAR(100),
    anio_publicacion YEAR,
    categoria VARCHAR(50),
    copias_disponibles INT DEFAULT 1,
    FOREIGN KEY (id_autor) REFERENCES autores(id_autor) ON DELETE RESTRICT
);

-- Crear tabla de usuarios
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    fecha_registro DATE DEFAULT (CURRENT_DATE),
    activo BOOLEAN DEFAULT TRUE
);

-- Crear tabla de préstamos
CREATE TABLE prestamos (
    id_prestamo INT AUTO_INCREMENT PRIMARY KEY,
    id_libro INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha_prestamo DATE NOT NULL DEFAULT (CURRENT_DATE),
    fecha_devolucion_esperada DATE NOT NULL,
    fecha_devolucion_real DATE,
    estado ENUM('activo', 'devuelto', 'atrasado') DEFAULT 'activo',
    FOREIGN KEY (id_libro) REFERENCES libros(id_libro) ON DELETE RESTRICT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT
);

-- Insertar datos de ejemplo
INSERT INTO autores (nombre, apellido, nacionalidad, fecha_nacimiento) VALUES
('Gabriel', 'Garcia Marquez', 'Colombiano', '1927-03-06'),
('Isabel', 'Allende', 'Chilena', '1942-08-02'),
('Mario', 'Vargas Llosa', 'Peruano', '1936-03-28'),
('Jorge Luis', 'Borges', 'Argentino', '1899-08-24');

INSERT INTO libros (titulo, id_autor, isbn, editorial, anio_publicacion, categoria, copias_disponibles) VALUES
('Cien anos de soledad', 1, '9780307474728', 'Sudamericana', 1967, 'Ficcion', 3),
('El amor en los tiempos del colera', 1, '9780307389732', 'Oveja Negra', 1985, 'Romance', 2),
('La casa de los espiritus', 2, '9780525433446', 'Plaza & Janes', 1982, 'Ficcion', 2),
('La ciudad y los perros', 3, '9788420412146', 'Seix Barral', 1963, 'Ficcion', 1),
('Ficciones', 4, '9780802130303', 'Sur', 1944, 'Cuentos', 2);

INSERT INTO usuarios (nombre, apellido, email, telefono) VALUES
('Juan', 'Perez', 'juan.perez@email.com', '555-0101'),
('Maria', 'Gonzalez', 'maria.gonzalez@email.com', '555-0102'),
('Carlos', 'Rodriguez', 'carlos.rodriguez@email.com', '555-0103');

INSERT INTO prestamos (id_libro, id_usuario, fecha_prestamo, fecha_devolucion_esperada, estado) VALUES
(1, 1, '2025-11-01', '2025-11-15', 'activo'),
(3, 2, '2025-11-10', '2025-11-24', 'activo'),
(2, 1, '2025-10-15', '2025-10-29', 'devuelto');

