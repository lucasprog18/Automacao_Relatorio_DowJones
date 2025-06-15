import time
import datetime # Importar datetime para obter a data atual
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

from report_generator import generate_html_report
from email_sender import send_email


from config import (
    YAHOO_FINANCE_BASE_URL,
    DOW_JONES_TICKERS,
    SELECTOR_OPEN_PRICE,
    SELECTOR_VOLUME,
    SELECTOR_PREVIOUS_CLOSE,
    RECIPIENT_EMAIL,
    SENDER_EMAIL,
    EMAIL_SUBJECT,
    ALERT_EMAIL_SUBJECT 
)

# Configura e retorna o WebDriver do Chrome.
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Roda o navegador em modo invisível (sem GUI)
    options.add_argument('--no-sandbox')   # Necessário para alguns ambientes Linux
    options.add_argument('--disable-dev-shm-usage') # Otimização para Docker/Linux
    options.add_argument('--log-level=3') # Suprime logs desnecessários do Chrome
    options.add_argument('--disable-gpu') # Adicionado para compatibilidade em alguns sistemas (boa prática)

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

    stock_data = {
        'Ticker': ticker,
        'Open Price': None,
        'Previous Close': None,
        'Volume': None,
        'Status': 'Falha' # Começa com Falha, muda para Sucesso se tudo der certo
    }

    try:
        driver.get(url)

        # Tentativa de fechar pop-up "Upgrade Now" ou "Consentimento de Cookies"
        try:
            # Tenta múltiplos seletores comuns para fechar pop-ups
            close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Close"]')) or
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-cmp-button="close"]')) or
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Não aceito')]")) or # Exemplo para "Não aceito"
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Recusar tudo')]")) # Exemplo para "Recusar tudo"
            )
            close_button.click()
            print(f"DEBUG: Pop-up fechado para {ticker}")
            time.sleep(1) # Pequena pausa após fechar o pop-up
        except Exception as e:
            # print(f"DEBUG: Nenhum pop-up para fechar ou erro ao fechar para {ticker}: {e}") # Descomente para depurar
            pass # Se o pop-up não aparecer ou o botão não for clicável, apenas continua.

        # Espera até que o elemento de preço de abertura esteja visível
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTOR_OPEN_PRICE))
        )
        time.sleep(3) # pausa extra para garantir carregamento dinâmico

        # Coletar cada dado usando os seletores
        try:
            open_price_element = driver.find_element(By.CSS_SELECTOR, SELECTOR_OPEN_PRICE)
            stock_data['Open Price'] = open_price_element.text.strip()
        except Exception as e:
            stock_data['Open Price'] = 'N/A'
            print(f'Erro ao coletar Preço de Abertura para {ticker}: {e}')

        try:
            volume_element = driver.find_element(By.CSS_SELECTOR, SELECTOR_VOLUME)
            stock_data['Volume'] = volume_element.text.strip()
        except Exception as e:
            stock_data['Volume'] = 'N/A'
            print(f'Erro ao coletar Volume para {ticker}: {e}')

        try:
            previous_close_element = driver.find_element(By.CSS_SELECTOR, SELECTOR_PREVIOUS_CLOSE)
            stock_data['Previous Close'] = previous_close_element.text.strip()
        except Exception as e:
            stock_data['Previous Close'] = 'N/A'
            print(f'Erro ao coletar Fechamento Anterior para {ticker}: {e}')

        # Define o status baseado na coleta principal (Preço de Abertura e Fechamento Anterior)
        # Se algum dos campos cruciais (Open/Previous Close) for N/A, é considerado falha para fins de repetição.
        if stock_data['Open Price'] != 'N/A' and stock_data['Previous Close'] != 'N/A':
            stock_data['Status'] = 'Sucesso'
        else:
            stock_data['Status'] = 'Falha - Dados Parciais' # Indica que coletou, mas com falhas críticas para a repetição

        print(f"Dados de {ticker} coletados: Abertura={stock_data['Open Price']}, Fechamento Anterior={stock_data['Previous Close']}, Volume={stock_data['Volume']} - Status: {stock_data['Status']}")
        return stock_data

    except Exception as e:
        stock_data['Status'] = f'Falha na página/processamento: {e}'
        print(f'Erro geral ao coletar dados para {ticker}: {e}')
        return stock_data

def run_scraper_process(max_retries=3):
    """
    Executa o processo de scraping completo e retorna o DataFrame final.
    Tenta repetir o scraping até que todas as ações tenham status 'Sucesso' ou atinja max_retries.
    """
    driver = None
    attempt = 0
    df = pd.DataFrame() # Inicializa um DataFrame vazio
    
    while attempt < max_retries:
        attempt += 1
        print(f"\n--- Tentativa de Coleta de Dados: {attempt}/{max_retries} ---")
        all_stocks_data = []

        try:
            driver = setup_driver()
            print('WebDriver configurado com sucesso.')

            for ticker in DOW_JONES_TICKERS:
                data = collect_stock_data(driver, ticker)
                all_stocks_data.append(data)
                time.sleep(1) # Pequena pausa entre as requisições

        except Exception as e:
            print(f'Ocorreu um erro crítico durante a configuração ou coleta: {e}')
        
        finally:
            if driver:
                driver.quit()
                print('WebDriver encerrado.')

        if all_stocks_data:
            column_order = ["Ticker", "Open Price", "Previous Close", "Volume", "Status"]
            df = pd.DataFrame(all_stocks_data, columns=column_order)
            print("\n--- Dados Coletados na Tentativa Atual ---")
            print(df)

            # Verificar se todas as ações tiveram 'Sucesso' (nenhuma 'Falha' ou 'Falha - Dados Parciais')
            if all(df['Status'] == 'Sucesso'):
                print("\nTodas as ações foram coletadas com sucesso. Processo de coleta concluído.")
                return df # Retorna o DataFrame para prosseguir
            else:
                failed_tickers = df[df['Status'] != 'Sucesso']['Ticker'].tolist()
                print(f"\nAlgumas ações falharam na coleta ({', '.join(failed_tickers)}). Tentando novamente...")
                time.sleep(5) # Pausa antes de repetir para evitar bloqueios ou sobrecarga
        else:
            print("\nNenhum dado foi coletado nesta tentativa.")
            time.sleep(5) # Pausa mesmo se nada foi coletado

    print(f"\nNúmero máximo de tentativas ({max_retries}) atingido. Prosseguindo com os dados disponíveis (podem conter falhas).")
    return df # Retorna o DataFrame com os melhores dados obtidos (pode conter falhas)


def main():
    final_df = pd.DataFrame()
    html_report_content = None

    MAX_SCRAPER_RETRIES = 3 

    # Executa o processo de scraping com retries
    final_df = run_scraper_process(max_retries=MAX_SCRAPER_RETRIES)

    today_date = datetime.date.today().strftime("%d/%m/%Y") # Formato DD/MM/AAAA
    full_email_subject = f"{EMAIL_SUBJECT} - {today_date}"

    # REESTRUTURANDO O BLOCO IF/ELSE PARA GARANTIR APENAS UM CAMINHO (SUCESSO OU FALHA)
    # Se final_df NÃO ESTÁ vazio E TODAS as ações têm status 'Sucesso', envia o relatório principal.
    if not final_df.empty and all(final_df['Status'] == 'Sucesso'):
        # --- BLOCO DE SUCESSO: Envia o relatório principal ---
        # Remover a coluna 'Status' para o relatório final e CSV
        df_report = final_df.drop(columns=['Status'], errors='ignore')

        # Salvar em CSV
        output_filename = "dow_jones_stock_data_csv"
        df_report.to_csv(output_filename, index=False, encoding='utf-8')
        print(f'\nDados salvos em "{output_filename}"')

        # Geração do relatório HTML (passando o df_report sem a coluna Status)
        print("\nGerando relatório HTML para envio...")
        html_report_content = generate_html_report(df_report)
        print("Relatório HTML gerado!")

        if html_report_content:
            print(f"Iniciando envio do relatório para {RECIPIENT_EMAIL} com o assunto: '{full_email_subject}'...")
            send_email(RECIPIENT_EMAIL, full_email_subject, html_report_content)
        else:
            print("Não foi possível gerar o conteúdo do relatório HTML. E-mail principal não enviado.")

    else: # <<< ESTE 'else' agora é diretamente associado ao 'if' acima.
          # --- BLOCO DE FALHA: Envia o e-mail de alerta ---
        print('\n--- Falha Crítica na Coleta de Dados ---')
        if final_df.empty:
            alert_message = f"O script não conseguiu coletar NENHUM dado para o Dow Jones após {MAX_SCRAPER_RETRIES} tentativas em {today_date}."
            print(alert_message)
        else:
            failed_tickers = final_df[final_df['Status'] != 'Sucesso']['Ticker'].tolist()
            alert_message = (
                f"O script não conseguiu coletar dados completos para todas as ações do Dow Jones "
                f"após {MAX_SCRAPER_RETRIES} tentativas em {today_date}.\n\n"
                f"As seguintes ações falharam ou tiveram dados parciais: {', '.join(failed_tickers)}.\n"
                f"O relatório principal NÃO foi enviado."
            )
            print(alert_message)
            print("\nÚltimo DataFrame coletado (com falhas):")
            print(final_df) # Mostra o DF com os status das falhas

        # Conteúdo do e-mail de alerta (HTML básico)
        alert_html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f8f8f8; color: #333; }}
                .container {{ max-width: 600px; margin: 20px auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); border-left: 5px solid #dc3545; /* Cor vermelha para alerta */ }}
                h2 {{ color: #dc3545; text-align: center; }}
                p {{ line-height: 1.5; }}
                .footer {{ margin-top: 20px; font-size: 0.8em; color: #777; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Alerta de Falha na Automação - Dow Jones</h2>
                <p>Prezado(a) Remetente,</p>
                <p>{alert_message.replace('\n', '<br>')}</p>
                <p>Por favor, verifique os logs do script para mais detalhes.</p>
                <div class="footer">
                    <p>Este é um e-mail de alerta automático gerado em {today_date}.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        print(f"Enviando e-mail de alerta para {SENDER_EMAIL} (seu próprio email) com o assunto: '{ALERT_EMAIL_SUBJECT}'...")
        send_email(SENDER_EMAIL, ALERT_EMAIL_SUBJECT, alert_html_body)

if __name__ == '__main__':
    main()