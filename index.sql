-- Crear la base de datos "test"
CREATE DATABASE IF NOT EXISTS test;

-- Utilizar la base de datos "test"
USE test;

-- Crear la tabla "users"
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255),
  name VARCHAR(255),
  password VARCHAR(255)
);

-- Agregar datos de ejemplo a la tabla "users"
INSERT INTO users (username, name, password) VALUES
  ('user1', 'User One', 'password1'),
  ('user2', 'User Two', 'password2'),
  ('user3', 'User Three', 'password3');
