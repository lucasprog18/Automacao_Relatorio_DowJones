import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

from config import (
    YAHOO_FINANCE_BASE_URL,
    DOW_JONES_TICKERS,
    SELECTOR_OPEN_PRICE,
    SELECTOR_VOLUME,
    SELECTOR_PREVIOUS_CLOSE
)

# Configura e retorna o WebDriver do Chrome.
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Roda o navegador em modo invisível (sem GUI)
    options.add_argument('--no-sandbox')  # Necessário para alguns ambientes Linux
    options.add_argument('--disable-dev-shm-usage') # Otimização para Docker/Linux
    options.add_argument('--log-level=3') # Suprime logs desnecessários do Chrome

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service = service, options = options)
    driver.set_page_load_timeout(30) # Aumenta o timeout para carregar a página
    return driver

def collect_stock_data(driver, ticker):
    """
    Coleta os dados de uma única ação a partir do Yahoo Finance.
    Retorna um dicionário com os dados ou None em caso de erro.
    """
    url = f"{YAHOO_FINANCE_BASE_URL}{ticker}"
    print(f'Coletando dados para: {ticker} em {url}')

    stock_data =  {
        'Ticker': ticker,
        'Open Price': None,
        'Previous Close': None,
        'Volume': None,
        'Status': 'Sucesso'
    }

    try:
        driver.get(url)

        try:
            
            close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Close"]')) # Tenta o botão de fechar genérico
            )
            close_button.click()
            print(f"DEBUG: Pop-up 'Upgrade Now' fechado para {ticker}")
            time.sleep(1) # Pequena pausa após fechar o pop-up
        except:
            # Se o botão de fechar não for encontrado ou não for clicável, apenas continua.
            # Isso é normal se o pop-up não apareceu.
            pass
        
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTOR_OPEN_PRICE)) 
        )
        time.sleep(3) # pausa extra para garantir carregamento dinâmico

        # Coletar cada dado usando os seletores
      
        
        try:
            open_price_element = driver.find_element(By.CSS_SELECTOR, SELECTOR_OPEN_PRICE)
            stock_data ['Open Price'] = open_price_element.text.strip()
        except Exception as e:
            stock_data ['Open Price'] = 'N/A'
            print(f'Erro ao coletar Preço de Abertura para {ticker}: {e}')

        
        try:
            volume_element = driver.find_element(By.CSS_SELECTOR, SELECTOR_VOLUME)
            stock_data ['Volume'] = volume_element.text.strip()
        except Exception as e:
            stock_data ['Volume'] = 'N/A'
            print(f'Erro ao coletar Volume para {ticker}: {e} ')


        try:
            previous_close_element = driver.find_element(By.CSS_SELECTOR, SELECTOR_PREVIOUS_CLOSE)
            stock_data ['Previous Close'] = previous_close_element.text.strip()
        except Exception as e:
            stock_data ['Previous Close'] = 'N/A'
            print(f'Erro ao coletar Fechamento Anterior para {ticker}: {e}')
        
        print(f"Dados de {ticker} coletados: Abertura={stock_data['Open Price']}, Fechamento Anterior={stock_data['Previous Close']}, Volume={stock_data['Volume']}")
        return stock_data
    
    except Exception as e:
        stock_data ['Status'] = f'Falha na página: {e}'
        print(f'Erro geral ao gerar ou processar {ticker}: {e}')
        return stock_data
    

def main():
    driver = None
    all_stocks_data = [] # Lista para armazenar os dicionários de dados de cada ação

    try:
        driver = setup_driver()
        print('WebDriver configurado com sucesso.')

        for ticker in DOW_JONES_TICKERS:
            data = collect_stock_data(driver, ticker)
            if data: # Adiciona apenas se houver dados (mesmo com N/A)
                all_stocks_data.append(data)
            time.sleep(1) # Pequena pausa entre as requisições para ser educado com o site

    except Exception as e:
        print(f'Ocorreu um erro crítico: {e}')
    
    finally:
        if driver:
            driver.quit()
            print('WebDriver encerrado.')


    # processar os dados coletados
    if all_stocks_data:
        column_order = ["Ticker", "Open Price", "Previous Close", "Volume", "Status"]
        df = pd.DataFrame(all_stocks_data, columns = column_order)
        print("\n--- Dados Coletados ---")
        print(df)

        # salvar em CSV
        output_filename = "dow_jones_stock_data_csv"
        df.to_csv(output_filename, index=False, encoding='utf-8')
        print(f'\nDados salvos em "{output_filename}"')

    else:
        print('\nNenhum dado foi coletado')


if __name__ == '__main__':
    main()


    






    









        