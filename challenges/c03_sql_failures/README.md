Challenge 3: SQL – Advertising System Failures Report
Objetivo del Desafío

El objetivo de este challenge es escribir una consulta SQL que identifique a los clientes que presentan más de 3 eventos con estado "failure" dentro del sistema de campañas publicitarias.

La consulta debe:

Contar la cantidad total de fallos por cliente (sumando fallos en todas sus campañas).

Incluir únicamente a los clientes con más de 3 fallos.

Listar dos columnas:
customer (nombre completo del cliente)
failures (cantidad de fallos)

Ordenar el resultado por el número de fallos en orden descendente.

Ser entregada en un archivo llamado applicant_query.sql.

Solución Implementada

Enfoque Algorítmico
La lógica SQL aplicada es la siguiente:

Se unen las tablas customers, campaigns y events a través de sus claves foráneas para relacionar cada evento con su cliente correspondiente.

Se filtran únicamente los eventos con status = 'failure'.

Se agrupan los registros por cliente para obtener la cantidad total de fallos.

Se aplica un filtro HAVING para conservar solo los clientes con más de 3 fallos.

Se ordena el resultado en orden descendente de fallos.

Se genera una columna customer que combina first_name y last_name.

Este enfoque garantiza que todos los fallos en todas las campañas del cliente sean sumados correctamente.

Estructura del Código
Los archivos relevantes del challenge son:

challenges/c03_sql_failures/sqlUtils/applicant_query.sql
Contiene la consulta SQL solicitada por el challenge.

challenges/c03_sql_failures/tests/test_databaseDAO.py
Pruebas en Python que crean una base de datos SQLite temporal, cargan los datos de ejemplo y ejecutan la consulta para validar su correcto funcionamiento.

challenges/c03_sql_failures/sqlUtils/databaseDAO.py
Código auxiliar que ejecuta la consulta SQL y expone los resultados para las pruebas unitarias.

challenges/c03_sql_failures/run.py
Script que ejecuta la misma consulta contra la base de datos incluida en el proyecto y muestra los resultados por consola.

Instrucciones de Ejecución

Ubicarse en la raíz del proyecto.

Opción A: usando make
make run-ch3

Opción B: usando Poetry
poetry run python challenges/c03_sql_failures/run.py

Ejemplo de Entrada y Salida

Los datos de entrada provienen de las tablas customers, campaigns y events.

Ejemplo de salida esperada usando los datos del PDF:

customer
Whitney Ferrero
failures
6

Pruebas Unitarias

Las pruebas están en:
challenges/c03_sql_failures/tests/test_databaseDAO.py

Para ejecutarlas:
poetry run pytest challenges/c03_sql_failures/