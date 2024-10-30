# Importação das bibliotecas necessárias para o envio de e-mails
import smtplib  # Para estabelecer uma conexão SMTP e enviar e-mails
from email.mime.text import MIMEText  # Para criar o corpo do e-mail no formato de texto

# Definições do remetente e senha do e-mail (considerar usar variáveis de ambiente para segurança)
sender = "testeps2fase@gmail.com"  # Endereço de e-mail do remetente
password = "lhhs xpdi bhhm ywek"  # Senha do e-mail do remetente (deveria ser mantida em segredo)

def send_email(senha_enviar, recebedor):
    """
    Envia um e-mail de confirmação de inscrição com a senha do usuário.

    Args:
        senha_enviar (str): A senha que será enviada ao usuário.
        recebedor (str): O endereço de e-mail do destinatário.

    Raises:
        Exception: Se ocorrer um erro ao enviar o e-mail.
    
    Prints:
        str: Mensagem indicando que o e-mail foi enviado com sucesso.
    """
    # Corpo do e-mail, que inclui uma mensagem de confirmação e a senha do usuário
    body = f"Se você está recebendo esse email significa que você foi cadastrado na plataforma do Cursinho Insper. Segue aqui a sua senha: {senha_enviar}"
    
    # Criação do objeto MIMEText para o corpo do e-mail
    msg = MIMEText(body)
    msg['Subject'] = "Cursinho Insper - Confirmação de Inscrição"  # Assunto do e-mail
    msg['From'] = sender  # Remetente do e-mail
    msg['To'] = recebedor  # Destinatário do e-mail
    
    # Estabelece uma conexão segura com o servidor SMTP do Gmail e envia o e-mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)  # Faz login com as credenciais do remetente
        smtp_server.sendmail(sender, recebedor, msg.as_string())  # Envia o e-mail
    
    print("Message sent!")  # Confirmação de que a mensagem foi enviada
