#%%
import pandas as pd 
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from bs4 import BeautifulSoup, Tag 


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
        df_scores['id_escuela'] = [school_id]*rows
        df_scores['id_area'] = [area_dict[area]]*rows
        
        print(df_scores.sample(3))
        
        

        print(f'>>> Resultados obtenidos de la escuela {school_id} para la carrera {career_id} del área {area_dict[area]}')
        
        return df_scores

    except Exception as e:
        print(f"Error processing scores table: {e}")
        return pd.DataFrame(columns=['id_aspirante','id_area', 'id_escuela', 'id_carrera', 'puntaje', 'acreditado'])


def get_scores_career(driver: webdriver.Chrome, schools: list[webdriver.Chrome], career_id: str, area: int) -> pd.DataFrame:
    df_career_scores = pd.DataFrame(columns=['id_aspirante','id_area', 'id_escuela', 'id_carrera', 'puntaje', 'acreditado'])

    school_info: list[list] = list() # what should I do with this?....
    try:
        for school in schools:
            
            school_name: str = school.text.strip()
            school_id:str = school.get_attribute('href')[-10:-5]
            school_info.append([school_name, school_id])
            
            school.click()
            print(f">> Obteniendo resultados de la carrera: {career_id} en la escuela: {school_name}")
            score_table_bs = BeautifulSoup(driver.find_element(by=By.TAG_NAME , 
                                                                value = 'table').get_attribute('outerHTML'), 'html.parser')
            # print(score_table_bs)
            
            df_career_scores = pd.concat([df_career_scores,
                                            get_scores_from_school(score_table_bs,
                                            school_id, career_id, area)],
                                            ignore_index=True)
            driver.back() # go back to A(i) list
    
    except Exception as e: 
        print(f"Error processing career {career_id}: {e}")
        raise
    
    return df_career_scores

    
def get_scores_area(driver: webdriver, area_page: list[webdriver.Chrome], area: int) -> pd.DataFrame:    

    df_area_scores = pd.DataFrame(columns=['id_aspirante','id_area', 'id_escuela', 'id_carrera', 'puntaje', 'acreditado'])
    
    schools_info: dict[str, set] = {
        'id_plantel': set(), 
        'plantel': set()
    } 
    
    carrera_info: dict[str, set] = {
        #this dictionary storage info of each career
        'id_carrera': set(),
        'id_area': set(),
        'carrera': set()
    }
    
    try:
        for career in area_page:
            career_bs = BeautifulSoup(career.get_attribute('outerHTML'), 'html.parser')
            career_name = career_bs.find('h3').text.strip()
            
            schools_bs = career_bs.find_all('a')

            career_id = schools_bs[0]['href'][2:5]
            
            carrera_info['id_area'].add(career_id) 
            carrera_info['id_area'].add(f'A{area}')
            carrera_info['carrera'].add(career_name)   
            # schools_id.append(a_href['href'][5:10] for a_href in href_ids)
                    
            schools = career.find_elements(by=By.TAG_NAME, value='a')
            
            df_area_scores = pd.concat([df_area_scores, 
                                        get_scores_career(driver, schools, career_id, area)],
                                        ignore_index=True)
    except Exception as e:
        print(f"\n> Error processing area {area}: {e}")
        driver.quit()
        raise
        
    return df_area_scores

def get_scores(pages: list[str]) -> pd.DataFrame:
    df_area_scores = pd.DataFrame(columns=['id_aspirante', 'id_escuela','id_area', 'id_carrera', 'puntaje', 'acreditado'])
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
    # Testeando 
    pages = [f'https://www.dgae.unam.mx/Licenciatura2025/resultados/{i}5.html' for i in range(1,5)]  
    page_test = pages[0]
    
    df_area_scores = pd.DataFrame(columns=['id_aspirante', 'id_escuela','id_area', 'carrera', 'puntaje', 'acreditado'])
    driver = init_driver()
    area = 0
    if driver is not None:
        
        print(f'\n::::: Obteniendo datos de las carreras del área {1} :::::\n')
        main_content = get_main_content(driver, page_test)
        if main_content is not None:
            career_content = main_content.find_elements(by=By.CLASS_NAME, value='post-preview')
            df_area_scores = pd.concat([df_area_scores,
                                        get_scores_area(driver, career_content, area+1)],
                                        ignore_index=True)
            
        else:
            print(f'No main content found for {page_test}')
    else:
        print('Driver initialization failed')
    