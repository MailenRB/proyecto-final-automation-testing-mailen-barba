import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False, help="ejecuta las pruebas en modo headless (sin cabezal)")

@pytest.fixture(scope="function")
def driver(request):
    sin_cabezal = request.config.getoption("--headless")
    opciones_chrome = Options()
    if sin_cabezal:
        opciones_chrome.add_argument("--headless")
        opciones_chrome.add_argument("--disable-gpu")
        opciones_chrome.add_argument("--window-size=1920,1080")
        opciones_chrome.add_argument("--no-sandbox")
        opciones_chrome.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=opciones_chrome)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    resultado = yield
    reporte = resultado.get_result()
    
    if reporte.when == "call" and reporte.failed:
        if "driver" in item.fixturenames:
            controlador_web = item.funcargs["driver"]
            # Crear directorio de reportes y capturas de pantalla
            dir_base = os.path.dirname(os.path.abspath(__file__))
            dir_reportes = os.path.join(dir_base, "reports")
            dir_capturas = os.path.join(dir_reportes, "screenshots")
            os.makedirs(dir_capturas, exist_ok=True)
            
            ahora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nombre_prueba = item.name
            nombre_archivo = f"{nombre_prueba}_{ahora}.png"
            ruta_archivo = os.path.join(dir_capturas, nombre_archivo)
            
            controlador_web.save_screenshot(ruta_archivo)
            
            # Incrustar en el Reporte HTML de Pytest
            extra = getattr(reporte, "extra", [])
            ruta_relativa = f"screenshots/{nombre_archivo}"
            
            try:
                import pytest_html
                extra.append(pytest_html.extras.image(ruta_relativa))
            except Exception:
                # Alternativa directa con etiqueta HTML
                html = f'<div><img src="{ruta_relativa}" alt="captura" style="width:300px;height:225px;" onclick="window.open(this.src)" align="right"/></div>'
                extra.append(html)
            
            reporte.extra = extra
