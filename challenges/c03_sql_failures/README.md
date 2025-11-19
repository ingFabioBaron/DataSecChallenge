# Challenge 3 · SQL – Advertising Failures Report

## 📋 Resumen del problema
Escribir una consulta SQL (`applicant_query.sql`) que identifique a los clientes con **más de 3 eventos fallidos** dentro del sistema publicitario.  
La salida debe contener:
- `customer`: nombre y apellido concatenados.
- `failures`: número total de eventos con `status = 'failure'`.
- Orden descendente por `failures`.

### Modelo de datos
| Tabla      | Campos relevantes                                  |
|------------|-----------------------------------------------------|
| `customers`| `id`, `first_name`, `last_name`                     |
| `campaigns`| `id`, `customer_id`, `name`                         |
| `events`   | `dt`, `campaign_id`, `status ∈ {success, failure}`  |

Las relaciones siguen la cadena `customers → campaigns → events`.

## 🧠 Estrategia de la consulta
```sql
SELECT
    first_name || ' ' || last_name AS customer,
    COUNT(*) AS failures
FROM customers
JOIN campaigns ON campaigns.customer_id = customers.id
JOIN events ON events.campaign_id = campaigns.id
WHERE events.status = 'failure'
GROUP BY customers.id
HAVING COUNT(*) > 3
ORDER BY failures DESC;
```

Puntos clave:
- Se usa `JOIN` explícito para garantizar consistencia referencial.
- El `WHERE` filtra sólo fallos antes del `GROUP BY`.
- `HAVING COUNT(*) > 3` aplica el umbral pedido.
- `COUNT(*)` es seguro porque los `JOIN` ya restringen a eventos fallidos.

## 🗂️ Organización
- `applicant_query.sql`: query entregable.
- `sqlUtils/databaseDAO.py`: inicialización de SQLite, lectura de `.sql` y helpers para pruebas/CLI.
- `sqlUtils/schema.sql` y `sample_data.sql`: crean y cargan datos de ejemplo.
- `run.py`: ejecuta la consulta contra la base local y registra los resultados.
- `tests/test_databaseDAO.py`: valida E2E que la query arroje los clientes esperados.

## ⚙️ Variables de entorno
- `DB_PATH` (opcional): ruta al archivo SQLite. Si no existe, se crea en `challenges/c03_sql_failures/database.sqlite3`.

## ▶️ Ejecución
Desde la raíz del repo:

**Con Make**
```bash
make run-ch3
```

**Con Poetry**
```bash
poetry run python challenges/c03_sql_failures/run.py
```
El script:
1. Verifica la conexión (`test_connection`).
2. Inicializa la DB si aún no existen tablas (carga schema + sample data).
3. Ejecuta `applicant_query.sql` y loguea cada fila.

## 🧪 Pruebas unitarias
```bash
poetry run pytest challenges/c03_sql_failures/
```
Cobertura:
- Creación on-demand de la base con datos de ejemplo.
- Ejecución de la consulta y comparación contra resultados esperados.
- Manejo de rutas inexistentes o SQL inválido (errores controlados).

## 🧾 Ejemplo de resultado
Con los datos provistos, el resultado parcial luce así:
```
customer          | failures
--------------------------------
Whitney Ferrero   | 6
Jonathan Darnell  | 4
```

## 🚧 Edge cases contemplados
- Base sin inicializar: el DAO crea estructura y datos automáticamente.
- `DB_PATH` apuntando a carpetas que no existen: se crean de forma recursiva.
- Datos faltantes o campañas sin eventos → no aparecen en el resultado (count = 0).