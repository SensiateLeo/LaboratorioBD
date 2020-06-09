from tkinter import *
from PIL import ImageTk, Image
import psycopg2
import sys
import database

import hashlib
from datetime import datetime

try:

    connection = psycopg2.connect(user = "postgres",
                                  password = "teste123",
                                  host = "localhost",
                                  port = "5432",
                                  database = "COVID")

    cursor = connection.cursor()

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    sys.exit()

class Application:


    def __init__(self,root):

        self.root = root
        self.root.geometry("500x500")
        self.root.title('Tela de Login')
        self.fontePadrao = ("Arial", "10")

        self.img = ImageTk.PhotoImage(Image.open("oms.png"))

        self.imgContainer = Frame(root)
        self.imgContainer["pady"] = 20
        self.imgContainer.pack()

        self.primeiroContainer = Frame(root)
        self.primeiroContainer["pady"] = 20
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(root)
        self.segundoContainer["pady"] = 20
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(root)
        self.terceiroContainer["pady"] = 20
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(root)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.quintoContainer = Frame(root)
        self.quintoContainer["pady"] = 20
        self.quintoContainer.pack()

        self.imgLabel = Label(self.imgContainer, image=self.img)
        self.imgLabel.pack()

        self.titulo = Label(self.primeiroContainer, text="Dados do usuário")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.nomeLabel = Label(self.segundoContainer, text="Nome", font=self.fontePadrao)
        self.nomeLabel.pack(side=LEFT)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 30
        self.nome["font"] = self.fontePadrao
        self.nome.pack(side=LEFT)

        self.senhaLabel = Label(self.terceiroContainer, text="Senha", font=self.fontePadrao)
        self.senhaLabel.pack(side=LEFT)

        self.senha = Entry(self.terceiroContainer)
        self.senha["width"] = 30
        self.senha["font"] = self.fontePadrao
        self.senha["show"] = "*"
        self.senha.pack(side=LEFT)

        self.autenticar = Button(self.quartoContainer)
        self.autenticar["text"] = "Entrar"
        self.autenticar["font"] = self.fontePadrao
        self.autenticar["width"] = 12
        self.autenticar["command"] = self.verificaSenha
        self.autenticar.pack()

        self.mensagem = Label(self.quintoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()

    def verificaSenha(self):
        usuario = self.nome.get()
        senha = self.senha.get()

        result = hashlib.md5(senha.encode())
        hash_senha = result.hexdigest()

        row = database.autenticar(cursor, usuario, hash_senha)

        log = open('log_COVID.txt', 'a+')

        if (row == None):
            self.mensagem["text"] = "Erro na autenticação"
        else:
            if usuario == row[0] and hash_senha == row[1]:
                self.mensagem["text"] = "Autenticado"

                log.write('Usuário ' + usuario + '. Acesso em: ')
                now = datetime.now()
                data_e_hora_em_texto = now.strftime('%d/%m/%Y às %H:%M')
                log.write(data_e_hora_em_texto)
                log.write('\n')
                # Destroy the current window
                root.destroy()

                # Open new window
                newroot = Tk()
                application = Dashboard(newroot,row[0],database.verifica_Tipo(cursor,row[0]))
                newroot.mainloop()

            else:
                print(row[1])
                self.mensagem["text"] = "Erro na autenticação"

        log.close()

class Dashboard:

    #Tela Inicial
    #Contém as opções Relatório,Simulações e Overview
    def frameTelaInicial(self, tipo):

        self.frame1 = Frame()
        self.frame1["pady"] = 10

        btn1 = Button(self.frame1,
                      text="Relatorio", height=3, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameRelatoriosTelaInicial(tipo).pack()]).pack(padx=20, pady=5)
        btn2 = Button(self.frame1, text="Simulações", height=3, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameSimulacoesTelaInicial(tipo).pack()]).pack(padx=20, pady=5)
        btn3 = Button(self.frame1,
                      text="Overview", height=3, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameOverviewTelaInicial(tipo).pack()]).pack(padx=20, pady=5)


        return self.frame1

    #Tela de Relatórios
    def frameRelatoriosTelaInicial(self, tipo):

        self.frame1 = Frame()
        self.frame1["pady"] = 10


        self.relatorios = Label(self.frame1, text="Relatórios Disponíveis:")
        self.relatorios["font"] = ("Arial", "10")
        self.relatorios["pady"] = 30
        self.relatorios.pack()

        btn1 = Button(master=self.frame1,
                      text="Histórico Pessoal", height=1, width=40).pack(padx=20, pady=5)

        if(tipo == 'Admin'):
            btn2 = Button(master=self.frame1, text="Histórico dos Hospitais", height=1, width=40).pack(padx=20, pady=5)

            btn3 = Button(master=self.frame1,
                          text="Histórico dos Atendimentos dos Hospitais", height=1, width=40).pack(padx=20, pady=5)

            btn4 = Button(master=self.frame1,
                          text="Histórico de Amostras", height=1, width=40).pack(padx=20, pady=5)

            btn5 = Button(master=self.frame1,
                          text="Histórico de Laboratórios", height=1, width=40).pack(padx=20, pady=5)

            btn6 = Button(master=self.frame1,
                          text="Histórico de Pesquisadores", height=1, width=40).pack(padx=20, pady=5)

        elif(tipo=='Medicina'):

            btn2 = Button(master=self.frame1, text="Histórico dos Hospitais", height=1, width=40).pack(padx=20, pady=5)

            btn3 = Button(master=self.frame1,
                          text="Histórico dos Atendimentos dos Hospitais", height=1, width=40).pack(padx=20, pady=5)

        elif(tipo=='Pesquisa'):
            btn4 = Button(master=self.frame1,
                          text="Histórico de Amostras", height=1, width=40).pack(padx=20, pady=5)

            btn5 = Button(master=self.frame1,
                          text="Histórico de Laboratórios", height=1, width=40).pack(padx=20, pady=5)

            btn6 = Button(master=self.frame1,
                          text="Histórico de Pesquisadores", height=1, width=40).pack(padx=20, pady=5)

        btn7 = Button(self.frame1,
                      text="Retornar a Tela Inicial", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameTelaInicial(tipo).pack()]).pack(padx=20, pady=30)

        return self.frame1

    #Tela de Overview
    def frameOverviewTelaInicial(self ,tipo):

        self.frame1 = Frame()
        self.frame1["pady"] = 10


        self.relatorios = Label(self.frame1, text="Indicadores Disponíveis:")
        self.relatorios["font"] = ("Arial", "10")
        self.relatorios["pady"] = 30
        self.relatorios.pack()

        btn1 = Button(master=self.frame1,
                      text="Total de casos positivos da COVID-19", height=1, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameCasosPositivos(tipo).pack()]).pack(padx=20, pady=5)

        btn2 = Button(master=self.frame1, text="Total de casos suspeitos da COVID-19", height=1, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameCasosSuspeitos(tipo).pack()]).pack(padx=20, pady=5)

        btn3 = Button(master=self.frame1,
                      text="20 Hospitais com mais pacientes no último mês", height=1, width=40,command=lambda:
            self.frameHospitalPopuloso()).pack(padx=20, pady=5)

        btn4 = Button(master=self.frame1,
                      text="20 Laboratórios com mais analises no ultimos mês", height=1, width=40,command=lambda:
            self.frameLabMaisAnalisado()).pack(padx=20, pady=5)

        btn5 = Button(master=self.frame1,
                      text="20 Cidades com mais casos positivos no último mês", height=1, width=40, command=lambda:
            self.frameCidadeMaisPositivos()).pack(padx=20, pady=5)

        btn6 = Button(master=self.frame1,
                      text="20 Cidades com mais casos suspeitos no último mês", height=1, width=40, command=lambda:
            self.frameCidadeMaisSuspeitos()).pack(padx=20, pady=5)
        btn7 = Button(self.frame1,
                      text="Retornar a Tela Inicial", height=1, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameTelaInicial(tipo).pack()]).pack(padx=50, pady=30)

        return self.frame1

    #Tela de Simulações
    def frameSimulacoesTelaInicial(self, tipo):

        self.frame1 = Frame()
        self.frame1["pady"] = 10

        self.relatorios = Label(self.frame1, text="Simulações Disponíveis:")
        self.relatorios["font"] = ("Arial", "10")
        self.relatorios.pack()

        if (tipo == 'Admin'):
            self.prontuarios = Label(self.frame1, text="Prontuarios")
            self.prontuarios["pady"] = 20
            self.prontuarios["font"] = ("Arial", "10")
            self.prontuarios.pack()

            btn1 = Button(master=self.frame1,
                          text="Criação de Prontuário", height=1, width=40).pack(padx=20, pady=5)

            btn2 = Button(master=self.frame1, text="Alteração de Prontuario", height=1, width=40).pack(padx=20, pady=5)

            self.atendimentos = Label(self.frame1, text="Atendimentos")
            self.atendimentos["pady"] = 20
            self.atendimentos["font"] = ("Arial", "10")
            self.atendimentos.pack()

            btn3 = Button(master=self.frame1,
                          text="Criação de Atendimento", height=1, width=40).pack(padx=20, pady=5)

            btn4 = Button(master=self.frame1,
                          text="Alteração de Atendimento", height=1, width=40).pack(padx=20, pady=5)

            self.amostra = Label(self.frame1, text="Amostras")
            self.amostra["pady"] = 20
            self.amostra["font"] = ("Arial", "10")
            self.amostra.pack()

            btn5 = Button(master=self.frame1,
                          text="Criação de Amostra", height=1, width=40).pack(padx=20, pady=5)

            btn6 = Button(master=self.frame1,
                          text="Alteração de Amostra", height=1, width=40).pack(padx=20, pady=5)
            btn7 = Button(self.frame1,
                          text="Retornar a Tela Inicial", height=1, width=40, command=lambda:
                [self.frame1.pack_forget(), self.frameTelaInicial(tipo).pack()]).pack(padx=20, pady=30)

        elif (tipo == 'Medicina'):
            self.prontuarios = Label(self.frame1, text="Prontuarios")
            self.prontuarios["pady"] = 20
            self.prontuarios["font"] = ("Arial", "10")
            self.prontuarios.pack()


            btn1 = Button(master=self.frame1,
                          text="Criação de Prontuário", height=1, width=40).pack(padx=20, pady=5)

            btn2 = Button(master=self.frame1, text="Alteração de Prontuario", height=1, width=40).pack(padx=20, pady=5)

            self.atendimentos = Label(self.frame1, text="Atendimentos")
            self.atendimentos["pady"] = 20
            self.atendimentos["font"] = ("Arial", "10")
            self.atendimentos.pack()

            btn3 = Button(master=self.frame1,
                          text="Criação de Atendimento", height=1, width=40).pack(padx=20, pady=5)

            btn4 = Button(master=self.frame1,
                          text="Alteração de Atendimento", height=1, width=40).pack(padx=20, pady=5)

        elif (tipo == 'Pesquisa'):
            self.amostra = Label(self.frame1, text="Amostras")
            self.amostra["pady"] = 20
            self.amostra["font"] = ("Arial", "10")
            self.amostra.pack()

            btn5 = Button(master=self.frame1,
                          text="Criação de Amostra", height=1, width=40).pack(padx=20, pady=5)

            btn6 = Button(master=self.frame1,
                          text="Alteração de Amostra", height=1, width=40).pack(padx=20, pady=5)
            btn7 = Button(self.frame1,
                          text="Retornar a Tela Inicial", height=1, width=40,command=lambda:
                [self.frame1.pack_forget(),self.frameTelaInicial(tipo).pack()]).pack(padx=20, pady=30)

        return self.frame1

    def frameCasosPositivos(self,tipo):
        self.frame1 = Frame()
        self.frame1["pady"] = 10

        self.casosPositivos = Label(self.frame1, text="Total de casos positivos:")
        self.casosPositivos["font"] = ("Arial", "20")
        self.casosPositivos.pack()

        self.numCasos = database.overview_casosPositivos(cursor)
        self.num = Label(self.frame1, text= self.numCasos)
        self.num["font"] = ("Arial", "20")
        self.num.pack()

        btn = Button(self.frame1,
                      text="Retornar a Overview", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameOverviewTelaInicial(tipo).pack()]).pack(padx=20, pady=30)

        return self.frame1

    def frameCasosSuspeitos(self,tipo):
        self.frame1 = Frame()
        self.frame1["pady"] = 10

        self.casosSuspeitos= Label(self.frame1, text="Total de casos suspeitos:")
        self.casosSuspeitos["font"] = ("Arial", "20")
        self.casosSuspeitos.pack()

        self.numCasos = database.overview_casosSuspeitos(cursor)
        self.num = Label(self.frame1, text=self.numCasos)
        self.num["font"] = ("Arial", "20")
        self.num.pack()

        btn = Button(self.frame1,
                     text="Retornar a Overview", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameOverviewTelaInicial(tipo).pack()]).pack(padx=20, pady=30)

        return self.frame1

    def frameHospitalPopuloso(self):

        self.root = Tk()
        self.root.title("Hospitais Populosos")

        self.lst = [("Hospital", "Quantidade")]
        self.list = database.overview_HopistalPopuloso(cursor)
        for row in self.list:
            self.lst.append(row)

        total_rows = len(self.lst)
        total_columns = len(self.lst[0])

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(self.root, width=50, fg='black',font=('Arial', 8),justify=CENTER)

                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i][j])

        self.root.mainloop()

    def frameLabMaisAnalisado(self):

        self.root = Tk()
        self.root.title("Laboratório Análises")

        self.lst = [("Laboratório", "Quantidade de Amostras")]
        self.list = database.overview_LabMaisAnalisados(cursor)
        for row in self.list:
            self.lst.append(row)

        total_rows = len(self.lst)
        total_columns = len(self.lst[0])

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(self.root, width=50, fg='black',font=('Arial', 8),justify=CENTER)

                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i][j])

        self.root.mainloop()

    def frameCidadeMaisPositivos(self):

        self.root = Tk()
        self.root.title("Cidades com Mais Casos Positivos")

        self.lst = [("Cidade", "Quantidade")]
        self.list = database.overview_CidadesMaisPositivos(cursor)
        for row in self.list:
            self.lst.append(row)

        total_rows = len(self.lst)
        total_columns = len(self.lst[0])

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(self.root, width=50, fg='black',font=('Arial', 8),justify=CENTER)

                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i][j])

        self.root.mainloop()

    def frameCidadeMaisSuspeitos(self):

        self.root = Tk()
        self.root.title("Cidades com Mais Casos Suspeitos")

        self.lst = [("Cidade", "Quantidade")]
        self.list = database.overview_CidadesMaisSuspeitos(cursor)
        for row in self.list:
            self.lst.append(row)

        total_rows = len(self.lst)
        total_columns = len(self.lst[0])

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(self.root, width=50, fg='black',font=('Arial', 8),justify=CENTER)

                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i][j])

        self.root.mainloop()




    def __init__(self, root, user, tipo):

        self.root = root
        self.root.geometry("600x600")
        self.root.title('Dashboard')

        self.primeiroContainer = Frame(root)
        self.primeiroContainer["pady"] = 20
        self.primeiroContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Bem vindo usuário " + user)
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.depto = Label(self.primeiroContainer, text="Departamento: " + tipo)
        self.depto["font"] = ("Arial", "10")
        self.depto.pack()

        frame_inicial = self.frameTelaInicial(tipo)

        frame_inicial.pack()

if __name__ == '__main__':

    root = Tk()
    app = Application(root)
    root.mainloop()