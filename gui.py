from tkinter import *
from PIL import ImageTk, Image
import psycopg2
import sys
import database
import hashlib
from datetime import datetime
from tkinter import messagebox

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:

    connection = psycopg2.connect(user = "postgres",
                                  password = "teste123",
                                  host = "localhost",
                                  port = "5432",
                                  database = "COVID")

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
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
                      text="Relatórios", height=3, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameRelatoriosTelaInicial(tipo).pack()]).pack(padx=20, pady=5)
        btn2 = Button(self.frame1, text="Simulações", height=3, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameSimulacoesTelaInicial(tipo).pack()]).pack(padx=20, pady=5)
        btn3 = Button(self.frame1,
                      text="Dashboard", height=3, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameOverviewTelaInicial(tipo).pack()]).pack(padx=20, pady=5)

        return self.frame1
##################################################################################################

    #Tela de Relatórios

    def frameRelatoriosTelaInicial(self,tipo):

        self.frame1 = Frame()
        self.frame1["pady"] = 10

        self.relatorios = Label(self.frame1, text="Relatórios Disponíveis:")
        self.relatorios["font"] = ("Arial", "10")
        self.relatorios["pady"] = 30
        self.relatorios.pack()

        btn1 = Button(master=self.frame1,
                      text="Histórico Pessoal", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameFiltraRelatorioPessoal(tipo).pack()]).pack(padx=20, pady=5)

        if(tipo=='Medicina' or tipo == 'Admin'):

            btn2 = Button(master=self.frame1, text="Histórico dos Hospitais", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameFiltraRelatorioHospital(tipo).pack()]).pack(padx=20, pady=5)

            btn3 = Button(master=self.frame1,
                          text="Histórico dos Atendimentos dos Hospitais", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameFiltraRelatorioAtendimento(tipo).pack()]).pack(padx=20, pady=5)

        if(tipo=='Pesquisa' or tipo == 'Admin'):
            btn4 = Button(master=self.frame1,
                          text="Histórico de Amostras", height=1, width=40, command=lambda:
                [self.frame1.pack_forget(), self.frameFiltraRelatorioAmostra(tipo).pack()]).pack(padx=20, pady=5)

            btn5 = Button(master=self.frame1,
                          text="Histórico de Laboratórios", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameFiltraRelatorioLab(tipo).pack()]).pack(padx=20, pady=5)

            btn6 = Button(master=self.frame1,
                          text="Histórico de Pesquisadores", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameFiltraRelatorioPesquisa(tipo).pack()]).pack(padx=20, pady=5)

        btn7 = Button(self.frame1,
                      text="Retornar a Tela Inicial", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameTelaInicial(tipo).pack()]).pack(padx=20, pady=30)

        return self.frame1

    #Função para pegar valor para filtragem de pesquisas
    def pegavalor(self):
        var = self.nome.get()
        return var

    # Exibir tabela com histórico de Pacientes
    def frameHistoricoPessoal(self, nome):

        self.root = Tk()
        self.root.title("Histórico Pessoal do Paciente")
        self.fontePadrao = ("Arial", "10")

        self.primeiroContainer = Frame(self.root)
        self.primeiroContainer["pady"] = 20
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(self.root)
        self.segundoContainer.pack()

        self.lst = [("Nome", "Idade", "Sexo", "Data de Nascimento", "Contato", "Endereço", "Hospital")]
        self.list = database.relatorio_historicoPessoal(cursor, nome)
        for row in self.list:
            self.lst.append(row)

        total_rows = len(self.lst)
        total_columns = len(self.lst[0])

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(self.segundoContainer, width=20, fg='black', font=('Arial', 8), justify=CENTER)

                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i][j])

        self.root.mainloop()

    # Tela para filtragem por nome de paciente
    def frameFiltraRelatorioPessoal(self,tipo):
        self.frame1 = Frame()
        self.frame1["pady"] = 10

        self.segundoContainer = Frame(self.frame1)
        self.segundoContainer["pady"] = 20
        self.segundoContainer["padx"] = 20

        self.textFiltro = Label(self.frame1, text="Deseja Filtrar sua pesquisa?")
        self.textFiltro["font"] = ("Arial", "15")
        self.textFiltro.pack()

        btn1 = Button(master=self.frame1, text="Sim", height=1, width=10, command=lambda:
        self.segundoContainer.pack()).pack(padx=20, pady=5)

        btn2 = Button(master=self.frame1, text="Não", height=1, width=10, command=lambda:
        [self.frame1.pack_forget(), self.frameRelatoriosTelaInicial(tipo).pack(),
         self.frameHistoricoPessoal('')]).pack(padx=20, pady=5)

        self.nomeLabel = Label(self.segundoContainer, text="Nome do Paciente: ", font=("Arial", "10"))
        self.nomeLabel.pack(side=LEFT)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 40
        self.nome["font"] = ("Arial", "10")
        self.nome.pack(side=LEFT)

        filtrar = Button(master=self.segundoContainer, text="Filtrar", height=1, width=10, command=lambda:
        [self.frame1.pack_forget(),self.frameRelatoriosTelaInicial(tipo).pack(), self.frameHistoricoPessoal(self.pegavalor())]).pack(padx=20, pady=5)

        return self.frame1

    # Exibir tabela com histórico de Hospitais
    def frameHistoricoHospital(self, nome):

        self.root = Tk()
        self.root.title("Histórico dos Hospitais")
        self.fontePadrao = ("Arial", "10")

        self.segundoContainer = Frame(self.root)
        self.segundoContainer.pack()

        self.lst = [("Nome", "Endereço", "Funcionários", "Leitos", "Atendimentos Registrados", "Pacientes Atendidos")]
        self.list = database.relatorio_historicoHospitais(cursor, nome)
        for row in self.list:
            self.lst.append(row)

        total_rows = len(self.lst)
        total_columns = len(self.lst[0])

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(self.segundoContainer, width=20, fg='black',font=('Arial', 8),justify=CENTER)

                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i][j])

        self.root.mainloop()

    # Tela para filtragem por nome de Hospital
    def frameFiltraRelatorioHospital(self, tipo):
        self.frame1 = Frame()
        self.frame1["pady"] = 10

        self.segundoContainer = Frame(self.frame1)
        self.segundoContainer["pady"] = 20
        self.segundoContainer["padx"] = 20

        self.textFiltro = Label(self.frame1, text="Deseja Filtrar sua pesquisa?")
        self.textFiltro["font"] = ("Arial", "15")
        self.textFiltro.pack()

        btn1 = Button(master=self.frame1, text="Sim", height=1, width=10, command=lambda:
        self.segundoContainer.pack()).pack(padx=20, pady=5)

        btn2 = Button(master=self.frame1, text="Não", height=1, width=10, command=lambda:
        [self.frame1.pack_forget(), self.frameRelatoriosTelaInicial(tipo).pack(),
         self.frameHistoricoHospital('')]).pack(padx=20, pady=5)

        self.nomeLabel = Label(self.segundoContainer, text="Nome do Hospital: ", font=("Arial", "10"))
        self.nomeLabel.pack(side=LEFT)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 40
        self.nome["font"] = ("Arial", "10")
        self.nome.pack(side=LEFT)

        filtrar = Button(master=self.segundoContainer, text="Filtrar", height=1, width=10, command=lambda:
        [self.frame1.pack_forget(), self.frameRelatoriosTelaInicial(tipo).pack(),
         self.frameHistoricoHospital(self.pegavalor())]).pack(padx=20, pady=5)

        return self.frame1

    # Exibir tabela com histórico de Atendimentos
    def frameHistoricoAtendimentos(self, nome):

        self.root = Tk()
        self.root.title("Histórico de Atendimentos dos Municípios")
        self.fontePadrao = ("Arial", "10")

        self.segundoContainer = Frame(self.root)
        self.segundoContainer.pack()

        self.lst = [("Cidade", "Atendimentos Realizados", "Pacientes Atendidos")]
        self.list = database.relatorio_historicoAtendimentos(cursor, nome)
        for row in self.list:
            self.lst.append(row)

        total_rows = len(self.lst)
        total_columns = len(self.lst[0])

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(self.segundoContainer, width=20, fg='black', font=('Arial', 8), justify=CENTER)

                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i][j])

        self.root.mainloop()

    # Tela para filtragem por nome de Atendimentos
    def frameFiltraRelatorioAtendimento(self, tipo):
        self.frame1 = Frame()
        self.frame1["pady"] = 10

        self.segundoContainer = Frame(self.frame1)
        self.segundoContainer["pady"] = 20
        self.segundoContainer["padx"] = 20

        self.textFiltro = Label(self.frame1, text="Deseja Filtrar sua pesquisa?")
        self.textFiltro["font"] = ("Arial", "15")
        self.textFiltro.pack()

        btn1 = Button(master=self.frame1, text="Sim", height=1, width=10, command=lambda:
        self.segundoContainer.pack()).pack(padx=20, pady=5)

        btn2 = Button(master=self.frame1, text="Não", height=1, width=10, command=lambda:
        [self.frame1.pack_forget(), self.frameRelatoriosTelaInicial(tipo).pack(),
         self.frameHistoricoAtendimentos('')]).pack(padx=20, pady=5)

        self.nomeLabel = Label(self.segundoContainer, text="Nome da Cidade: ", font=("Arial", "10"))
        self.nomeLabel.pack(side=LEFT)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 40
        self.nome["font"] = ("Arial", "10")
        self.nome.pack(side=LEFT)

        filtrar = Button(master=self.segundoContainer, text="Filtrar", height=1, width=10, command=lambda:
        [self.frame1.pack_forget(), self.frameRelatoriosTelaInicial(tipo).pack(),
         self.frameHistoricoAtendimentos(self.pegavalor())]).pack(padx=20, pady=5)

        return self.frame1

    # Exibir tabela com histórico de Amostras
    def frameHistoricoAmostras(self, valor):

        self.root = Tk()
        self.root.title("Histórico de Amostras")
        self.fontePadrao = ("Arial", "10")

        self.segundoContainer = Frame(self.root)
        self.segundoContainer.pack()

        self.lst = [("Nome Paciente", "Idade", "Sexo", "Endereço", "Data da Amostra", "Resultado", "Laboratório")]
        self.list = database.relatorio_historicoAmostras(cursor, valor)
        for row in self.list:
            self.lst.append(row)

        total_rows = len(self.lst)
        total_columns = len(self.lst[0])

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(self.segundoContainer, width=20, fg='black', font=('Arial', 8), justify=CENTER)

                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i][j])

        self.root.mainloop()

    # Tela para filtragem por data de amostra
    def frameFiltraRelatorioAmostra(self,tipo):
        self.frame1 = Frame()
        self.frame1["pady"] = 10

        self.segundoContainer = Frame(self.frame1)
        self.segundoContainer["pady"] = 20
        self.segundoContainer["padx"] = 20

        self.textFiltro = Label(self.frame1, text="Deseja Filtrar sua pesquisa?")
        self.textFiltro["font"] = ("Arial", "15")
        self.textFiltro.pack()

        btn1 = Button(master=self.frame1, text="Sim", height=1, width=10, command=lambda:
        self.segundoContainer.pack()).pack(padx=20, pady=5)

        btn2 = Button(master=self.frame1, text="Não", height=1, width=10, command=lambda:
        [self.frame1.pack_forget(), self.frameRelatoriosTelaInicial(tipo).pack(),
         self.frameHistoricoAmostras('')]).pack(padx=20, pady=5)

        self.nomeLabel = Label(self.segundoContainer, text="Data: ", font=("Arial", "10"))
        self.nomeLabel.pack(side=LEFT)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 40
        self.nome["font"] = ("Arial", "10")
        self.nome.pack(side=LEFT)

        filtrar = Button(master=self.segundoContainer, text="Filtrar", height=1, width=10, command=lambda:
        [self.frame1.pack_forget(),self.frameRelatoriosTelaInicial(tipo).pack(), self.frameHistoricoAmostras(self.pegavalor())]).pack(padx=20, pady=5)

        return self.frame1

    # Exibir tabela com histórico de Laboratorios
    def frameHistoricoLaboratorios(self, nome):

        self.root = Tk()
        self.root.title("Histórico de Laboratórios")
        self.fontePadrao = ("Arial", "10")

        self.segundoContainer = Frame(self.root)
        self.segundoContainer.pack()

        self.lst = [("Nome", "Quantidade Pesquisadores", "Endereço", "Amostras Recebidas")]
        self.list = database.relatorio_historicoLaboratorios(cursor, nome)
        for row in self.list:
            self.lst.append(row)

        total_rows = len(self.lst)
        total_columns = len(self.lst[0])

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(self.segundoContainer, width=20, fg='black', font=('Arial', 8), justify=CENTER)

                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i][j])

        self.root.mainloop()

    # Tela para filtragem por nome de laboratório
    def frameFiltraRelatorioLab(self,tipo):
        self.frame1 = Frame()
        self.frame1["pady"] = 10

        self.segundoContainer = Frame(self.frame1)
        self.segundoContainer["pady"] = 20
        self.segundoContainer["padx"] = 20

        self.textFiltro = Label(self.frame1, text="Deseja Filtrar sua pesquisa?")
        self.textFiltro["font"] = ("Arial", "15")
        self.textFiltro.pack()

        btn1 = Button(master=self.frame1, text="Sim", height=1, width=10, command=lambda:
        self.segundoContainer.pack()).pack(padx=20, pady=5)

        btn2 = Button(master=self.frame1, text="Não", height=1, width=10, command=lambda:
        [self.frame1.pack_forget(), self.frameRelatoriosTelaInicial(tipo).pack(),
         self.frameHistoricoLaboratorios('')]).pack(padx=20, pady=5)

        self.nomeLabel = Label(self.segundoContainer, text="Nome do Laboratório: ", font=("Arial", "10"))
        self.nomeLabel.pack(side=LEFT)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 40
        self.nome["font"] = ("Arial", "10")
        self.nome.pack(side=LEFT)

        filtrar = Button(master=self.segundoContainer, text="Filtrar", height=1, width=10, command=lambda:
        [self.frame1.pack_forget(),self.frameRelatoriosTelaInicial(tipo).pack(), self.frameHistoricoLaboratorios(self.pegavalor())]).pack(padx=20, pady=5)

        return self.frame1

    #Exibir tabela com histórico de Pesquisadores
    def frameHistoricoPesquisadores(self, valor):

        self.root = Tk()
        self.root.title("Histórico de Pesquisadores")
        self.fontePadrao = ("Arial", "10")

        self.segundoContainer = Frame(self.root)
        self.segundoContainer.pack()

        self.lst = [("Nome", "Registro Institucional", "Data de Contratação", "ID da Amostra", "Data da Amostra", "Resultado Amostra")]
        self.list = database.relatorio_historicoPesquisadores(cursor, valor)
        for row in self.list:
            self.lst.append(row)

        total_rows = len(self.lst)
        total_columns = len(self.lst[0])

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(self.segundoContainer, width=20, fg='black', font=('Arial', 8), justify=CENTER)

                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i][j])

        self.root.mainloop()

    #Tela para filtragem por nome de pesquisador
    def frameFiltraRelatorioPesquisa(self,tipo):
        self.frame1 = Frame()
        self.frame1["pady"] = 10

        self.segundoContainer = Frame(self.frame1)
        self.segundoContainer["pady"] = 20
        self.segundoContainer["padx"] = 20

        self.textFiltro = Label(self.frame1, text="Deseja Filtrar sua pesquisa?")
        self.textFiltro["font"] = ("Arial", "15")
        self.textFiltro.pack()

        btn1 = Button(master=self.frame1, text="Sim", height=1, width=10, command=lambda:
        self.segundoContainer.pack()).pack(padx=20, pady=5)

        btn2 = Button(master=self.frame1, text="Não", height=1, width=10, command=lambda:
        [self.frame1.pack_forget(), self.frameRelatoriosTelaInicial(tipo).pack(),
         self.frameHistoricoPesquisadores('')]).pack(padx=20, pady=5)

        self.nomeLabel = Label(self.segundoContainer, text="Nome do Pesquisador: ", font=("Arial", "10"))
        self.nomeLabel.pack(side=LEFT)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 40
        self.nome["font"] = ("Arial", "10")
        self.nome.pack(side=LEFT)

        filtrar = Button(master=self.segundoContainer, text="Filtrar", height=1, width=10, command=lambda:
        [self.frame1.pack_forget(),self.frameRelatoriosTelaInicial(tipo).pack(), self.frameHistoricoPesquisadores(self.pegavalor())]).pack(padx=20, pady=5)

        return self.frame1

#######################################################################################

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

    def frameSimulacoesTelaInicial(self, tipo):

        self.frame1 = Frame()
        self.frame1["pady"] = 10

        self.relatorios = Label(self.frame1, text="Simulações Disponíveis:")
        self.relatorios["font"] = ("Arial", "10")
        self.relatorios.pack()

        if (tipo == 'Medicina' or tipo =='Admin'):
            self.prontuarios = Label(self.frame1, text="Prontuarios")
            self.prontuarios["pady"] = 20
            self.prontuarios["font"] = ("Arial", "10")
            self.prontuarios.pack()


            btn1 = Button(master=self.frame1,
                          text="Criação de Prontuário", height=1, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameSimulacaoCriaProntuario(tipo).pack()]).pack(padx=20)

            btn2 = Button(master=self.frame1, text="Visualização de Prontuario", height=1, width=40,command=lambda:
            self.frameshowSimulacaoProntuario()).pack(padx=20)

            btn3 = Button(master=self.frame1, text="Alteração de Prontuario", height=1, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameSimulacaoAlteraProntuario(tipo).pack()]).pack(padx=20)

            btn4 = Button(master=self.frame1,
                          text="Limpar Simulação Prontuário", height=1, width=40,command=lambda: self.limpaProntuario()).pack(padx=20)

            self.atendimentos = Label(self.frame1, text="Atendimentos")
            self.atendimentos["pady"] = 20
            self.atendimentos["font"] = ("Arial", "10")
            self.atendimentos.pack()

            btn5 = Button(master=self.frame1,
                          text="Criação de Atendimento", height=1, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameSimulacaoCriaAtendimento(tipo).pack()]).pack(padx=20)

            btn6 = Button(master=self.frame1,
                          text="Visualização de Atendimento", height=1, width=40,command=lambda:
            self.frameshowSimulacaoAtendimento()).pack(padx=20)
            btn7 = Button(master=self.frame1,
                          text="Alteração de Atendimento", height=1, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameSimulacaoAlteraAtendimento(tipo).pack()]).pack(padx=20)
            btn8 = Button(master=self.frame1,
                          text="Limpar Simulação Atendimento", height=1, width=40,command=lambda: self.limpaAtendimento()).pack(padx=20)

        if (tipo == 'Pesquisa' or tipo == 'Admin'):
            self.amostra = Label(self.frame1, text="Amostras")
            self.amostra["pady"] = 20
            self.amostra["font"] = ("Arial", "10")
            self.amostra.pack()

            btn9 = Button(master=self.frame1,
                          text="Criação de Amostra", height=1, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameSimulacaoCriaAmostra(tipo).pack()]).pack(padx=20)

            btn10 = Button(master=self.frame1,
                          text="Visualização de Amostra", height=1, width=40,command=lambda:
            self.frameshowSimulacaoAmostra()).pack(padx=20)
            btn11 = Button(master=self.frame1,
                          text="Alteração de Amostra", height=1, width=40,command=lambda:
            [self.frame1.pack_forget(),self.frameSimulacaoAlteraAmostra(tipo).pack()]).pack(padx=20)
            btn12 = Button(master=self.frame1,
                          text="Limpar Simulação Amostra", height=1, width=40,command=lambda: self.limpaAmostra()).pack(padx=20)
            btn13 = Button(self.frame1,
                          text="Retornar a Tela Inicial", height=1, width=40,command=lambda:
                [self.frame1.pack_forget(),self.frameTelaInicial(tipo).pack()]).pack(padx=20, pady=10)

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
##################################################################################################

    #Tela de Simulacoes

    #ATENDIMENTOS

    #Função de chamada ao banco de dados - UPDATE
    def alteraAtendimento(self,id_atendimento,data,grau_avaliacao,observacao):

        database.updateAtendimento(cursor,id_atendimento,data,grau_avaliacao,observacao)

    #Funcao de chamada ao banco de dados - INSERT
    def insereAtendimento(self,date,grau_avalicao,observacoes,idMedico,idPaciente,idProntuario):
        database.insertAtendimento(cursor,date,grau_avalicao,observacoes,idMedico,idPaciente,idProntuario)

    #Funcao de chamada ao banco de dados - DROP AND INSERT
    def limpaAtendimento(self):
        database.resetAtendimento(cursor)
        messagebox.showinfo("Reset Atendimento", "Tabela Atendimento voltou ao seu estado original")

    #Funcao que mostra a tabela simulada
    def frameshowSimulacaoAtendimento(self):

        self.root = Tk()
        self.root.title("Visualização Simulação Atendimento")

        self.lst = [("ID Atendimento", "Data","Grau de Avaliação,","Observações","ID Médico","ID Paciente","ID Prontuário")]
        self.list = database.showAtendimento(cursor)
        for row in self.list:
            self.lst.append(row)

        total_rows = len(self.lst)
        total_columns = len(self.lst[0])

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(self.root, width=20, fg='black',font=('Arial', 12),justify=CENTER)

                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i][j])

        self.root.mainloop()

    #Funcao Forms para insercao de atendimento
    def frameSimulacaoCriaAtendimento(self,tipo):

        def change():
            messagebox.showinfo("Inserção", "Inserido com sucesso")
            self.data.delete(0, 'end')
            self.grau_avaliacao.delete(0, 'end')
            self.observacoes.delete(0, 'end')
            self.idMedico.delete(0, 'end')
            self.idPaciente.delete(0, 'end')
            self.idProntuario.delete(0, 'end')

        self.frame1 = Frame()
        self.frame1["pady"] = 20
        self.fontePadrao = ("Arial", "10")

        self.atendimento = Label(self.frame1, text="Criação do Atendimento")
        self.atendimento["pady"] = 5
        self.atendimento["font"] = self.fontePadrao
        self.atendimento.pack()

        self.dataLabel = Label(self.frame1, text="Data", font=self.fontePadrao)
        self.dataLabel["pady"] = 5
        self.dataLabel.pack(side=TOP)

        self.data = Entry(self.frame1)
        self.data["width"] = 30
        self.data["font"] = self.fontePadrao
        self.data.pack(side=TOP)

        self.grau_avaliacaoLabel = Label(self.frame1, text="Grau de Avaliação", font=self.fontePadrao)
        self.grau_avaliacaoLabel["pady"] = 5
        self.grau_avaliacaoLabel.pack(side=TOP)

        self.grau_avaliacao = Entry(self.frame1)
        self.grau_avaliacao["width"] = 30
        self.grau_avaliacao["font"] = self.fontePadrao
        self.grau_avaliacao.pack(side=TOP)

        self.observacoesLabel = Label(self.frame1, text="Observações", font=self.fontePadrao)
        self.observacoesLabel["pady"] = 5
        self.observacoesLabel.pack(side=TOP)

        self.observacoes = Entry(self.frame1)
        self.observacoes["width"] = 30
        self.observacoes["font"] = self.fontePadrao
        self.observacoes.pack(side=TOP)

        self.idMedicoLabel = Label(self.frame1, text="ID Médico", font=self.fontePadrao)
        self.idMedicoLabel["pady"] = 5
        self.idMedicoLabel.pack(side=TOP)

        self.idMedico = Entry(self.frame1)
        self.idMedico["width"] = 30
        self.idMedico["font"] = self.fontePadrao
        self.idMedico.pack(side=TOP)

        self.idPacienteLabel = Label(self.frame1, text="ID Paciente", font=("Arial", "10"))
        self.idPacienteLabel["pady"] = 5
        self.idPacienteLabel.pack(side=TOP)

        self.idPaciente = Entry(self.frame1)
        self.idPaciente["width"] = 30
        self.idPaciente["font"] = font=self.fontePadrao
        self.idPaciente.pack(side=TOP)

        self.idProntuarioLabel = Label(self.frame1, text="ID Prontuário", font=("Arial", "10"))
        self.idProntuarioLabel["pady"] = 5
        self.idProntuarioLabel.pack(side=TOP)

        self.idProntuario = Entry(self.frame1)
        self.idProntuario["width"] = 30
        self.idProntuario["font"] = font=self.fontePadrao
        self.idProntuario.pack(side=TOP)

        self.mensagem = Label(self.frame1, text="", font=self.fontePadrao)
        self.mensagem.pack()

        btn1 = Button(self.frame1,
                      text="Confirmar", height=1, width=40,command=lambda:
            [self.insereAtendimento(self.data.get(),self.grau_avaliacao.get(),self.observacoes.get(),self.idMedico.get(),self.idPaciente.get(),self.idProntuario.get()),change()]).pack(padx=50, pady=30)

        btn2 = Button(self.frame1,
                      text="Retornar a Tela Inicial", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacoesTelaInicial(tipo).pack()]).pack(padx=50)

        return self.frame1

    #Funcao que recebe id de atendimento a ser alterado
    def frameSimulacaoAlteraAtendimento(self,tipo):

        self.frame1 = Frame()
        self.frame1["pady"] = 20
        self.fontePadrao = ("Arial", "10")

        #Label Inicial
        self.atendimento = Label(self.frame1, text="Alteração de Atendimento")
        self.atendimento["pady"] = 5
        self.atendimento["font"] = self.fontePadrao
        self.atendimento.pack()

        #Label de ID Atendimento
        self.idLabel = Label(self.frame1, text="Selecione o ID de Atendimento", font=self.fontePadrao)
        self.idLabel["pady"] = 20
        self.idLabel.pack()

        self.id = Entry(self.frame1)
        self.id["width"] = 30
        self.id["font"] = self.fontePadrao
        self.id.pack()

        self.btn1 = Button(self.frame1,
                      text="Confirmar", height=1, width=40,command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacaoAlteraMostraAtendimento(tipo,self.id.get()).pack()]).pack(padx=50, pady=30)

        btn2 = Button(self.frame1,
                      text="Retornar a Tela Simulaçãoes", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacoesTelaInicial(tipo).pack()]).pack(padx=50, pady=30)

        return self.frame1

    #Funcao que confirma tupla a ser alterada
    def frameSimulacaoAlteraMostraAtendimento(self,tipo,id_atendimento):

        self.frame1 = Frame()
        self.frame1["pady"] = 20
        self.fontePadrao = ("Arial", "10")

        # Label de Dados
        self.info1Label = Label(self.frame1, text="", font=self.fontePadrao)
        self.info2Label = Label(self.frame1, text="", font=self.fontePadrao)
        self.info3Label = Label(self.frame1, text="", font=self.fontePadrao)
        self.info4Label = Label(self.frame1, text="", font=self.fontePadrao)
        self.info5Label = Label(self.frame1, text="", font=self.fontePadrao)
        self.info6Label = Label(self.frame1, text="", font=self.fontePadrao)
        self.info7Label = Label(self.frame1, text="", font=self.fontePadrao)

        self.mensagem = Label(self.frame1, text="", font=self.fontePadrao)
        self.mensagem.pack()

        self.info1Label.pack()
        self.info2Label.pack()
        self.info3Label.pack()
        self.info4Label.pack()
        self.info5Label.pack()
        self.info6Label.pack()
        self.info7Label.pack()

        row = database.getAtendimento(cursor, id_atendimento)

        if (row == None):
            self.mensagem['text'] = "Atendimento não encontrado"
            self.mensagem.pack()

        else:
            self.info1Label['text'] = "ID Atendimento: " + str(row[0])
            self.info2Label['text'] = "Data: " + str(row[1])
            self.info3Label['text'] = "Grau de Avaliação: " + row[2]
            self.info4Label['text'] = "Observações: " + row[3]
            self.info5Label['text'] = "ID Médico: " + str(row[4])
            self.info6Label['text'] = "ID Paciente: " + str(row[5])
            self.info7Label['text'] = "ID Prontuário: " + str(row[6])

            btn1 = Button(self.frame1,text="Confirmar", height=1, width=40,command=lambda:[self.frame1.pack_forget(),self.frameSimulacaoAlteraConfirmaAtendimento(tipo,id_atendimento).pack()]).pack(padx=50, pady=30)

        btn2 = Button(self.frame1,
                      text="Retornar a procura de Atendimento", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacaoAlteraAtendimento(tipo).pack()]).pack(padx=50, pady=30)

        return self.frame1

    #Funcao que realiza o update da tupla alterada
    def frameSimulacaoAlteraConfirmaAtendimento(self,tipo,id_atendimento):

        def change():
            messagebox.showinfo("Alteração", "Alterado com sucesso")
            self.data.delete(0, 'end')
            self.grauAvaliacao.delete(0, 'end')
            self.observacao.delete(0, 'end')

        self.frame1 = Frame()
        self.frame1["pady"] = 20
        self.fontePadrao = ("Arial", "10")

        #Label Inicial
        self.atendimento = Label(self.frame1, text="Alteração de Atendimento")
        self.atendimento["pady"] = 5
        self.atendimento["font"] = self.fontePadrao
        self.atendimento.pack()

        #Label de alteração data Atendimento
        self.dataLabel = Label(self.frame1, text="Data", font=self.fontePadrao)
        self.dataLabel["pady"] = 20
        self.dataLabel.pack()

        self.data = Entry(self.frame1)
        self.data["width"] = 30
        self.data["font"] = self.fontePadrao
        self.data.pack()

        # Label de alteração grau de avaliação Amostra
        self.grauAvaliacaoLabel = Label(self.frame1, text="Grau de Avaliação", font=self.fontePadrao)
        self.grauAvaliacaoLabel["pady"] = 20
        self.grauAvaliacaoLabel.pack()

        self.grauAvaliacao = Entry(self.frame1)
        self.grauAvaliacao["width"] = 30
        self.grauAvaliacao["font"] = self.fontePadrao
        self.grauAvaliacao.pack()

        self.observacaoLabel = Label(self.frame1, text="Observação", font=self.fontePadrao)
        self.observacaoLabel["pady"] = 20
        self.observacaoLabel.pack()

        self.observacao = Entry(self.frame1)
        self.observacao["width"] = 30
        self.observacao["font"] = self.fontePadrao
        self.observacao.pack()

        btn1 = Button(self.frame1,
                      text="Confirmar", height=1, width=40,command=lambda:
            [self.alteraAtendimento(id_atendimento,self.data.get(),self.grauAvaliacao.get(),self.observacao.get()),change()]).pack(padx=50, pady=30)

        btn2 = Button(self.frame1,
                      text="Retornar a Tela Simulaçãoes", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacoesTelaInicial(tipo).pack()]).pack(padx=50, pady=30)

        return self.frame1

#-----------------------------------------------------------------------------------

    # Prontuario

    # Função de chamada ao banco de dados - UPDATE
    def alteraProntuario(self, id_prontuario, id_paciente):
        database.updateProntuario(cursor, id_prontuario, id_paciente)

    # Funcao de chamada ao banco de dados - INSERT
    def insereProntuario(self,id_paciente):
        database.insertProntuario(cursor,id_paciente)

    # Funcao de chamada ao banco de dados - DROP AND INSERT
    def limpaProntuario(self):
        database.resetProntuario(cursor)
        messagebox.showinfo("Reset Prontuário", "Tabela Prontuário voltou ao seu estado original")

    # Funcao que mostra a tabela simulada
    def frameshowSimulacaoProntuario(self):

        self.root = Tk()
        self.root.title("Visualização Simulação Prontuário")

        self.lst = [("ID Prontuário", "ID Paciente")]
        self.list = database.showProntuario(cursor)
        for row in self.list:
            self.lst.append(row)

        total_rows = len(self.lst)
        total_columns = len(self.lst[0])

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(self.root, width=20, fg='black',font=('Arial', 12),justify=CENTER)

                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i][j])

        self.root.mainloop()

    # Funcao Forms para insercao de prontuario
    def frameSimulacaoCriaProntuario(self,tipo):

        def change():
            messagebox.showinfo("Inserção", "Inserido com sucesso")
            self.idPaciente.delete(0, 'end')

        self.frame1 = Frame()
        self.frame1["pady"] = 20
        self.fontePadrao = ("Arial", "10")

        self.prontuario = Label(self.frame1, text="Criação de Prontuário")
        self.prontuario["pady"] = 5
        self.prontuario["font"] = self.fontePadrao
        self.prontuario.pack()

        self.idPacienteLabel = Label(self.frame1, text="ID Paciente", font=("Arial", "10"))
        self.idPacienteLabel["pady"] = 5
        self.idPacienteLabel.pack(side=TOP)

        self.idPaciente = Entry(self.frame1)
        self.idPaciente["width"] = 30
        self.idPaciente["font"] = font=self.fontePadrao
        self.idPaciente.pack(side=TOP)

        self.mensagem = Label(self.frame1, text="", font=self.fontePadrao)
        self.mensagem.pack()

        btn1 = Button(self.frame1,
                      text="Confirmar", height=1, width=40,command=lambda:
            [self.insereProntuario(self.idPaciente.get()),change()]).pack(padx=50, pady=30)

        btn2 = Button(self.frame1,
                      text="Retornar a Tela Inicial", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacoesTelaInicial(tipo).pack()]).pack(padx=50, pady=30)

        return self.frame1

    # Funcao que recebe id de prontuario a ser alterado
    def frameSimulacaoAlteraProntuario(self, tipo):

        self.frame1 = Frame()
        self.frame1["pady"] = 20
        self.fontePadrao = ("Arial", "10")

        # Label Inicial
        self.amostra = Label(self.frame1, text="Alteração de Prontuário")
        self.amostra["pady"] = 5
        self.amostra["font"] = self.fontePadrao
        self.amostra.pack()

        # Label de ID AMOSTRA
        self.idLabel = Label(self.frame1, text="Selecione o ID de Prontuário", font=self.fontePadrao)
        self.idLabel["pady"] = 20
        self.idLabel.pack()

        self.id = Entry(self.frame1)
        self.id["width"] = 30
        self.id["font"] = self.fontePadrao
        self.id.pack()

        self.btn1 = Button(self.frame1,
                           text="Confirmar", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacaoAlteraMostraProntuario(tipo, self.id.get()).pack()]).pack(
            padx=50, pady=30)

        btn2 = Button(self.frame1,
                      text="Retornar a Tela Simulaçãoes", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacoesTelaInicial(tipo).pack()]).pack(padx=50, pady=30)

        return self.frame1

    # Funcao que confirma tupla a ser alterada
    def frameSimulacaoAlteraMostraProntuario(self,tipo,id_prontuario):

        self.frame1 = Frame()
        self.frame1["pady"] = 20
        self.fontePadrao = ("Arial", "10")

        # Label de Dados
        self.info1Label = Label(self.frame1, text="", font=self.fontePadrao)
        self.info2Label = Label(self.frame1, text="", font=self.fontePadrao)

        self.mensagem = Label(self.frame1, text="", font=self.fontePadrao)
        self.mensagem.pack()

        self.info1Label.pack()
        self.info2Label.pack()

        row = database.getProntuario(cursor,id_prontuario)

        if (row == None):
            self.mensagem['text'] = "Prontuário não encontrado"
            self.mensagem.pack()

        else:
            self.info1Label['text'] = "ID Prontuário: " + str(row[0])
            self.info2Label['text'] = "ID Paciente: " + str(row[1])

            btn1 = Button(self.frame1,text="Confirmar", height=1, width=40,command=lambda:[self.frame1.pack_forget(),
                                                                                           self.frameSimulacaoAlteraConfirmaProntuario(tipo,id_prontuario).pack()]).pack(padx=50, pady=30)

        btn2 = Button(self.frame1,
                      text="Retornar a procura de prontuário", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacaoAlteraProntuario(tipo).pack()]).pack(padx=50, pady=30)

        return self.frame1

    # Funcao que realiza o update da tupla alterada
    def frameSimulacaoAlteraConfirmaProntuario(self,tipo,id_prontuario):

        def change():
            messagebox.showinfo("Alteração", "Alterado com sucesso")
            self.idPaciente.delete(0, 'end')

        self.frame1 = Frame()
        self.frame1["pady"] = 20
        self.fontePadrao = ("Arial", "10")

        #Label Inicial
        self.prontuario = Label(self.frame1, text="Alteração de Prontuário")
        self.prontuario["pady"] = 5
        self.prontuario["font"] = self.fontePadrao
        self.prontuario.pack()

        #Label de alteração data Amostra
        self.idPacienteLabel = Label(self.frame1, text="ID Paciente", font=self.fontePadrao)
        self.idPacienteLabel["pady"] = 20
        self.idPacienteLabel.pack()

        self.idPaciente = Entry(self.frame1)
        self.idPaciente["width"] = 30
        self.idPaciente["font"] = self.fontePadrao
        self.idPaciente.pack()

        btn1 = Button(self.frame1,
                      text="Confirmar", height=1, width=40,command=lambda:
            [self.alteraProntuario(id_prontuario,self.idPaciente.get()),change()]).pack(padx=50, pady=30)

        btn2 = Button(self.frame1,
                      text="Retornar a Tela Simulaçãoes", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacoesTelaInicial(tipo).pack()]).pack(padx=50, pady=30)

        return self.frame1

#------------------------------------------------------------------------------

    #Amostra

    # Função de chamada ao banco de dados - UPDATE
    def alteraAmostra(self,id_amostra,data,resultado):
        database.updateAmostra(cursor,id_amostra,data,resultado)

    # Funcao de chamada ao banco de dados - INSERT
    def insereAmostra(self,data,resultado,id_laboratorio,id_paciente,id_pesquisador):
        database.insertAmostra(cursor,data, resultado, id_laboratorio, id_paciente, id_pesquisador)

    # Funcao de chamada ao banco de dados - DROP AND INSERT
    def limpaAmostra(self):
        database.resetAmostra(cursor)
        messagebox.showinfo("Reset Amostra", "Tabela Amostra voltou ao seu estado original")

    # Funcao que mostra a tabela simulada
    def frameshowSimulacaoAmostra(self):

        self.root = Tk()
        self.root.title("Visualização Simulação Amostra")

        self.lst = [("ID Amostra", "Data","Resultado","ID Laboratório","ID Paciente","ID Pesquisador")]
        self.list = database.showAmostra(cursor)
        for row in self.list:
            self.lst.append(row)

        total_rows = len(self.lst)
        total_columns = len(self.lst[0])

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(self.root, width=20, fg='black',font=('Arial', 12),justify=CENTER)

                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i][j])

        self.root.mainloop()

    # Funcao Forms para insercao de amostra
    def frameSimulacaoCriaAmostra(self,tipo):

        def change():
            messagebox.showinfo("Inserção", "Inserido com sucesso")
            self.data.delete(0, 'end')
            self.resultado.delete(0, 'end')
            self.idLaboratorio.delete(0, 'end')
            self.idPesquisador.delete(0, 'end')
            self.idPaciente.delete(0, 'end')

        self.frame1 = Frame()
        self.frame1["pady"] = 20
        self.fontePadrao = ("Arial", "10")

        self.amostra = Label(self.frame1, text="Criação de Amostra")
        self.amostra["pady"] = 5
        self.amostra["font"] = self.fontePadrao
        self.amostra.pack()

        self.dataLabel = Label(self.frame1, text="Data", font=self.fontePadrao)
        self.dataLabel["pady"] = 5
        self.dataLabel.pack(side=TOP)

        self.data = Entry(self.frame1)
        self.data["width"] = 30
        self.data["font"] = self.fontePadrao
        self.data.pack(side=TOP)

        self.resultadoLabel = Label(self.frame1, text="Resultado", font=self.fontePadrao)
        self.resultadoLabel["pady"] = 5
        self.resultadoLabel.pack(side=TOP)

        self.resultado = Entry(self.frame1)
        self.resultado["width"] = 30
        self.resultado["font"] = self.fontePadrao
        self.resultado.pack(side=TOP)

        self.idLaboratorioLabel = Label(self.frame1, text="ID Laboratório", font=self.fontePadrao)
        self.idLaboratorioLabel["pady"] = 5
        self.idLaboratorioLabel.pack(side=TOP)

        self.idLaboratorio = Entry(self.frame1)
        self.idLaboratorio["width"] = 30
        self.idLaboratorio["font"] = self.fontePadrao
        self.idLaboratorio.pack(side=TOP)

        self.idPacienteLabel = Label(self.frame1, text="ID Paciente", font=("Arial", "10"))
        self.idPacienteLabel["pady"] = 5
        self.idPacienteLabel.pack(side=TOP)

        self.idPaciente = Entry(self.frame1)
        self.idPaciente["width"] = 30
        self.idPaciente["font"] = font=self.fontePadrao
        self.idPaciente.pack(side=TOP)

        self.idPesquisadorLabel = Label(self.frame1, text="ID Pesquisador", font=("Arial", "10"))
        self.idPesquisadorLabel["pady"] = 5
        self.idPesquisadorLabel.pack(side=TOP)

        self.idPesquisador = Entry(self.frame1)
        self.idPesquisador["width"] = 30
        self.idPesquisador["font"] = font=self.fontePadrao
        self.idPesquisador.pack(side=TOP)

        self.mensagem = Label(self.frame1, text="", font=self.fontePadrao)
        self.mensagem.pack()

        btn1 = Button(self.frame1,
                      text="Confirmar", height=1, width=40,command=lambda:
            [self.insereAmostra(self.data.get(),self.resultado.get(),self.idLaboratorio.get(),self.idPaciente.get(),self.idPesquisador.get()),change()]).pack(padx=50, pady=30)

        btn2 = Button(self.frame1,
                      text="Retornar a Tela Inicial", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacoesTelaInicial(tipo).pack()]).pack(padx=50, pady=30)

        return self.frame1

    # Funcao que recebe id de amostra a ser alterado
    def frameSimulacaoAlteraAmostra(self,tipo):

        self.frame1 = Frame()
        self.frame1["pady"] = 20
        self.fontePadrao = ("Arial", "10")

        #Label Inicial
        self.amostra = Label(self.frame1, text="Alteração de Amostra")
        self.amostra["pady"] = 5
        self.amostra["font"] = self.fontePadrao
        self.amostra.pack()

        #Label de ID AMOSTRA
        self.idLabel = Label(self.frame1, text="Selecione o ID de Amostra", font=self.fontePadrao)
        self.idLabel["pady"] = 20
        self.idLabel.pack()

        self.id = Entry(self.frame1)
        self.id["width"] = 30
        self.id["font"] = self.fontePadrao
        self.id.pack()

        self.btn1 = Button(self.frame1,
                      text="Confirmar", height=1, width=40,command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacaoAlteraMostraAmostra(tipo,self.id.get()).pack()]).pack(padx=50, pady=30)

        btn2 = Button(self.frame1,
                      text="Retornar a Tela Simulaçãoes", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacoesTelaInicial(tipo).pack()]).pack(padx=50, pady=30)

        return self.frame1

    # Funcao que confirma tupla a ser alterada
    def frameSimulacaoAlteraMostraAmostra(self,tipo,id_amostra):

        self.frame1 = Frame()
        self.frame1["pady"] = 20
        self.fontePadrao = ("Arial", "10")

        # Label de Dados
        self.info1Label = Label(self.frame1, text="", font=self.fontePadrao)
        self.info2Label = Label(self.frame1, text="", font=self.fontePadrao)
        self.info3Label = Label(self.frame1, text="", font=self.fontePadrao)
        self.info4Label = Label(self.frame1, text="", font=self.fontePadrao)
        self.info5Label = Label(self.frame1, text="", font=self.fontePadrao)
        self.info6Label = Label(self.frame1, text="", font=self.fontePadrao)

        self.mensagem = Label(self.frame1, text="", font=self.fontePadrao)
        self.mensagem.pack()

        self.info1Label.pack()
        self.info2Label.pack()
        self.info3Label.pack()
        self.info4Label.pack()
        self.info5Label.pack()
        self.info6Label.pack()

        row = database.getAmostra(cursor, id_amostra)

        if (row == None):
            self.mensagem['text'] = "Amostra não encontrada"
            self.mensagem.pack()

        else:
            self.info1Label['text'] = "ID Amostra: " + str(row[0])
            self.info2Label['text'] = "Data: " + str(row[1])
            self.info3Label['text'] = "Resultado: " + row[2]
            self.info4Label['text'] = "ID Laboratório: " + str(row[3])
            self.info5Label['text'] = "ID Paciente: " + str(row[4])
            self.info6Label['text'] = "ID Pesquisador: " + str(row[5])

            btn1 = Button(self.frame1,text="Confirmar", height=1, width=40,command=lambda:[self.frame1.pack_forget(),self.frameSimulacaoAlteraConfirmaAmostra(tipo,id_amostra).pack()]).pack(padx=50, pady=30)

        btn2 = Button(self.frame1,
                      text="Retornar a procura de Amostra", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacaoAlteraAmostra(tipo).pack()]).pack(padx=50, pady=30)

        return self.frame1

    # Funcao que realiza o update da tupla alterada
    def frameSimulacaoAlteraConfirmaAmostra(self,tipo,id_amostra):

        def change():
            messagebox.showinfo("Alteração", "Alterado com sucesso")
            self.data.delete(0, 'end')
            self.resultado.delete(0, 'end')

        self.frame1 = Frame()
        self.frame1["pady"] = 20
        self.fontePadrao = ("Arial", "10")

        #Label Inicial
        self.amostra = Label(self.frame1, text="Alteração de Amostra")
        self.amostra["pady"] = 5
        self.amostra["font"] = self.fontePadrao
        self.amostra.pack()

        #Label de alteração data Amostra
        self.dataLabel = Label(self.frame1, text="Data", font=self.fontePadrao)
        self.dataLabel["pady"] = 20
        self.dataLabel.pack()

        self.data = Entry(self.frame1)
        self.data["width"] = 30
        self.data["font"] = self.fontePadrao
        self.data.pack()

        # Label de alteração data Amostra
        self.resultadoLabel = Label(self.frame1, text="Resultado", font=self.fontePadrao)
        self.resultadoLabel["pady"] = 20
        self.resultadoLabel.pack()

        self.resultado = Entry(self.frame1)
        self.resultado["width"] = 30
        self.resultado["font"] = self.fontePadrao
        self.resultado.pack()

        btn1 = Button(self.frame1,
                      text="Confirmar", height=1, width=40,command=lambda:
            [self.alteraAmostra(id_amostra,self.data.get(),self.resultado.get()),change()]).pack(padx=50, pady=30)

        btn2 = Button(self.frame1,
                      text="Retornar a Tela Simulaçãoes", height=1, width=40, command=lambda:
            [self.frame1.pack_forget(), self.frameSimulacoesTelaInicial(tipo).pack()]).pack(padx=50, pady=30)

        return self.frame1


#################################################################################
    def __init__(self, root, user, tipo):

        self.root = root
        self.root.geometry("600x680")
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