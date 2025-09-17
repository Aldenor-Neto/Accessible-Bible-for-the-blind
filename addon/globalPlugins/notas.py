import wx
import json
import os
import globalPluginHandler

from . import init


class NotasStorage:

    def __init__(self, arquivo="dados/notas.json"):
        self.caminho = os.path.join(os.path.dirname(__file__), arquivo)
        self.notas = self.carregarNotas()

    def carregarNotas(self):
        if os.path.exists(self.caminho):
            with open(self.caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def salvarNotas(self):
        try:
            with open(self.caminho, "w", encoding="utf-8") as arquivo:
                json.dump(self.notas, arquivo, ensure_ascii=False, indent=4)
        except Exception as e:
            wx.MessageBox(f"Erro ao salvar as notas: {str(e)}", "Erro", wx.OK | wx.ICON_ERROR)

    def adicionarNota(self, nota):
        """Adiciona uma nova nota ao armazenamento."""
        self.notas.append(nota)
        self.salvarNotas()

    def exibirNotas(self):
        if not self.notas:
            wx.MessageBox(
                "Você não tem anotações salvas!",
                "Aviso",
                wx.OK | wx.ICON_INFORMATION
            )

            menu = init.GlobalPlugin()
            menu.exibirMenu()
            return

        self.frame = wx.Frame(None, title="Notas Salvas", size=(600, 400))
        panel = wx.Panel(self.frame)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Adiciona um botão para cada nota
        for i, nota in enumerate(self.notas):
            btn_nota = wx.Button(panel, label=f"{i + 1}. {nota['titulo']}")
            btn_nota.Bind(wx.EVT_BUTTON, lambda event, n=nota: self.mostrarNota(n))
            sizer.Add(btn_nota, flag=wx.EXPAND | wx.ALL, border=5)

        # Botão para fechar
        btn_fechar = wx.Button(panel, label="Fechar")
        btn_fechar.Bind(wx.EVT_BUTTON, lambda event: self.frame.Close())
        sizer.Add(btn_fechar, flag=wx.ALIGN_CENTER | wx.TOP, border=20)

        panel.SetSizer(sizer)
        self.frame.Show()

    def mostrarNota(self, nota):
        """Exibe o conteúdo de uma nota e permite edição e exclusão."""
        frame = wx.Frame(None, title=f"Nota: {nota['titulo']}", size=(600, 500))
        panel = wx.Panel(frame)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.frame.Close()

        # Conteúdo inicial da nota
        conteudo = f"Título: {nota['titulo']}\nVersão: {nota['versao']}\n"
        conteudo += f"{nota['livro']} {nota['capitulo']}\n\n"
        if nota.get('versiculos'):
            conteudo += "Versículos:\n" + "\n".join([f"{v['numero']}. {v['texto']}" for v in nota['versiculos']]) + "\n\n"
        conteudo += f"Descrição:\n{nota['descricao']}"

        # Caixa de texto inicialmente não editável
        txt_conteudo = wx.TextCtrl(panel, value=conteudo, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        sizer.Add(txt_conteudo, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Botões para ações
        btn_editar = wx.Button(panel, label="Editar")
        btn_excluir = wx.Button(panel, label="Excluir")
        btn_lista = wx.Button(panel, label="Lista de Notas")
        btn_fechar = wx.Button(panel, label="Fechar")

        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)
        sizer_botoes.Add(btn_editar, flag=wx.RIGHT, border=5)
        sizer_botoes.Add(btn_excluir, flag=wx.LEFT, border=5)
        sizer_botoes.Add(btn_lista, flag=wx.LEFT, border=5)  # Adiciona o botão para voltar à lista
        sizer_botoes.Add(btn_fechar, flag=wx.LEFT, border=5)
        sizer.Add(sizer_botoes, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        def habilitarEdicao(event):
            """Habilita a edição da nota."""
            # Oculta o botão "Lista de Notas" durante a edição
            btn_lista.Hide()

            txt_conteudo.SetEditable(True)
            txt_conteudo.SetStyle(0, txt_conteudo.GetLastPosition(), wx.TextAttr(wx.Colour(0, 0, 0)))  # Torna texto preto (ativo)
            btn_editar.Hide()
            btn_excluir.Hide()
            btn_fechar.Hide()

            # Adiciona botões de salvar e cancelar
            btn_salvar = wx.Button(panel, label="Salvar Alteração")
            btn_cancelar = wx.Button(panel, label="Cancelar")
            sizer_botoes.Add(btn_salvar, flag=wx.RIGHT, border=5)
            sizer_botoes.Add(btn_cancelar, flag=wx.LEFT, border=5)
            panel.Layout()

            def salvarAlteracao(event):
                """Salva a alteração feita na nota."""
                novo_conteudo = txt_conteudo.GetValue()
                linhas = novo_conteudo.split("\n")
                nota['descricao'] = "\n".join(linhas[-1:])  # Atualiza apenas a descrição no dicionário
                self.salvarNotas()  # Persiste as alterações no JSON
                wx.MessageBox("Alteração salva com sucesso!", "Sucesso", wx.OK | wx.ICON_INFORMATION)
                txt_conteudo.SetEditable(False)
                btn_salvar.Hide()
                btn_cancelar.Hide()
                btn_editar.Show()
                btn_excluir.Show()
                btn_fechar.Show()
                btn_lista.Show()  # Exibe novamente o botão "Lista de Notas"
                panel.Layout()

            def cancelarAlteracao(event):
                """Cancela a alteração e restaura o conteúdo original."""
                txt_conteudo.SetValue(conteudo)
                txt_conteudo.SetEditable(False)
                btn_salvar.Hide()
                btn_cancelar.Hide()
                btn_editar.Show()
                btn_excluir.Show()
                btn_fechar.Show()
                btn_lista.Show()  # Exibe novamente o botão "Lista de Notas"
                panel.Layout()

            btn_salvar.Bind(wx.EVT_BUTTON, salvarAlteracao)
            btn_cancelar.Bind(wx.EVT_BUTTON, cancelarAlteracao)

        btn_editar.Bind(wx.EVT_BUTTON, habilitarEdicao)

        def excluirNota(event):
            """Exclui a nota após confirmação e volta para a lista de notas."""
            dialogo = wx.MessageDialog(frame,
                                    "Deseja realmente excluir esta nota? Esta ação não poderá ser desfeita.",
                                    "Confirmar Exclusão", wx.YES_NO | wx.ICON_WARNING)
            if dialogo.ShowModal() == wx.ID_YES:
                self.notas.remove(nota)  # Remove a nota da lista
                self.salvarNotas()  # Salva a lista atualizada no JSON
                wx.MessageBox("Nota excluída com sucesso!", "Sucesso", wx.OK | wx.ICON_INFORMATION)
                frame.Close()  # Fecha a janela atual da nota
                self.exibirNotas()  # Reabre a lista de notas

        btn_excluir.Bind(wx.EVT_BUTTON, excluirNota)

        def voltarParaLista(event):
            """Fecha a janela de conteúdo e abre a lista de notas novamente."""
            frame.Close()
            self.exibirNotas()  # Exibe novamente a lista de notas salvas

        btn_lista.Bind(wx.EVT_BUTTON, voltarParaLista)  # Vincula a ação ao botão

        btn_fechar.Bind(wx.EVT_BUTTON, lambda event: frame.Close())

        panel.SetSizer(sizer)
        frame.Show()


class NotasManager:
    """Gerencia o fluxo de criação de notas."""

    def __init__(self, versao, livro, capitulo, versiculos):
        self.versao = versao
        self.livro = livro
        self.capitulo = capitulo
        self.versiculos = versiculos  # Todos os versículos do capítulo
        self.selecionados = []  # Para armazenar os versículos escolhidos
        self.notasStorage = NotasStorage()  # Instancia o gerenciador de notas

        # Inicia fluxo direto no título (sem seleção de versículos)
        self.exibirTituloNota(None)

    def exibirSelecaoVersiculos(self):
        frame = wx.Frame(None, title=f"Selecione os versículos - {self.livro} {self.capitulo}", size=(600, 400))
        panel = wx.Panel(frame)

        # Layout principal
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.checkbox_list = []  # Armazena as checkboxes

        # Adiciona as checkboxes para cada versículo
        for i, texto in enumerate(self.versiculos):
            checkbox = wx.CheckBox(panel, label=f"{i + 1}. {texto}")
            self.checkbox_list.append(checkbox)
            sizer.Add(checkbox, flag=wx.TOP | wx.LEFT, border=10)

        # Botão para avançar
        btn_avancar = wx.Button(panel, label="Avançar")
        btn_avancar.Bind(wx.EVT_BUTTON, lambda event: self.exibirTituloNota(frame))

        # Botão de cancelar
        btn_cancelar = wx.Button(panel, label="Cancelar")
        btn_cancelar.Bind(wx.EVT_BUTTON, lambda event: frame.Close())

        # Layout para os botões
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(btn_cancelar, flag=wx.RIGHT, border=10)
        btn_sizer.Add(btn_avancar)

        # Adiciona o layout principal e o layout dos botões ao painel
        sizer.Add(btn_sizer, flag=wx.ALIGN_CENTER | wx.TOP, border=20)
        panel.SetSizer(sizer)
        frame.Show()

        # Habilita o botão de "Avançar" após selecionar pelo menos um versículo
        for checkbox in self.checkbox_list:
            checkbox.Bind(wx.EVT_CHECKBOX, lambda event: self.ativarBotaoAvancar(btn_avancar))

    def ativarBotaoAvancar(self, btn_avancar):
        """Ativa o botão de avançar quando pelo menos um versículo for selecionado."""
        if any(checkbox.IsChecked() for checkbox in self.checkbox_list):
            btn_avancar.Enable(True)  # Habilita o botão de "Avançar"
        else:
            btn_avancar.Enable(False)  # Desabilita o botão caso nenhuma checkbox esteja marcada

    def exibirTituloNota(self, frame_anterior):
        """Exibe a caixa para o usuário inserir o título da nota usando wx.TextEntryDialog.

        Se nenhuma seleção de versículos ocorreu, segue sem versículos.
        """
        # Se vier de uma tela anterior (seleção), fecha-a; caso contrário, ignora
        if frame_anterior is not None:
            try:
                # Coleta os versículos selecionados quando houver checkboxes
                self.selecionados = [
                    (i + 1, self.versiculos[i])
                    for i, checkbox in enumerate(self.checkbox_list)
                    if checkbox.IsChecked()
                ]
                frame_anterior.Destroy()
            except Exception:
                # Se não houver checkboxes, mantém selecionados como lista vazia
                self.selecionados = []
        else:
            # Fluxo direto: nenhum versículo selecionado
            self.selecionados = []

        # Usa wx.TextEntryDialog para coletar o título da nota
        dialog = wx.TextEntryDialog(None, "Digite o título da sua nota:", "Título da Nota", "", style=wx.OK | wx.CANCEL)

        if dialog.ShowModal() == wx.ID_OK:
            titulo = dialog.GetValue()

            # Verifica se o título foi fornecido
            if not titulo.strip():
                wx.MessageBox("O título não pode estar vazio.", "Erro", wx.OK | wx.ICON_ERROR)
                dialog.Destroy()
                return

            # Fecha o diálogo de entrada de título
            dialog.Destroy()

            # Exibe a próxima tela de edição da nota
            self.exibirNotaEditavel(titulo)

    def exibirNotaEditavel(self, titulo):
        """Exibe uma janela editável com a nota completa."""
        frame = wx.Frame(None, title="Editar Nota", size=(600, 400))
        panel = wx.Panel(frame)

        # Conteúdo inicial da nota
        conteudo = f"{titulo}\nVersão: {self.versao}\n{self.livro} {self.capitulo}\n\n"
        if self.selecionados:
            conteudo += "\n".join([f"{num}. {texto}" for num, texto in self.selecionados]) + "\n\n"
        conteudo += "Adicione suas anotações aqui."

        # Janela para edição
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.txt_nota = wx.TextCtrl(panel, value=conteudo, style=wx.TE_MULTILINE | wx.HSCROLL)
        sizer.Add(self.txt_nota, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Botões para salvar ou cancelar a nota
        btn_salvar = wx.Button(panel, label="Salvar Nota")
        btn_salvar.Bind(wx.EVT_BUTTON, lambda event: self.salvarNota(btn_salvar))
        
        btn_cancelar = wx.Button(panel, label="Cancelar")
        btn_cancelar.Bind(wx.EVT_BUTTON, lambda event: self.fecharJanela(frame))

        # Adiciona os botões ao layout
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(btn_salvar, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        btn_sizer.Add(btn_cancelar, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.Add(btn_sizer, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        panel.SetSizer(sizer)
        frame.Show()

    def fecharJanela(self, frame):
        """Fecha a janela de edição sem salvar as alterações."""
        frame.Destroy()

    def salvarNota(self, btn_salvar):
        """Salva a nota no arquivo JSON e retorna à lista de anotações."""
        titulo = self.txt_nota.GetValue().split("\n")[0]
        descricao = self.txt_nota.GetValue().split("\n\n")[-1]
        nota = {
            "titulo": titulo,
            "versao": self.versao,
            "livro": self.livro,
            "capitulo": self.capitulo,
            "versiculos": [{"numero": num, "texto": texto} for num, texto in self.selecionados],
            "descricao": descricao.strip(),
        }

        # Caminho do arquivo JSON
        caminho = os.path.join(os.path.dirname(__file__), "dados", "notas.json")
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
        else:
            dados = []

        # Adiciona a nova nota
        dados.append(nota)

        # Salva no arquivo
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        # Exibe a mensagem de sucesso
        wx.MessageBox("Nota salva com sucesso!", "Confirmação", wx.OK | wx.ICON_INFORMATION)

        # Fecha a janela atual
        frame_atual = btn_salvar.GetParent().GetTopLevelParent()
        frame_atual.Destroy()

        # Exibe a lista de notas
        #self.notasStorage.exibirNotas()
#