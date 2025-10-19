from time import sleep
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

planilha = "1Ox8O0pMcPJqWB22znkzoM-_H4kVuDf91b4yVg9RApNk"
pagina_planilha = "Login gerencial!A3:C"

def fazer_login():
    login = input('Operador Gerente:')
    senha = input('Senha: ')
    return (login, senha)

def buscar_usuario(login, senha):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credenciais.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=planilha, range=pagina_planilha)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("Sem dados encontrados.")
            return

        for row in values:
            nome = row[0]
            password = row[1]
            if login == nome and senha == password:
                return True

    except HttpError as err:
        print('erros')
        print(err)

login, senha = fazer_login()
user = buscar_usuario(login,senha)
if user == True:
    print('Login realizado com sucesso pelo gerente!')
    sleep(2)
else:
    print('Invalido')

