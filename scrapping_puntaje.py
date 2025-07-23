import pandas as pd 
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 


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

def get_scores_from_school(scores_table: webdriver.Chrome, school_name: str, career_name: str, area: int) -> pd.DataFrame:
    
    id_list: list[str] = []
    score_list: list[str | int] = []
    accepted_list: list[str] = []
    
    acreditado_dict: dict = {
                'S': 'Seleccionado',
                '': 'No seleccionado',
                'C': 'Cancelado',
                'N': 'No presentado'
            }
    
    area_dict: dict = {1: 'A1', 2: 'A2', 3: 'A3', 4: 'A4'}
    
    try: 
        rows = scores_table.find_elements(by = By.TAG_NAME, value = 'tr')
        for row in rows:  
            cells = row.find_elements(by = By.TAG_NAME, value = 'td')
            id_list.append(cells[0].text)
            score_list.append(cells[1].text)
            accepted_list.append(acreditado_dict[cells[2].text])
        
        career_list: list[str] = [career_name]*len(id_list)
        school_list: list[str] = [school_name]*len(id_list)
        area_list: list[str] = [area_dict[area]]*len(id_list)
        
        data: dict = {
            'id_aspirante': id_list,
            'escuela': school_list,
            'carrera': career_list,
            'area': area_list,
            'puntaje': score_list,
            'acreditado': accepted_list
        }
        
        print(f'>>> Resultados obtenidos de la escuela {school_name} para la carrera {career_name} del área {area_dict[area]}')
        return pd.DataFrame(data)

    except Exception as e:
        print(f"Error processing scores table: {e}")
        return pd.DataFrame(columns=['id_aspirante', 'escuela', 'carrera','area', 'puntaje', 'acreditado'])


def get_scores_career(driver: webdriver.Chrome, schools: webdriver.Chrome, career_name: str, area: int) -> pd.DataFrame:
    df_career_scores = pd.DataFrame(columns=['id_aspirante', 'escuela','area', 'carrera', 'puntaje', 'acreditado'])
    try:
        for school in schools:
            school_name: str = school.text
            school.click()
            print(f">> Obteniendo resultados de la carrera: {career_name} en la escuela: {school_name}")
            
            df_career_scores = pd.concat([df_career_scores,
                                            get_scores_from_school(driver.find_element(by = By.TAG_NAME, value='tbody'),
                                            school_name, career_name, area)],
                                            ignore_index=True)
            driver.back() # go back to A(i) list
    
    except Exception as e: 
        print(f"Error processing career {career_name}: {e}")
        return df_career_scores
    return df_career_scores

    
def get_scores_area(driver: webdriver.Chrome, area_page: list[str], area: int) -> pd.DataFrame:    
    df_area_scores = pd.DataFrame(columns=['id_aspirante', 'escuela','area', 'carrera', 'puntaje', 'acreditado'])
    try:
        for career in area_page:
            career_name = career.find_element(by=By.TAG_NAME, value='h3').text
            schools = career.find_elements(by=By.TAG_NAME, value='a')
            print(f"> Accediendo a los resultados de la carrera: {career_name}")

            df_area_scores = pd.concat([df_area_scores, 
                                        get_scores_career(driver, schools, career_name, area)],
                                        ignore_index=True)
            print()
    except Exception as e:
        print(f"Error processing area {area}: {e}")
        return df_area_scores
    
    return df_area_scores

def get_scores(pages: list[str]) -> pd.DataFrame:
    df_area_scores = pd.DataFrame(columns=['id_aspirante', 'escuela','area', 'carrera', 'puntaje', 'acreditado'])
    driver = init_driver()
    if driver is not None:
        for area,page in enumerate(pages):
            print(f'\n::::: Obteniendo datos de las carreras del área {area + 1} :::::\n')
            main_content = get_main_content(driver, page)
            if main_content is not None:
                career_content = main_content.find_elements(by=By.CLASS_NAME, value='post-preview')
                df_area_scores = pd.concat([df_area_scores,
                                            get_scores_area(driver, career_content, area+1)],
                                            ignore_index=True)
            else:
                print(f'No main content found for {page}')
    else:
        print('Driver initialization failed')
        return df_area_scores
    
    driver.quit()
    return df_area_scores
#%%
if __name__ == "__main__":

    pages = [f'https://www.dgae.unam.mx/Licenciatura2025/resultados/{i}5.html' for i in range(1,5)]    
    datos_path = './datos'
    df_area_scores = get_scores(pages)
    if not df_area_scores.empty:
        os.makedirs(datos_path, exist_ok=True)
        ruta = os.path.join(datos_path, 'resultados_unam_2025.csv')
        df_area_scores.to_csv(ruta, index=False)
        print(f"Scrapping completado :D\n Tamaño del DataFrame: {df_area_scores.shape}")
        
    else:
        print("No se pudo hacer el scrapping.")