"""Librería para manejar tablas de datos en Python.
Se puede utilizar para leer datos de archivos CSV, JSON o diccionarios y luego utilizarlos en pruebas automatizadas.
Se puede integrar con cualquier framework de testing para pruebas automatizadas como pytest, unittest, robot framework, etc.

Ejemplo con pytest y playwright:
```python
from playwright.sync_api import Page
from playwright.mark import parametrize
from data_table_library import TestDataRow

@parametrize("row", TestDataCreator.from_csv("path/to/file.csv"))
def test_scenario(row: TestDataRow, page: Page):
    page.goto("https://example.com")
    page.fill("input[name='id']", row.id)
    page.fill("input[name='first_name']", row.first_name)
    page.fill("input[name='last_name']", row.last_name)
    page.fill("input[name='age']", row.age)
    page.click("button[type='submit']")
```

Ejemplo con robot framework:
```robot
*** Settings ***
Library    TestDataLibrary
Test Template    Tests Template
Test Setup    Tests Setup
Test Teardown    Test Teardown


**** Variables ****
${TEST_DATA}    ${None}


*** Test Cases ***
Data Driven Test 1      1
Data Driven Test 2      2
Data Driven Test 3      3
Data Driven Test 4      4


*** Keywords ***
Tests Setup
    ${data_table}=    Create Data Table    path_to_test_data
    Set Suite Variable    ${TEST_DATA}    ${data_table}

Test Teardown
    No Operation

Test Template
    [Arguments]    ${index}
    ${data_row}=    Get Data Table Row    ${TEST_DATA}    ${index}
    Log    ${data_row.id}
    Log    ${data_row.first_name}
    Log    ${data_row.last_name}
    Log    ${data_row.age}
    Do Something    ${data_row.id}    ${data_row.first_name}    ${data_row.last_name}    ${data_row.age}
```
"""
