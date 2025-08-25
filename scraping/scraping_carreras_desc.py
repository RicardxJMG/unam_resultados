#%%
import os
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraping_puntaje import init_driver, get_main_content, webdriver

#%%
def extract_carrera_info(driver: webdriver.Chrome) -> dict:
    """Extrae carrera_id, facultad, oferta y aciertos_minimos de la página abierta."""
    main_html = driver.find_element(By.TAG_NAME, 'main').get_attribute('outerHTML')
    soup = BeautifulSoup(main_html, 'html.parser')

    h2_tag = soup.find('h2')
    h2_text = h2_tag.get_text(" ", strip=True) if h2_tag else ""
    
    carrera_id = None
    m = re.search(r'\((\d+)\)', h2_text)
    if m:
        carrera_id = m.group(1)
    
    facultad = None
    parts = [p.strip() for p in h2_text.split('-') if p.strip()]
    if len(parts) >= 2:
        facultad = parts[1]

    span_tag = soup.find('span')
    span_text = span_tag.get_text(" ", strip=True) if span_tag else ""

    oferta = None
    mo = re.search(r'Oferta\s*=?\s*(\d+)', span_text, re.I)
    if mo:
        oferta = int(mo.group(1))

    aciertos_minimos = None
    ma = re.search(r'Aciertos\s*Minimos\s*=?\s*(\d+)', span_text, re.I)
    if ma:
        aciertos_minimos = int(ma.group(1))

    return {
        "carrera_id": carrera_id,
        "facultad": facultad,
        "oferta": oferta,
        "aciertos_minimos": aciertos_minimos
    }


def scrape_carrera_descripcion(pages:list ) -> pd.DataFrame:
    driver = init_driver()
    resultados = []

    for area, page in enumerate(pages, start=1):
        print(f"\n=== Área {area} ===")
        main_content = get_main_content(driver, page)
        if not main_content: continue
        
        carreras = main_content.find_elements(By.CLASS_NAME, 'post-preview')

        for carrera in carreras:
            escuelas = carrera.find_elements(By.TAG_NAME, 'a')

            for escuela in escuelas:
                escuela_nombre = escuela.text.strip()
                print(f"> Procesando: {escuela_nombre}")

                escuela.click()

                try:
                    time.sleep(3)
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'span')))
                    info = extract_carrera_info(driver)
                    if info:
                        resultados.append(info)
                except Exception as e:
                    print(f"  Error extrayendo info: {e}")
                driver.back()
                time.sleep(0.5)

    driver.quit()
    return pd.DataFrame(resultados)


if __name__ == "__main__":
    pages:list  = [f'https://www.dgae.unam.mx/Licenciatura2025/resultados/{i}5.html' for i in range(1, 5)]
    df = scrape_carrera_descripcion(pages)

    os.makedirs("./../datos/raw", exist_ok=True)
    output_path = "./../datos/raw/carrera_descripcion.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"\nArchivo guardado en {output_path}")
    print(df.head())
