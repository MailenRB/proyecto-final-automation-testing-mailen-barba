# Framework de Automatización de Pruebas - Trabajo Final Integrador

Este repositorio contiene el **Trabajo Final Integrador** para el curso de Automation Testing. Consiste en un framework de pruebas automatizado desarrollado en **Python** que combina pruebas de interfaz de usuario (UI) mediante **Selenium WebDriver**, pruebas de servicios REST (API) mediante la biblioteca **Requests**, estructuración estructurada con el patrón **Page Object Model (POM)**, generación automática de reportes HTML detallados y sistema de logging integrado.

---

## 🚀 Tecnologías Utilizadas

- **Lenguaje:** [Python 3.13+](https://www.python.org/)
- **Framework de Testing:** [Pytest](https://pytest.org/)
- **Automatización de UI:** [Selenium WebDriver](https://www.selenium.dev/)
- **Pruebas de API:** [Requests](https://requests.readthedocs.io/)
- **Reportes:** [pytest-html](https://github.com/pytest-dev/pytest-html)
- **CI/CD:** [GitHub Actions](https://github.com/features/actions)
- **Control de Versiones:** [Git](https://git-scm.com/) y [GitHub](https://github.com/)

---

## 📂 Estructura del Proyecto

El proyecto está organizado de manera modular siguiendo las mejores prácticas de la industria:

```text
proyecto-final-automation-testing-mailen-barba/
│
├── .github/workflows/
│   └── run-tests.yml        # Configuración del pipeline de CI/CD (GitHub Actions)
│
├── data/
│   ├── .gitkeep
│   └── test_data.json       # Datos externos para parametrizar las pruebas (URLs, credenciales, etc.)
│
├── logs/
│   ├── .gitkeep
│   └── execution.log        # Archivo persistente con el registro de logs de las pruebas ejecutadas
│
├── pages/                   # Clases correspondientes al patrón Page Object Model (POM)
│   ├── __init__.py
│   ├── base_page.py         # Clase base con wrappers de Selenium (esperas explícitas, clic, etc.)
│   ├── login_page.py        # Localizadores y acciones de la página de Login
│   ├── inventory_page.py    # Localizadores y acciones de la página de productos (añadir/remover, ordenar)
│   ├── cart_page.py         # Localizadores y acciones de la página del carrito
│   └── checkout_page.py     # Localizadores y acciones del formulario y confirmación de compra
│
├── reports/
│   ├── .gitkeep
│   └── screenshots/         # Capturas de pantalla guardadas automáticamente en caso de fallos de UI
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py          # Casos de prueba automatizados para el Backend (API)
│   └── test_ui.py           # Casos de prueba automatizados para el Frontend (UI)
│
├── utils/
│   ├── __init__.py
│   ├── data_reader.py       # Utilidad para cargar la configuración y datos desde test_data.json
│   └── logger.py            # Configuración del Logger centralizado (consola y archivo)
│
├── .gitignore               # Exclusiones de archivos para Git (entorno virtual, logs y reportes locales)
├── conftest.py              # Fixtures de Pytest (configuración de WebDriver y capturador de fallas)
├── pytest.ini               # Argumentos y configuraciones del test runner por defecto
└── requirements.txt         # Lista de dependencias del framework
```

---

## 🛠️ Instalación y Configuración

Sigue estos pasos para configurar el proyecto en tu entorno local:

1. **Clonar el repositorio:**
   ```bash
   git clone <enlace-de-tu-repositorio-en-github>
   cd proyecto-final-automation-testing-mailen-barba
   ```

2. **Crear e inicializar el entorno virtual (Recomendado):**
   * En Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   * En macOS / Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧪 Ejecución de Pruebas

Pytest está configurado mediante `pytest.ini` para generar por defecto un reporte HTML en `reports/report.html`.

### 1. Ejecutar la Suite Completa (10 casos de prueba: 5 UI y 5 API)
- **Modo Headless (Recomendado, sin levantar ventana del navegador):**
  ```bash
  pytest --headless
  ```
- **Modo Gráfico (Se abrirá la ventana de Chrome para las pruebas de UI):**
  ```bash
  pytest
  ```

### 2. Ejecutar solo Pruebas de UI (Selenium)
- Ejecuta los 5 casos de prueba de UI (Login exitoso, Login fallido, Añadir al carrito, Remover del carrito y Checkout completo):
  ```bash
  pytest tests/test_ui.py --headless
  ```

### 3. Ejecutar solo Pruebas de API (Requests)
- Ejecuta los 5 casos de prueba de API (GET, POST, DELETE, Encadenamiento GET-GET, Encadenamiento POST-PUT-DELETE a JSONPlaceholder):
  ```bash
  pytest tests/test_api.py
  ```

---

## 📊 Visualización de Reportes y Logs

### Reportes HTML
Al finalizar la ejecución, abre el reporte generado en tu navegador:
- **Ruta del reporte:** `reports/report.html`
- **Captura automática de fallas:** Si una prueba de UI falla, el framework captura una screenshot del navegador, la guarda en `reports/screenshots/` y la incrusta directamente en la fila correspondiente al test fallido en el reporte HTML para facilitar el diagnóstico.

### Logs del Sistema
Todas las acciones críticas realizadas por las clases POM y los assertions de pruebas son registradas en consola y en un archivo de log físico:
- **Ruta de logs:** `logs/execution.log`
- **Seguridad:** El framework oculta los caracteres de la contraseña reemplazándolos por asteriscos (`******`) en los logs para resguardar la privacidad.

---

## 🚀 Integración Continua (CI/CD)

El repositorio incluye un pipeline de **GitHub Actions** configurado en `.github/workflows/run-tests.yml`. 
- Se ejecuta automáticamente ante cada evento `push` o `pull_request` sobre las ramas `main` o `master`.
- Levanta un contenedor Ubuntu, instala Python, instala las dependencias de `requirements.txt`, ejecuta la suite en modo headless y archiva la carpeta de reportes y logs (`reports/` y `logs/`) como un artefacto descargable en la interfaz de GitHub Actions para que puedas examinar los reportes de ejecuciones en la nube.