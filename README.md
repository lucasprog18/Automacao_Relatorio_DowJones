# 📈 Automação de Relatórios Diários: Cotação das Ações do Índice Dow Jones no Seu Email

Este projeto nasceu de uma ideia simples, mas poderosa: **transformar o tempo gasto na busca por dados financeiros em produtividade real**. Imagine chegar à sua mesa todos os dias e encontrar um relatório conciso no seu e-mail, destacando as informações vitais do Dow Jones: **Preço de Abertura**, **Fechamento no Dia Anterior** (perfeito para comparação imediata) e o **Volume Negociado**. Uma ferramenta ágil e precisa, pensada para analistas e corretores que buscam otimizar seu tempo.

## ✅ Status do Projeto: Fase Essencial Concluída!

Estamos prontos para a próxima etapa! A fase de estruturação e testes fundamentais foi concluída com sucesso:

* 🎯 **Design e Estrutura:** A arquitetura do projeto está sólida e bem definida, pronta para expansões futuras.
* 🎯 **30 Ações Coletadas:** A coleta de dados das principais ações do Dow Jones agora está a um clique de distância, funcionando de forma eficiente e confiável.
* 🎯 **Dados Estruturados e Prontos:** Todas as informações coletadas são entregues em um formato limpo e organizado, perfeito para a próxima fase: o envio direto para o seu e-mail.

## 🚀 Próximos Passos (Nosso Roadmap)

O futuro deste projeto promete ainda mais automação e valor. Nosso planejamento detalhado (`PLANNING.md`) guia as próximas fases, que incluem:

* **Geração de Relatórios:** Transformar os dados em relatórios visuais e fáceis de ler.
* **Envio Automatizado de E-mails:** Integrar o sistema para que os relatórios cheguem à sua caixa de entrada diariamente.
* **Agendamento da Execução:** Configurar a ferramenta para rodar de forma totalmente autônoma, todos os dias.
* **Robustez e Monitoramento:** Adicionar camadas de segurança e logs para garantir que a automação funcione sem falhas e avisar caso algo saia do planejado.

## 📚 Bibliotecas Utilizadas (Nesta Primeira Fase)

Para tornar tudo isso possível, contei com as seguintes ferramentas Python:

* **Selenium:** O motor da automação web, essencial para interagir com o Yahoo Finance.
* **WebDriver Manager:** Garantindo que o driver do navegador esteja sempre atualizado e compatível.
* **Pandas:** Minha escolha para organizar e manipular os dados coletados de forma eficiente.

## 🚀 MVP (Produto Mínimo Viável) em Ação!

O projeto já entrega um valor tangível! Atualmente, você pode rodar o MVP e obter um arquivo **CSV completo com as cotações das 30 ações do Dow Jones.**

### Como Rodar o MVP:

1.  **Clone o projeto:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd AUTOMACAO_RELATORIO_ACOES_DJIA
    ```
2.  **Configure seu ambiente:** (Altamente recomendado usar um ambiente virtual)
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
4.  **Execute o script principal:**
    ```bash
    python main.py
    ```
    Após a execução, um arquivo CSV (`dow_jones_stock_data_csv`) será gerado na raiz do projeto com os dados coletados.

---