import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SENDER_EMAIL, SENDER_PASSWORD, SMTP_SERVER, SMTP_PORT

def send_email(recipient_email: str, subject: str, html_body: str, sender_email: str = SENDER_EMAIL, sender_password: str = SENDER_PASSWORD):
    """
    Envia um e-mail com conteúdo HTML.

    Args:
        recipient_email (str): O endereço de e-mail do destinatário.
        subject (str): O assunto do e-mail.
        html_body (str): O conteúdo HTML do corpo do e-mail.
        sender_email (str): O endereço de e-mail do remetente.
        sender_password (str): A senha (ou senha de app) do e-mail do remetente.
    """
    try:
        # Crie a mensagem multipart para suportar HTML
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Anexe a parte HTML
        part_html = MIMEText(html_body, 'html', 'utf-8')
        msg.attach(part_html)

        # Conecte-se ao servidor SMTP
        print(f"Conectando ao servidor SMTP: {SMTP_SERVER}:{SMTP_PORT}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls() # Inicia a criptografia TLS (Transport Layer Security)
        
        # Faça login na conta
        print(f"Tentando login com o usuário: {sender_email}...")
        server.login(sender_email, sender_password)
        print("Login bem-sucedido!")

        # Envie o e-mail
        print(f"Enviando e-mail para: {recipient_email}...")
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("E-mail enviado com sucesso!")

    except smtplib.SMTPAuthenticationError as e:
        print(f"Erro de autenticação SMTP. Verifique seu e-mail e senha (ou senha de app). Detalhes: {e}")
        print("Para Gmail, lembre-se de que pode ser necessário usar uma 'Senha de App'.")
    except smtplib.SMTPServerDisconnected as e:
        print(f"Erro: Servidor SMTP desconectado. Isso pode ser um problema de rede ou firewall. Detalhes: {e}")
    except Exception as e:
        print(f"Ocorreu um erro ao enviar o e-mail: {e}")
    finally:
        if 'server' in locals() and server:
            server.quit() # Encerre a conexão com o servidor SMTP

