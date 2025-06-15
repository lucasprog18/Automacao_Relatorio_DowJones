import pandas as pd
import datetime # Para usar a data atual no rodapé do relatório

def generate_html_report(df: pd.DataFrame) -> str:
    """
    Gera um relatório HTML a partir de um DataFrame Pandas,
    com um cabeçalho, corpo do e-mail e estilo básico para a tabela.

    Args:
        df (pd.DataFrame): O DataFrame contendo os dados das ações.

    Returns:
        str: Uma string HTML completa contendo o relatório, pronta para ser embutida em um e-mail.
    """
    today_date_str = datetime.date.today().strftime("%d/%m/%Y")

    if df.empty:
        # Mensagem mais amigável para relatório vazio
        return """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Relatório Diário de Ações - Dow Jones</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
                .container { max-width: 700px; margin: auto; background-color: #ffffff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); text-align: center; }
                h2 { color: #e74c3c; }
                p { font-size: 1.1em; }
                .footer { margin-top: 30px; font-size: 0.8em; color: #777; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Ops! Algo deu errado.</h2>
                <p>Não foi possível coletar os dados das ações do Dow Jones para hoje.</p>
                <p>Por favor, tente novamente mais tarde ou verifique a conexão.</p>
                <div class="footer">
                    <p>Relatório gerado em: {datetime.date.today().strftime('%d/%m/%Y')}</p>
                    <p>&copy; {datetime.datetime.now().year} Automação de Relatórios Dow Jones.</p>
                </div>
            </div>
        </body>
        </html>
        """

    # Converte o DataFrame para HTML
    # index=False: não mostra o índice do DataFrame como coluna
    # border=0: remove a borda padrão do HTML
    # classes='styled-table': adiciona uma classe CSS para estilização
    html_table = df.to_html(index=False, border=0, classes='styled-table')

    # Define o estilo CSS para a tabela e o corpo do e-mail
    css_style = """
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; color: #333; }
        .email-body { max-width: 800px; margin: 20px auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
        h2 { color: #2c3e50; text-align: center; margin-bottom: 25px; }
        p { line-height: 1.6; margin-bottom: 10px; }
        .styled-table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.9em;
            min-width: 400px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            border-radius: 8px;
            overflow: hidden; /* Garante que bordas arredondadas funcionem */
        }
        .styled-table thead tr {
            background-color: #007bff; /* Azul, cor comum para relatórios */
            color: #ffffff;
            text-align: left;
        }
        .styled-table th,
        .styled-table td {
            padding: 12px 15px;
            border: 1px solid #dddddd; /* Bordas suaves */
        }
        .styled-table tbody tr {
            border-bottom: 1px solid #dddddd;
        }
        .styled-table tbody tr:nth-of-type(even) {
            background-color: #f8f8f8; /* Linhas alternadas para legibilidade */
        }
        .styled-table tbody tr:last-of-type {
            border-bottom: 2px solid #007bff;
        }
        .footer { text-align: center; margin-top: 30px; font-size: 0.8em; color: #777; border-top: 1px solid #eee; padding-top: 15px; }
    </style>
    """

    # Monta o HTML completo do relatório
    html_report = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório Diário de Ações - Dow Jones - {today_date_str}</title> 
        {css_style}
    </head>
    <body>
        <div class="email-body">
            <h2>Relatório Diário de Cotações - Dow Jones ({today_date_str})</h2>
            <p>Prezado(a) Analista/Corretor(a),</p>
            <p>Conforme solicitado, segue o relatório diário das cotações das ações do índice Dow Jones Industrial Average, com dados atualizados de **Preço de Abertura**, **Fechamento Anterior** e **Volume Negociado**.</p>
            {html_table}
            <p>Esperamos que estas informações auxiliem em suas análises e decisões diárias.</p>
            <p>Atenciosamente,</p>
            <p>Sua Equipe de Automação de Mercado</p>
            <div class="footer">
                <p>Este relatório foi gerado automaticamente em: {today_date_str}</p> 
                <p>&copy; {datetime.datetime.now().year} Automação de Relatórios Dow Jones. Todos os direitos reservados.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_report

