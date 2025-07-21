#%%
import pandas as pd 
import time
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 


#%%
def init_driver(driver_path: str = "C:/WebDrivers/chromedriver.exe") -> webdriver.Chrome:
    try:
        driver = webdriver.Chrome(service = Service(driver_path))
    except Exception as e:
        print(f"Error initializing the driver: {e}")
        return None
    return driver


def get_main_content(driver: webdriver.Chrome, url: str) -> webdriver.Chrome:
    try:
        driver.get(url)
        main_content = driver.find_element(by = By.TAG_NAME, value='main')
    except Exception as e:
        print(f"Cannot get main content from {url}: {e}")
        return None

    return main_content

def get_scores_from_school(scores_table: webdriver.Chrome, school_name: str, career_name: str) -> pd.DataFrame:
    
    id_list: list[str] = []
    score_list: list[str | int] = []
    accepted_list: list[str] = []
    
    acreditado_dict: dict = {
                'S': 'Seleccionado',
                '': 'No seleccionado',
                'C': 'Cancelado',
                'N': 'No presentado'
            }
    
    try: 
        rows = scores_table.find_elements(by = By.TAG_NAME, value = 'tr')
        for row in rows:  
            cells = row.find_elements(by = By.TAG_NAME, value = 'td')
            id_list.append(cells[0].text)
            score_list.append(cells[1].text)
            accepted_list.append(acreditado_dict[cells[2].text])
        
        career_list: str = [career_name] * len(id_list)
        school_list: str = [school_name] * len(id_list)
        
        data: dict = {
            'id_aspirante': id_list,
            'escuela': school_list,
            'carrera': career_list,
            'puntaje': score_list,
            'acreditado': accepted_list
        }
        
        return pd.DataFrame(data)

    except Exception as e:
        print(f"Error processing scores table: {e}")
        return pd.DataFrame(columns=['id_aspirante', 'escuela', 'carrera', 'puntaje', 'acreditado'])


def get_scores_career(driver: webdriver.Chrome, schools: webdriver.Chrome, career_name: str) -> pd.DataFrame:
    df_career_scores = pd.DataFrame(columns=['id_aspirante', 'escuela', 'carrera', 'puntaje', 'acreditado'])
    try:
        for school in schools:
            print(f"Processing school: {school.text}")
            
            school_name = school.text
            school.click()
            
            df = get_scores_from_school(driver.find_element(by = By.TAG_NAME, value='tbody'),
                                        school_name, career_name)
            
            df_career_scores = pd.concat([df_career_scores, df], ignore_index=True)
            driver.back() # go back to A1 list
    except Exception as e: 
        print(f"Error processing career {career_name}: {e}")
        return df_career_scores
    return df_career_scores
    
    
    


    
#%%

if __name__ == "__main__":

    pages = [f'https://www.dgae.unam.mx/Licenciatura2025/resultados/{i}5.html' for i in range(1,5)]    
    driver = init_driver()
    
    
    if driver is not None:
        main_content = get_main_content(driver, pages[0])
        if main_content is not None:
            career_content = main_content.find_elements(by=By.CLASS_NAME, value='post-preview')[0]
            career_name = career_content.find_element(by=By.TAG_NAME, value='h3').text                    
            schools = career_content.find_elements(by=By.TAG_NAME, value='a')
            
            df_career_scores = get_scores_career(driver, schools, career_name)
            
        else: 
            print('No main content found')
    else: 
        print('Driver initialization failed')


    print(df_career_scores.sample(7))
#%%
    driver.quit()
