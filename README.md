# Aplicación Web de Gestión de Facturas y Usuarios

Este repositorio contiene el código fuente y archivos necesarios para el desarrollo y despliegue de una aplicación web creada con Flask. La aplicación se enfoca en la gestión de usuarios y facturas en una base de datos MySQL.

## Características Principales

- Registro y visualización de usuarios.
- Registro y visualización de facturas con detalles y precios.
- Seguridad de datos y manejo de usuarios con base en autenticación.
- Uso de base de datos MySQL para almacenamiento y recuperación de datos.
- Estructura de rutas y vistas utilizando el framework Flask.

## Requisitos

- Python 3.7 o superior.
- Flask y dependencias (`flask`, `mysql-connector`).
- Base de datos MySQL configurada según `db_config`.

## Cómo Usar

1. Clona este repositorio en tu máquina local.
2. Asegúrate de tener Python 3.7 o superior instalado.
3. Instala las dependencias necesarias usando `pip install -r requirements.txt`.
4. Configura la conexión a tu base de datos en el archivo `app.py` (variable `db_config`).
5. Ejecuta la aplicación con `python app.py`.
6. Accede a la aplicación en tu navegador a través de `http://localhost:3000`.

## Contribución

¡Siéntete libre de contribuir a este proyecto! Puedes abrir un *pull request* para proponer mejoras, solucionar problemas o agregar nuevas características.

---
Creado por Edwin Romero - ecro98.98@gmail.com
