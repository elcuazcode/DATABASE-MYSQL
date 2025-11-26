CREATE DATABASE IF NOT EXISTS cerebro_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cerebro_db;

-- tabla personas
CREATE TABLE IF NOT EXISTS personas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL UNIQUE,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- tabla informacion
CREATE TABLE IF NOT EXISTS informacion (
  id INT AUTO_INCREMENT PRIMARY KEY,
  persona_id INT,
  contenido TEXT NOT NULL,
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE
);

-- tabla temas
CREATE TABLE IF NOT EXISTS temas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre_tema VARCHAR(100) UNIQUE NOT NULL
);


-- tabla info_temas 
CREATE TABLE IF NOT EXISTS info_temas(
  informacion_id INT,
  tema_id INT,
  PRIMARY KEY (informacion_id, tema_id),
  FOREIGN KEY (informacion_id) REFERENCES informacion(id) ON DELETE CASCADE,
  FOREIGN KEY (tema_id) REFERENCES temas(id) ON DELETE CASCADE
);