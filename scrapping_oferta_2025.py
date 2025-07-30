
#%%
# import os 
import pandas as pd 
from bs4 import BeautifulSoup
from selenium import webdriver
from scrapping_puntaje import init_driver, get_main_content 
#%%

def get_oferta(url:str,driver_path: str = "C:/WebDrivers/chromedriver.exe") -> pd.DataFrame|None:
    if url is None:
        print('> URL no proporcionada.') 
        return None
    
    if not os.path.exists(driver_path):
        print(f'> No se encontró el driver en la ruta: {driver_path}')
        return None
    
    
    driver: webdriver = init_driver(driver_path)
    
    
    if driver is not None: 
        main_content = get_main_content(driver, url)
        print('> Accediendo a la página de oferta de lugares de la UNAM...')
        if main_content is not None:
            main_bs = BeautifulSoup(main_content.get_attribute('outerHTML'), 'html.parser')
            
            table_html = main_bs.find('table', {'id': 'table'})
            header_table = [th.text.strip() for th in table_html.find('thead').find_all('th')]
            
            table_data = table_html.find('tbody').find_all('tr')
            table_data = [[td.text.strip() for td in row.find_all('td')] for row in table_data] 
            
            df_oferta = pd.DataFrame(columns = header_table, data = table_data)
        
        else: 
            print('> No fue posible acceder al contenido principal de la página')
            return None
    else:
        print('> No se pudo iniciar el driver de Selenium')
        driver.quit()
        return None
    
    rename_cols = {'Área': 'area', 
                   'Clave': 'id_carrera',
                   'Plantel donde se imparte': 'plantel',
                   'Oferta Licenciatura 2025': 'oferta_2025',
                   'Oferta Licenciatura 2024': 'oferta_2024',
                   'Demanda Licenciatura 2024': 'demanda_2024',}
    
    df_oferta.rename(columns=rename_cols, inplace=True)
    df_oferta.columns = [col.lower() for col in df_oferta.columns]
    area_map = {'1': 'A1', '2': 'A2', '3': 'A3', '4': 'A4'}
    df_oferta['area'] = df_oferta['area'].map(area_map)
    
    print('> Extracción de datos completada.')
    driver.quit()
    return df_oferta
    

if __name__ == '__main__': 
    
    url = 'https://www.dgae.unam.mx/Licenciatura2025/oferta_lugares/oferta_licenciatura2025.html'
    print(f'::: Iniciando scrapping de oferta de lugares de la UNAM:::\n')
    data = get_oferta(url)
    
    print(f'::: Scrapping finalizado. Se encontraron {len(data)} registros de oferta de lugares :::\n')
    print(data.sample(7))
    
    
    os.makedirs('./datos/', exist_ok = True)
    
    data.to_csv('./datos/oferta_lugares_unam_2025_2024.csv', index=False)