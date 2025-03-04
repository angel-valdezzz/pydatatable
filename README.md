## 📌 pytabify

**📊 Tabify your data, Python-style**  

*📊 Tabula tus datos con magia Python*

**pytabify** es una librería de propósito general para la manipulación, transformación y análisis de datos tabulares obtenidos a través de diversos formatos de archivo (**CSV, JSON, Excel**). Ofrece una API intuitiva y flexible que permite crear, validar y persistir estructuras de datos (**DataTables**), facilitando su integración en proyectos de **automatización de pruebas**, **scripts** y **aplicaciones de análisis de datos**.

---

## 🚀 Características

✅ **Soporte para múltiples formatos:** Importa datos desde archivos CSV, JSON y Excel.  
✅ **Estructura tabular flexible:** Manipula datos con un enfoque basado en filas y columnas.  
✅ **Validación de datos integrada:** Usa JSON Schema para garantizar la calidad de los datos.  
✅ **Fácil integración con frameworks de pruebas:** Compatible con **Robot Framework, unittest, pytest, etc.**  
✅ **Exportación flexible:** Guarda los datos en distintos formatos según sea necesario.  

---

## 📦 Instalación

### Usando pip:
```sh
pip install pytabify
```

---

## 📖 Uso Básico

### 📌 Creando un DataTable desde un archivo
```python
from pytabify.creator import DataTableCreator

# Desde CSV
datatable = DataTableCreator.from_file("data.csv")

# Desde JSON
datatable = DataTableCreator.from_file("data.json")

# Desde Excel (requiere indicar la hoja)
datatable = DataTableCreator.from_file("data.xlsx", sheet_name="Hoja1")
```

### 📌 Accediendo a los datos
```python
# Obtener una fila específica
row = datatable[0]  
print(row.first_name.value)

# Iterar sobre filas
for row in datatable:
    print(row.to_dict())

# Modificar valores
row.new_field = "Nuevo Valor"
row["edad"] = 25
```

### 📌 Guardando datos
```python
from pytabify.saver import DataTableSaver

# Guardar en CSV
DataTableSaver.into_csv(datatable, "output.csv")

# Guardar en JSON
DataTableSaver.into_json(datatable, "output.json")

# Guardar en Excel
DataTableSaver.into_xlsx(datatable, "output.xlsx")
```

---

## 🛠️ Integración con Pruebas Automatizadas

**pytabify** está diseñado para funcionar en entornos de **pruebas automatizadas**.  
Ejemplo de uso en **Robot Framework**:

```robot
*** Settings ***
Library    pytabify.core.creator     AS    DataTableCreator

*** Test Cases ***
Leer datos desde CSV
    ${datatable}=    DataTableCreator.From File    path=data.csv
    Should Not Be Empty    ${datatable}

Validar un campo específico
    ${row}=    Get From List    ${datatable}    0
    Should Be Equal As Strings    ${row.first_name}    "Alice"
```

---

## 🧪 Pruebas

Para ejecutar los tests unitarios:

```sh
poetry run pytest -s .\utests\test_pytabify.py
```

---

## 📜 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo `LICENSE` para más detalles.

---