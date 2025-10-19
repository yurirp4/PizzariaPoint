import time
import tkinter.messagebox

import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from datetime import datetime
from time import sleep
import os
import sys
import os.path
import customtkinter
from CTkListbox import *

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

janela = ctk.CTk()
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

planilha = "sua senha"
pagina_planilha = "Login gerencial!A3:C"

def press_enter(event):
    MenuGerenteLogin.tela_login()
class MenuGerenteLogin():
    def __init__(self):
        self.janela = janela
        self.tela_login_state = False
        self.tema()
        self.tela()
        self.tela_login()
        self.relogio()
        self.operador = ''
        self.senha = ''
        self.gerente = ''
        self.funcionario_name = ''
        self.funcionario_operador_state = False
        self.comanda_ativa = False
        self.lista_pratos = ["(1) - Pizza [R$26,90]", "(2) - Beirute[R$19,90]", "(3) - X-tudo[R$5,50]",
                             "(4) - Batata-Frita[R$3,00]", "(5) - Coca-Cola 2 Litros[R$8,50]",
                             "(6) - Coca-Cola 1 Litro[R$5,25]"]
        self.caches_produtos = {"Pizza": 0, "Beirute": 0, "X-tudo": 0, "Batata-Frita": 0, "cocacola2": 0,
                                'cocacola1': 0}
        self.total = 0

        janela.mainloop()
    def tema(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')
    def tela(self):
        self.janela.geometry("700x400")
        self.janela.resizable(1,  1)
        self.janela.title("Point Restaurante - Login Gerencial")
        self.janela.iconbitmap('pizza.ico')
        self.janela.resizable(width=False, height=False)
    def tela_abre_operador(self):
        self.button_abreoperador.destroy()
        self.relatorio_gerencial.destroy()
        self.button_volta.destroy()
        self.button_logout.destroy()
        self.janela.title('Poi')

        self.entry_operador_funcionario = ctk.CTkEntry(placeholder_text='Digite o operador do funcionario',master=self.janela, justify='center',width=300,font=('ROBOTO BOLD', 14))
        self.entry_operador_funcionario.place(x=200,y=85)

        self.button_logar_operador = ctk.CTkButton(master=janela,text='Abrir Caixa',command= lambda: self.caixa_aberto(),fg_color='#10CB3D',hover_color='#18D80F',width=90,font=('ROBOTO BOLD', 14))
        self.button_logar_operador.place(x=200,y=120)

        self.button_cadastra_operador = ctk.CTkButton(master=janela, text='Cadastrar', width=90,
                                                      command=lambda: self.cadastrar_operador(),
                                                      font=('ROBOTO BOLD', 14))
        self.button_cadastra_operador.place(x=300, y=120)

        self.button_cancelar_operador = ctk.CTkButton(master=janela, text='Cancelar', width=90,command= lambda : self.tela_suceeso(),
                                                   font=('ROBOTO BOLD', 14),fg_color='#CD2626',hover_color='#F81111')
        self.button_cancelar_operador.place(x=400, y=120)

    def tela_login(self):
        self.img = ctk.CTkImage(Image.open('logo.png'),size=(350, 400))
        self.imagem = ctk.CTkLabel(self.janela, text='',image=self.img)
        self.imagem.place(x=4,y=5)
        self.frm = ctk.CTkFrame(master=self.janela, width=350,height=396)
        self.frm.pack(side=RIGHT)

        self.label = ctk.CTkLabel(master=self.frm, text='     Seja Bem-Vindo', font=('ROBOTO BOLD', 30))
        self.label.place(x=25,y=25)

        self.label2 = ctk.CTkLabel(master=self.frm, text='Faça o login para realizar a abertura do caixa', font=('ROBOTO BOLD UI',16))
        self.label2.place(x=25,y=90)


        self.operador_entry = ctk.CTkEntry(master=self.frm,  justify='center',placeholder_text='Digite seu Operador', width=300,font=('ROBOTO BOLD', 14))
        self.operador_entry.place(x=25,y=140)


        self.senha_entry = ctk.CTkEntry(master=self.frm, justify='center',placeholder_text='Digite sua senha', show="*",width=300,font=('ROBOTO BOLD', 14))
        self.senha_entry.place(x=25,y=180)

       # but1 = ctk.CTkButton(master=self.frm, text='LOGIN',senha=str(senha_entry.get())),width=300).place(x=25,y=220)
        self.but1 = ctk.CTkButton(master=self.frm,text='LOGIN',command=lambda : self.fazer_login(),width=300,hover_color='#108AF7')
        self.but1.place(x=25,y=220)
        self.label3 = ctk.CTkLabel(master=self.frm, text=f'-', font=('Roboto', 20))
        self.label3.place(x=80,y=280)
        #self.janela.bind('<Return>', self.fazer_login())
    def relogio(self):
        if  self.tela_login_state == False:
            relo = datetime.now()
            horaatual = relo.strftime('%H:%M:%S | %d/%m/%y')
            janela.after(1000, self.relogio)
            self.label3.configure(text=horaatual)
        else:
            pass
    def ewroon(self):
        self.but1.place(x=25,y=240)
        self.but1.configure(fg_color='#F33A0D')
        self.label4 = ctk.CTkLabel(master=self.frm, text_color='#BB2E0C',text='* Dados incorretos',
                                   font=('ROBOTO BOLD', 12))
        self.label4.place(x=25, y=210)
        self.operador_entry.delete(0, 'end')
        self.senha_entry.delete(0,'end')

    def cadastrar_operador_final(self):

        if self.entry_operador_funcionario.get() == '' or self.entry_cadastro_name.get() == '':
            self.messagem_erro_cadastro = ctk.CTkLabel(master=self.janela, text='*Dados incorretos!',
                                                      font=('ROBOTO BOLD', 14))
            self.messagem_erro_cadastro.place(y=150,x=200)
            self.button_cadastra_operador.place(y=180)
            self.button_cancelar_operador.place(y=180)
            self.button_logar_operador.place(y=180)
            self.entry_cadastro_name.delete(0, 'end')
            self.entry_operador_funcionario.delete(0, 'end')
        elif self.entry_operador_funcionario.get().isalpha() or len(self.entry_operador_funcionario.get()) > 8 or len(self.entry_cadastro_name.get()) > 50 or self.entry_cadastro_name.get().isnumeric():
            self.messagem_erro_cadastro = ctk.CTkLabel(master=self.janela, text='Por favor preencha corretamente!',
                                                      font=('ROBOTO BOLD', 14))
            self.entry_cadastro_name.delete(0, 'end')
            self.entry_operador_funcionario.delete(0, 'end')
            self.messagem_erro_cadastro.place(y=150, x=200)
            self.button_cadastra_operador.place(y=180)
            self.button_cancelar_operador.place(y=180)
            self.button_logar_operador.place(y=180)
        else:
            try:
                funcionarios = []
                with open('funcionarios.txt', 'a+', encoding='Utf-8', newline='') as arquivo:
                    arquivo.writelines(f'{self.entry_operador_funcionario.get()},{self.entry_cadastro_name.get()}\n')
                    print('cadastro aprovado')
            except FileNotFoundError:
                open('funcionarios.txt', 'w+')
                funcionarios = []
                with open('funcionarios.txt', 'a+', encoding='Utf-8', newline='') as arquivo:
                    arquivo.writelines(f'{self.entry_operador_funcionario.get()},{self.entry_cadastro_name.get()}\n')
                    print('cadastro aprovado')
            self.entry_cadastro_name.destroy()
            try:
                self.messagem_erro_cadastro.destroy()
            except:
                pass
            self.button_cadastra_operador.place(y=120)
            self.button_cancelar_operador.place(y=120)
            self.button_logar_operador.place(y=120)
            self.button_cadastra_operador.configure(command=lambda: self.cadastrar_operador())
            self.messagem_sucesso_cadastro = tkinter.messagebox.showinfo(title='Cadastro Realizado!',message='Cadastro concluido com sucesso!')
    def cadastrar_operador(self):
        try:
            self.messagem_erro_cadastro.destroy()
        except:
            pass
        self.button_cadastra_operador.place(y=150)
        self.button_cancelar_operador.place(y=150)
        self.button_logar_operador.place(y=150)
        self.entry_cadastro_name = ctk.CTkEntry(master=self.janela,justify='center', width=300, placeholder_text='Nome do funcionario',
                                                font=('ROBOTO BOLD', 14))
        self.entry_cadastro_name.place(x=200, y=120)
        self.MenuGerenteLogin = True
        self.button_cadastra_operador.configure(command=lambda: self.cadastrar_operador_final())


    def voltarr(self):
        if self.tela_login_state == True:
            self.button_name_gerente.destroy()
            self.message_menu_gerencial.destroy()
            self.button_abreoperador.destroy()
            self.relatorio_gerencial.destroy()
            self.button_volta.destroy()
            self.button_logout.destroy()
            self.tela_login()
            self.janela.geometry("700x400")
            self.tela_login_state = False
            self.relogio()

    def add_pratos(self):
        n = self.combobox.get()
        size = self.listbox_pratos.size()
        items = self.listbox_pratos.get()
        if not n in self.lista_pratos:
            for i in reversed(range(size)):
                self.listbox_pratos.delete(i)

            if n == self.lista_pratos[0]:

                self.caches_produtos[f'Pizza'] += 1

                self.total += 26.90

            elif n == self.lista_pratos[1]:

                self.caches_produtos[f'Beirute'] += 1

                self.total += 19.90

            elif n == self.lista_pratos[2]:

                self.caches_produtos['X-tudo'] += 1

                self.total += 5.50

            elif n == self.lista_pratos[3]:

                self.caches_produtos[f'Batata-Frita'] += 1

                self.total += 3.0

            elif n == self.lista_pratos[4]:

                self.caches_produtos[f'cocacola2'] += 1

                self.total += 8.50

            elif n == self.lista_pratos[5]:

                self.caches_produtos[f'cocacola1'] += 1

                self.total += 5.50

            for i in self.caches_produtos.keys():

                quantidade = self.caches_produtos[i]

                if quantidade >= 1:
                    msg = i.split("[", 1)[0]

                    self.listbox_pratos.insert(0, f'({quantidade}) {msg}'.replace('cocacola2',
                                                                                  'Coca-Cola 2 Litros').replace(

                        "cocacola1", 'Coca-Cola 1 Litro'))

            self.listbox_pratos.insert(0, f'Total: {self.total:.2f}'.replace('.', ','))

        else:
            try:


                for i in reversed(range(size)):
                    self.listbox_pratos.delete(i)

                if n == self.lista_pratos[0]:

                    self.caches_produtos[f'Pizza'] += 1

                    self.total += 26.90

                elif n == self.lista_pratos[1]:

                    self.caches_produtos[f'Beirute'] += 1

                    self.total += 19.90

                elif n == self.lista_pratos[2]:

                    self.caches_produtos['X-tudo'] += 1

                    self.total += 5.50

                elif n == self.lista_pratos[3]:

                    self.caches_produtos[f'Batata-Frita'] += 1

                    self.total += 3.0

                elif n == self.lista_pratos[4]:

                    self.caches_produtos[f'cocacola2'] += 1

                    self.total += 8.50

                elif n == self.lista_pratos[5]:

                    self.caches_produtos[f'cocacola1'] += 1

                    self.total += 5.50

                for i in self.caches_produtos.keys():

                    quantidade = self.caches_produtos[i]

                    if quantidade >= 1:
                        msg = i.split("[", 1)[0]

                        self.listbox_pratos.insert(0, f'({quantidade}) {msg}'.replace('cocacola2', 'Coca-Cola 2 Litros').replace(

                            "cocacola1", 'Coca-Cola 1 Litro'))

                self.listbox_pratos.insert(0, f'Total: {self.total:.2f}'.replace('.', ','))
            except Exception as e:
                print(e)
    def tela_suceeso(self):
        self.tela_login_state = True
        try:
            self.imagem.destroy()
            self.label.destroy()
            self.label2.destroy()
            self.operador_entry.destroy()
            self.label3.destroy()
            self.but1.destroy()
            self.frm.destroy()
            self.button_cancelar_operador.destroy()
            self.button_logar_operador.destroy()
            try:
                self.entry_cadastro_name.destroy()
            except:
                pass
            self.entry_operador_funcionario.destroy()
            self.button_cadastra_operador.destroy()
            self.message_menu_gerencial.destroy()
            self.entry_operador_funcionario.destroy()
            self.button_cadastra_operador.destroy()
            self.messagem_erro_cadastro.destroy()
        except:
            pass
        self.janela.geometry("700x220")
        self.janela.title('Point Restaurante - Menu Gerencial')


       # self.frame_gerente = ctk.CTkFrame(master=self.janela)
        self.button_name_gerente = ctk.CTkButton(master=self.janela, text=f'{self.gerente.title()}', fg_color='transparent',border_width=1,border_color='#F33A0D',hover=False,width=670,height=30,font=('Arial Bold', 20))
        self.button_name_gerente.place(x=25, y=15)

        self.message_menu_gerencial = ctk.CTkLabel(master=self.janela, text='Menu Gerencial',font=('ROBOTO BOLD', 20))
        self.message_menu_gerencial.place(x=290,y=50)

        self.button_abreoperador = ctk.CTkButton(master=self.janela, text='Abri Caixa',fg_color='#0064DC',width=94, height=37,command=lambda: self.tela_abre_operador(),font=('ROBOTO Bold', 20))
        self.button_abreoperador.place(x=25, y=100)

        self.button_logout = ctk.CTkButton(master=self.janela, text='Logout Caixa', fg_color='#0064DC', width=94,
                                                 height=37, font=('ROBOTO Bold', 20))
        self.button_logout.place(x=25, y=160)

        self.button_volta = ctk.CTkButton(master=self.janela, text='Volta', fg_color='#0064DC', width=94,
                                           height=37, font=('ROBOTO Bold', 20),command=lambda: self.voltarr())
        self.button_volta.place(x=600, y=100)

        self.relatorio_gerencial = ctk.CTkButton(master=self.janela, text='Relatorio Gerencial', fg_color='#0064DC', width=94,
                                           height=37, font=('ROBOTO Bold', 20))
        self.relatorio_gerencial.place(x=165, y=100)

    def caixa_aberto(self):
        id = self.entry_operador_funcionario.get()
        func = self.buscar_funcionario(id)
        print(id)
        if func == True:
            self.combobox = ctk.StringVar()

            try:
                self.janela.geometry("700x400")
                self.button_name_gerente.destroy()
                self.message_menu_gerencial.destroy()
                self.button_abreoperador.destroy()
                self.relatorio_gerencial.destroy()
                self.button_volta.destroy()
                self.button_logout.destroy()
                try:
                    self.entry_cadastro_name.destroy()
                except:
                    pass
                try:
                    self.messagem_erro_cadastro.destroy()
                except:
                    pass


                self.button_name_gerente.destroy()
                self.button_name_funcionario = ctk.CTkButton(master=self.janela, text=f'{self.funcionario_name}',
                                                         fg_color='transparent', border_width=1, border_color='#0064DC',
                                                         hover=False, width=670, height=30, font=('Arial Bold', 20))
                self.button_name_funcionario.place(x=25, y=15)
                self.button_cadastra_operador.destroy()
                self.button_cancelar_operador.destroy()
                self.entry_operador_funcionario.destroy()
                self.button_abreoperador.destroy()
                self.button_logar_operador.destroy()
                print('funcionou')
                pratos = ['pizza','cachorro quente']

                self.messagem_escolha_prato = ctk.CTkLabel(master=self.janela, text='Escolha o Prato!',
                                                       font=('ROBOTO BOLD', 18))
                self.messagem_escolha_prato.place(x=275, y=100)
                self.selecionar_pratos = ctk.CTkComboBox(master=self.janela,values=pratos,width=200)
                self.selecionar_pratos.place(x=250, y=130)
                self.button_adicionar_prato = ctk.CTkButton(master=self.janela,fg_color='#545c5c',hover=False,text="+",command=lambda : self.add_pratos(),font=('ROBOTO BOLD', 20),width=20,height=20)
                self.button_adicionar_prato.place(x=455,y=130)

                self.listbox_pratos = CTkListbox(self.janela,listvariable=self.combobox)
                self.listbox_pratos.place(x=200,y=150)
                lista_pratos = ['pizza','carne','picanha']
            except Exception as e:
                print(e)
        else:
            self.messagem_erro_cadastro = ctk.CTkLabel(master=self.janela, text='*Dados incorretos!',
                                                       font=('ROBOTO BOLD', 14))
            self.messagem_erro_cadastro.place(y=150, x=200)
    def buscar_funcionario(self, login):
        funcionarios = []
        try:
            with open('funcionarios.txt', 'r+', encoding='Utf-8', newline='') as arquivo:
                for linha in arquivo:
                    linha = linha.strip(",")
                    funcionarios.append(linha.split(","))
                for funcionario in funcionarios:
                    operador = funcionario[0]
                    print(funcionario[0],funcionario[1],login)
                    self.funcionario_name = funcionario[1]
                    if login == operador:
                        return True
        except:
            pass
    def buscar_usuario(self,login, senha):
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
                self.gerente = row[2]
                if login == nome and senha == password:
                    return True

        except HttpError as err:
            print('erros')
            print(err)
    def fazer_login(self):
        operador = self.operador_entry.get()
        senha = self.senha_entry.get()
        print(operador,senha)
        if operador == '' or senha == '' or not operador.isnumeric() or not senha.isnumeric() or len(operador) > 8 or len(senha) > 5:
            self.ewroon()
            return
        user = self.buscar_usuario(operador,senha)
        if user == True:
            print('Login realizado com sucesso pelo gerente!')
            self.tela_suceeso()
        else:
            self.ewroon()


MenuGerenteLogin()