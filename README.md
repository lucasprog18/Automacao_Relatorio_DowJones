# 📈 Automação de Relatórios Diários: Cotação das Ações do Índice Dow Jones no Seu Email

Este projeto nasceu de uma ideia simples, mas poderosa: **transformar o tempo gasto na busca por dados financeiros em produtividade real**. Imagine chegar à sua mesa todos os dias e encontrar um relatório conciso no seu e-mail, destacando as informações vitais do Dow Jones: **Preço de Abertura**, **Fechamento no Dia Anterior** (perfeito para comparação imediata) e o **Volume Negociado**. Uma ferramenta ágil e precisa, pensada para analistas e corretores que buscam otimizar seu tempo.

## ✅ Status do Projeto: Concluído e Automatizado!

Este projeto foi **completamente desenvolvido** para entregar um sistema de automação de relatórios de ações robusto e autônomo. Todas as fases do planejamento inicial foram concluídas com sucesso, resultando em uma ferramenta que opera de forma confiável diariamente.

## 🚀 Funcionalidades Chave Implementadas

O projeto oferece as seguintes funcionalidades principais:

1.  **Coleta de Dados Dinâmica:**
    * Utiliza `Selenium` e `WebDriver Manager` para interagir com o Yahoo Finance e extrair dados atualizados das 30 ações que compõem o Dow Jones Industrial Average.
    * Lida com a natureza dinâmica do site, garantindo a captura de informações cruciais como Preço de Abertura, Fechamento Anterior e Volume Negociado. Inclui tratamento para indisponibilidades momentâneas do site, notificando no relatório sem interromper a execução.

2.  **Processamento e Geração de Relatórios:**
    * Os dados coletados são estruturados e manipulados com `Pandas`, garantindo um formato limpo e organizado.
    * Gera relatórios detalhados em **formato HTML**, visualmente atraentes e fáceis de ler, que incluem todas as cotações do dia.

3.  **Envio Automatizado de E-mails:**
    * Integração com serviço de e-mail (`smtplib`, `email`) para enviar o relatório HTML diretamente para a caixa de entrada do usuário.
    * Configuração flexível do remetente e destinatário do e-mail, com assuntos personalizados para relatórios normais e alertas de falha.

4.  **Segurança e Organização:**
    * **Variáveis de Ambiente:** Credenciais sensíveis (como senha de e-mail) são gerenciadas com `python-dotenv`, garantindo que não sejam expostas no código-fonte e facilitando a configuração em diferentes ambientes.
    * **Estrutura de Pastas:** Os outputs (relatórios CSV e HTML) são salvos em uma pasta `output/` e os logs de execução em uma pasta `logs/`, mantendo o projeto limpo e organizado. Cada arquivo de log e relatório é nomeado com um timestamp para um histórico completo.
    * **`.gitignore`:** Configurado para ignorar arquivos temporários, de ambiente e de saída, mantendo o repositório Git limpo.

5.  **Automação Diária:**
    * Configurado para execução autônoma e diária via **Agendador de Tarefas do Windows**, garantindo que o relatório seja entregue pontualmente às 09:00.
    * A saída do script é redirecionada para arquivos de log na pasta `logs/`, permitindo o monitoramento de cada execução mesmo em background.

## 📚 Bibliotecas e Módulos Utilizados

Para tornar este projeto possível, foram utilizadas as seguintes bibliotecas e módulos Python:

* **Selenium:** Essencial para a automação do navegador e o web scraping dinâmico no Yahoo Finance.
* **WebDriver Manager:** Garante que o driver do navegador (como o ChromeDriver) esteja sempre atualizado e compatível.
* **Pandas:** Utilizada para a manipulação, análise e estruturação dos dados coletados, bem como para a exportação para CSV.
* **python-dotenv:** Usada para carregar variáveis de ambiente (como credenciais de e-mail) de um arquivo `.env`, garantindo a segurança e a flexibilidade das configurações.
* **smtplib (módulo padrão do Python):** Para o envio de e-mails utilizando o protocolo SMTP.
* **email (módulo padrão do Python, com submódulos como `email.mime.multipart`, `email.mime.text`):** Utilizado para a criação e formatação de mensagens de e-mail complexas, incluindo conteúdo HTML e anexos.
* **datetime (módulo padrão do Python):** Para manipulação de datas e horas, essencial na geração de timestamps únicos para os arquivos de log e de saída.
* **os (módulo padrão do Python):** Usado para interagir com o sistema operacional, como acessar variáveis de ambiente e manipular caminhos de arquivo.

## 💡 Abordagem Didática e Arquitetura do Projeto (Portfólio)

Este projeto foi construído não apenas para ser funcional, mas também para servir como uma **peça didática em meu portfólio**, demonstrando compreensão sobre boas práticas de engenharia de software e design de sistemas.

* **`scrapers/` (pastas `dynamic_scraper.py`, `static_scraper.py`):**
    * Embora a lógica de scraping esteja centralizada no `main.py` para este MVP, os módulos `dynamic_scraper.py` e `static_scraper.py` foram criados como placeholders conceituais. Eles ilustram o entendimento sobre a modularização de diferentes estratégias de scraping (dinâmico vs. estático) para futura escalabilidade e organização.
* **`tests/` (pasta `info.py`):**
    * A pasta `tests/` inclui um arquivo informativo (`info.py`) explicando que, apesar dos testes manuais durante o desenvolvimento, a implementação de uma suíte de testes automatizados com `pytest` será explorada em um projeto de portfólio dedicado a testes. Isso demonstra a consciência sobre a importância da garantia de qualidade via automação e a intenção de aprofundar nessa área.
* **`concurrent_collector.py`:**
    * Este arquivo é um placeholder conceitual para a implementação de lógicas de coleta concorrente (ex: `multithreading`, `asyncio`). Embora não essencial para o volume de dados atual, sua presença indica a visão para otimização de performance e escalabilidade em cenários com maior volume de dados ou maior número de fontes.
* **`data_models.py`:**
    * Este módulo define modelos de dados utilizando `dataclasses`. Embora a tipagem formal não fosse estritamente "essencial" para a complexidade deste MVP, sua inclusão demonstra o entendimento da importância da consistência de dados, tipagem e padrões de projeto para a qualidade e manutenibilidade de projetos de software maiores e mais complexos. Serve como base para futuras expansões que envolvam análise de dados, persistência em banco de dados ou integração com outras APIs.

## ⚙️ Como Configurar e Rodar o Projeto

### Pré-requisitos:

* Python 3.x instalado.
* Um navegador (ex: Google Chrome) instalado.

### Passos:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/](https://github.com/)lucasprog18/https://github.com/lucasprog18/Automacao_Relatorio_DowJones
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure suas credenciais de e-mail (Segurança):**
    * Crie um arquivo chamado `.env` na **raiz do projeto**.
    * Adicione suas credenciais de e-mail (usando senha de aplicativo para Gmail, por exemplo):
        ```env
        SMTP_EMAIL="seu.email@gmail.com"
        SMTP_PASSWORD="sua_senha_de_app"
        ```
    * **IMPORTANTE:** O arquivo `.env` já está configurado no `.gitignore` para não ser versionado.

5.  **Crie as pastas de saída:**
    * Crie manualmente as pastas `logs/` e `output/` na raiz do projeto.

6.  **Execute o script manualmente (para teste):**
    * **No Terminal PowerShell:**
        ```powershell
        powershell.exe -Command "C:\Caminho\Completo\Para\Seu\Projeto\venv\Scripts\python.exe C:\Caminho\Completo\Para\Seu\Projeto\main.py > C:\Caminho\Completo\Para\Seu\Projeto\logs\app_$(Get-Date -Format \"yyyyMMdd_HHmmss\").log 2>&1"
        ```
        *(Substitua `C:\Caminho\Completo\Para\Seu\Projeto` pelo caminho real da raiz do seu projeto)*
    * Verifique sua caixa de entrada e as pastas `logs/` e `output/`.

7.  **Configure a Automação Diária (Windows):**
    * Abra o **Agendador de Tarefas** (pesquise no Menu Iniciar).
    * Clique em "Criar Tarefa Básica..." e siga o assistente:
        * **Nome:** `Relatório Diário de Ações Dow Jones`
        * **Gatilho:** `Diariamente`, configurando o horário desejado (ex: `09:00:00`).
        * **Ação:** `Iniciar um programa`
        * **Programa/script:** `powershell.exe`
        * **Adicionar argumentos (opcional):**
            ```
            -Command "C:\Caminho\Completo\Para\Seu\Projeto\venv\Scripts\python.exe C:\Caminho\Completo\Para\Seu\Projeto\main.py > C:\Caminho\Completo\Para\Seu\Projeto\logs\app_$(Get-Date -Format \"yyyyMMdd_HHmmss\").log 2>&1"
            ```
            *(Substitua `C:\Caminho\Completo\Para\Seu\Projeto` pelo caminho real da raiz do seu projeto)*
        * **Iniciar em (opcional):** `C:\Caminho\Completo\Para\Seu\Projeto\`
            *(Substitua pelo caminho real da raiz do seu projeto)*
    * Revise e conclua a configuração.