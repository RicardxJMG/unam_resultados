#%%
import os
import pandas as pd 
import time 
from typing import List, Any
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def init_driver(driver_path: str = "C:/WebDrivers/chromedriver.exe") -> webdriver.Chrome | None:
    print("> Iniciando driver...")
    try:
        driver = webdriver.Chrome(service = Service(driver_path))
    except Exception as e:
        print(f"Error initializing the driver: {e}")
        return None
    return driver


def get_main_content(driver: webdriver.Chrome, url: str) -> webdriver.Chrome:
    print(f"> Accediendo al siguiente url: {url}")
    try:
        driver.get(url)
        main_content = driver.find_element(by = By.TAG_NAME, value='main')
    except Exception as e:
        print(f"Cannot get main content from {url}: {e}")
        return None

    return main_content

def get_scores_from_school(scores_table: BeautifulSoup, career_id: str, school_id: str, area: int) -> pd.DataFrame:
    acreditado_dict: dict = {
                'S': 'Seleccionado',
                '': 'No seleccionado',
                'C': 'Cancelado',
                'N': 'No presentado'
            }
    
    area_dict: dict = {1: 'A1', 2: 'A2', 3: 'A3', 4: 'A4'}
    
    try: 
        
        header_table = [th.text.strip() for th in scores_table.find('thead').find_all('th')]
        scores_data = scores_table.find('tbody').find_all('tr')
        table_data = [[td.text.strip() for td in row.find_all('td')] for row in scores_data]
        
        df_scores = pd.DataFrame(columns=header_table, data = table_data)
        
        df_scores = df_scores.drop(columns =['Detalles', 'Diagnóstico'], axis =1)
        rename_cols = {'Número de comprobante': 'id_aspirante',
                       'Aciertos': 'puntaje',
                       'Acreditado': 'acreditado'}
        
        rows, _ = df_scores.shape
        
        df_scores.rename(columns=rename_cols, inplace=True)
        df_scores['acreditado'] = df_scores['acreditado'].map(acreditado_dict)
        
        df_scores['id_carrera'] = [career_id]*rows
        df_scores['id_facultad'] = [school_id]*rows
        df_scores['id_area'] = [area_dict[area]]*rows      

        print(f'>>> Resultados obtenidos para la carrera {career_id} del área {area_dict[area]}')
        
    except Exception as e:
        print(f"Error processing scores table: {e}")
        return None
    
    return df_scores

def get_scores_career(driver: webdriver, schools: list[webdriver.Chrome], career_id: str, area: int) -> List[Any]:
    df_career_scores = pd.DataFrame(columns=['id_aspirante', 'id_area', 'id_facultad', 'id_carrera', 'puntaje', 'acreditado'])
    schools_info: set[list] = set()
    
    try:
        for school in schools:
            school_name: str = school.text.strip()
            school_id: str = school.get_attribute('href')[-10:-5]
            schools_info.add((school_id, school_name))

            print(f">> Obteniendo resultados de la carrera: {career_id} en la escuela: {school_name}")
 
            school.click()

            MAX_INTENTOS = 12
            tries = 0
            table_finding = False

            while tries < MAX_INTENTOS:
                try:
                    WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'table'))
                    )
                    tabla_html = driver.find_element(By.TAG_NAME, 'table').get_attribute('outerHTML')
                    score_table_bs = BeautifulSoup(tabla_html, 'html.parser')
                    
                    df_career_scores = pd.concat([df_career_scores, 
                                                get_scores_from_school(score_table_bs, school_id, career_id, area)], ignore_index=True)

                    table_finding = True
                    break  

                except Exception as e:
                    print(f">>> Intento {tries + 1}: no se encontró la tabla. Recargando...")
                    driver.refresh()
                    time.sleep(2)
                    tries += 1

            if not table_finding:
                print(f">>> No se pudo obtener tabla para {school_name} después de varios intentos.")
            
            driver.back()  # Regresar a la lista de escuelas

    except Exception as e: 
        print(f">>> Error procesando carrera {career_id}: {e}")
        raise

    return [df_career_scores, schools_info]

    
def get_scores_area(driver: webdriver, area_page: List[webdriver.Chrome], area: int) -> List[Any]:    

    df_area_scores = pd.DataFrame(columns=['id_aspirante','id_area', 'id_facultad', 'id_carrera', 'puntaje', 'acreditado'])
    
    career_info: dict[str, set] = {
        #this dictionary storage info of each career
        'id_carrera': list(),
        'id_area': list(),
        'carrera': list()
    }
    
    schools_info: set[tuple] = set()
    
    try:
        for career in area_page:
            career_bs = BeautifulSoup(career.get_attribute('outerHTML'), 'html.parser')
            career_name = career_bs.find('h3').text.strip()
            
            schools_bs = career_bs.find_all('a')

            career_id = schools_bs[0]['href'][2:5]
            
            career_info['id_carrera'].append(career_id)
            career_info['id_area'].append(f'A{area}') 
            career_info['carrera'].append(career_name)
        
            # schools_id.append(a_href['href'][5:10] for a_href in href_ids)
                    
            schools = career.find_elements(by=By.TAG_NAME, value='a')
            tmp_scores, tmp_schools = get_scores_career(driver=driver, schools=schools, career_id=career_id, area=area)
            df_area_scores = pd.concat([df_area_scores, tmp_scores],ignore_index=True)

            schools_info = schools_info.union(tmp_schools)
        # convert the whole info into a dataframe    
        career_df = pd.DataFrame(career_info)
    except Exception as e:
        print(f"\n> Error processing area {area}: {e}")
        driver.quit()
        raise

    return [df_area_scores, career_df, schools_info]

def get_scores(pages: list[str]) -> List[pd.DataFrame] | None:
    df_area_scores = pd.DataFrame(columns=['id_aspirante', 'id_facultad','id_area', 'id_carrera', 'puntaje', 'acreditado'])
    df_career_info = pd.DataFrame(columns=['id_carrera', 'id_area', 'carrera'])
    schools_info: set[tuple] = set()
    
    driver = init_driver()
    
    if driver is not None:
        for area,page in enumerate(pages):
            print(f'\n::::: Obteniendo datos de las carreras del área {area + 1} :::::\n')
            main_content = get_main_content(driver, page)
            if main_content is not None:
                career_content = main_content.find_elements(by=By.CLASS_NAME, value='post-preview')
                #modificar porque ahora devuelve hasta tres valores
                tmp_scores, tmp_career, tmp_schools = get_scores_area(driver=driver, area_page=career_content,area =  area+1)
                df_area_scores = pd.concat([df_area_scores,tmp_scores], ignore_index=True)
                df_career_info = pd.concat([df_career_info, tmp_career], ignore_index=True)
                schools_info = schools_info.union(tmp_schools)
                
            else:
                print(f'No main content found for {page}')
    else:
        driver.quit()
        print('Driver initialization failed')
        return None    
    
    driver.quit()
    
    df_schools_info = pd.DataFrame(columns = ['id_facultad', 'facultad'], data = schools_info)
    
    return [df_area_scores, df_career_info, df_schools_info]


#%%
if __name__ == "__main__":
    # Testeando 
    
    pages = [f'https://www.dgae.unam.mx/Licenciatura2025/resultados/{i}5.html' for i in range(1,5)]    
    datos_path = './datos'
    df_scores, df_career_info, df_school_info = get_scores(pages=pages)
    if df_scores.empty is not None:
        os.makedirs(datos_path, exist_ok=True)
        ruta_1 = os.path.join(datos_path, 'resultados_unam_2025.csv')
        ruta_2 = os.path.join(datos_path, 'carreras_info.csv')
        ruta_3 = os.path.join(datos_path, 'facultades_info.csv')
        
        df_scores.to_csv(ruta_1, index=False)
        df_career_info.to_csv(ruta_2, index=False)
        df_school_info.to_csv(ruta_3, index=False)
        print(f"Scrapping completado :D\n")
        
    else:
        print("No se pudo hacer el scrapping.")