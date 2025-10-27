import wx
import json
import os
import globalPluginHandler

class NotasStorage:

    def __init__(self, pluginRef, arquivo="dados/notas.json"):
        self.pluginRef = pluginRef  
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
        self.notas.append(nota)
        self.salvarNotas()

    def exibirNotas(self):
        if not self.notas:
            wx.MessageBox(
                "Você não tem anotações salvas!",
                "Aviso",
                wx.OK | wx.ICON_INFORMATION
            )
            wx.CallLater(0, self.pluginRef.exibirMenu)
            return

        self.frame = wx.Frame(None, title="Notas Salvas", size=(600, 400))
        panel = wx.Panel(self.frame)
        sizer = wx.BoxSizer(wx.VERTICAL)

        for i, nota in enumerate(self.notas):
            btn_nota = wx.Button(panel, label=f"{i + 1}. {nota['titulo']}")
            btn_nota.Bind(wx.EVT_BUTTON, lambda event, n=nota: self.mostrarNota(n))
            sizer.Add(btn_nota, flag=wx.EXPAND | wx.ALL, border=5)

        btn_menu = wx.Button(panel, label="Voltar ao Menu")
        btn_menu.Bind(wx.EVT_BUTTON, lambda event: self.voltarAoMenu())
        sizer.Add(btn_menu, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        btn_fechar = wx.Button(panel, label="Fechar")
        btn_fechar.Bind(wx.EVT_BUTTON, lambda event: self.frame.Close())
        sizer.Add(btn_fechar, flag=wx.ALIGN_CENTER | wx.TOP, border=20)

        panel.SetSizer(sizer)
        self.frame.Show()

    def voltarAoMenu(self):
        """Fecha a tela de notas e exibe o menu principal do plugin."""
        if hasattr(self, "frame") and self.frame:
            self.frame.Close()
        wx.CallLater(0, self.pluginRef.exibirMenu)

    def mostrarNota(self, nota):
        """Exibe o conteúdo de uma nota e permite edição e exclusão."""
        frame = wx.Frame(None, title=f"Nota: {nota['titulo']}", size=(600, 500))
        panel = wx.Panel(frame)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.frame.Close()

        conteudo = f"Título: {nota['titulo']}\nVersão: {nota['versao']}\n"
        conteudo += f"{nota['livro']} {nota['capitulo']}\n\n"
        if nota.get('versiculos'):
            conteudo += "Versículos:\n" + "\n".join([f"{v['numero']}. {v['texto']}" for v in nota['versiculos']]) + "\n\n"
        conteudo += f"Descrição:\n{nota['descricao']}"

        txt_conteudo = wx.TextCtrl(panel, value=conteudo, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        sizer.Add(txt_conteudo, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        btn_editar = wx.Button(panel, label="Editar")
        btn_excluir = wx.Button(panel, label="Excluir")
        btn_lista = wx.Button(panel, label="Lista de Notas")
        btn_fechar = wx.Button(panel, label="Fechar")

        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)
        sizer_botoes.Add(btn_editar, flag=wx.RIGHT, border=5)
        sizer_botoes.Add(btn_excluir, flag=wx.LEFT, border=5)
        sizer_botoes.Add(btn_lista, flag=wx.LEFT, border=5)  
        sizer_botoes.Add(btn_fechar, flag=wx.LEFT, border=5)
        sizer.Add(sizer_botoes, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        def habilitarEdicao(event):
            """Habilita a edição da nota."""
            btn_lista.Hide()

            txt_conteudo.SetEditable(True)
            txt_conteudo.SetStyle(0, txt_conteudo.GetLastPosition(), wx.TextAttr(wx.Colour(0, 0, 0)))  
            btn_editar.Hide()
            btn_excluir.Hide()
            btn_fechar.Hide()

            btn_salvar = wx.Button(panel, label="Salvar Alteração")
            btn_cancelar = wx.Button(panel, label="Cancelar")
            sizer_botoes.Add(btn_salvar, flag=wx.RIGHT, border=5)
            sizer_botoes.Add(btn_cancelar, flag=wx.LEFT, border=5)
            panel.Layout()

            def salvarAlteracao(event):
                """Salva a alteração feita na nota."""
                novo_conteudo = txt_conteudo.GetValue()
                linhas = novo_conteudo.split("\n")
                nota['descricao'] = "\n".join(linhas[-1:])  
                self.salvarNotas()  
                wx.MessageBox("Alteração salva com sucesso!", "Sucesso", wx.OK | wx.ICON_INFORMATION)
                txt_conteudo.SetEditable(False)
                btn_salvar.Hide()
                btn_cancelar.Hide()
                btn_editar.Show()
                btn_excluir.Show()
                btn_fechar.Show()
                btn_lista.Show()  
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
                btn_lista.Show()  
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
                self.notas.remove(nota)  
                self.salvarNotas()  
                wx.MessageBox("Nota excluída com sucesso!", "Sucesso", wx.OK | wx.ICON_INFORMATION)
                frame.Close()  
                self.exibirNotas()  

        btn_excluir.Bind(wx.EVT_BUTTON, excluirNota)

        def voltarParaLista(event):
            """Fecha a janela de conteúdo e abre a lista de notas novamente."""
            frame.Close()
            self.exibirNotas()  

        btn_lista.Bind(wx.EVT_BUTTON, voltarParaLista)  

        btn_fechar.Bind(wx.EVT_BUTTON, lambda event: frame.Close())

        panel.SetSizer(sizer)
        frame.Show()


class NotasManager:
    def __init__(self, versao, livro, capitulo, versiculos, pluginRef):
        self.versao = versao
        self.livro = livro
        self.capitulo = capitulo
        self.versiculos = versiculos
        self.selecionados = []
        
        self.notasStorage = NotasStorage(pluginRef)
        self.exibirTituloNota(None)

    def exibirSelecaoVersiculos(self):
        frame = wx.Frame(None, title=f"Selecione os versículos - {self.livro} {self.capitulo}", size=(600, 400))
        panel = wx.Panel(frame)

        
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.checkbox_list = []  

        
        for i, texto in enumerate(self.versiculos):
            checkbox = wx.CheckBox(panel, label=f"{i + 1}. {texto}")
            self.checkbox_list.append(checkbox)
            sizer.Add(checkbox, flag=wx.TOP | wx.LEFT, border=10)

        
        btn_avancar = wx.Button(panel, label="Avançar")
        btn_avancar.Bind(wx.EVT_BUTTON, lambda event: self.exibirTituloNota(frame))

        
        btn_cancelar = wx.Button(panel, label="Cancelar")
        btn_cancelar.Bind(wx.EVT_BUTTON, lambda event: frame.Close())

        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(btn_cancelar, flag=wx.RIGHT, border=10)
        btn_sizer.Add(btn_avancar)

        
        sizer.Add(btn_sizer, flag=wx.ALIGN_CENTER | wx.TOP, border=20)
        panel.SetSizer(sizer)
        frame.Show()

        
        for checkbox in self.checkbox_list:
            checkbox.Bind(wx.EVT_CHECKBOX, lambda event: self.ativarBotaoAvancar(btn_avancar))

    def ativarBotaoAvancar(self, btn_avancar):
        """Ativa o botão de avançar quando pelo menos um versículo for selecionado."""
        if any(checkbox.IsChecked() for checkbox in self.checkbox_list):
            btn_avancar.Enable(True)  
        else:
            btn_avancar.Enable(False)  

    def exibirTituloNota(self, frame_anterior):
        """Exibe a caixa para o usuário inserir o título da nota usando wx.TextEntryDialog.

        Se nenhuma seleção de versículos ocorreu, segue sem versículos.
        """
        if frame_anterior is not None:
            try:
                self.selecionados = [
                    (i + 1, self.versiculos[i])
                    for i, checkbox in enumerate(self.checkbox_list)
                    if checkbox.IsChecked()
                ]
                frame_anterior.Destroy()
            except Exception:
                self.selecionados = []
        else:
            self.selecionados = []

        dialog = wx.TextEntryDialog(None, "Digite o título da sua nota:", "Título da Nota", "", style=wx.OK | wx.CANCEL)

        if dialog.ShowModal() == wx.ID_OK:
            titulo = dialog.GetValue()

            if not titulo.strip():
                wx.MessageBox("O título não pode estar vazio.", "Erro", wx.OK | wx.ICON_ERROR)
                dialog.Destroy()
                return

            dialog.Destroy()

            self.exibirNotaEditavel(titulo)

    def exibirNotaEditavel(self, titulo):
        """Exibe uma janela editável com a nota completa."""
        frame = wx.Frame(None, title="Editar Nota", size=(600, 400))
        panel = wx.Panel(frame)

        conteudo = f"{titulo}\nVersão: {self.versao}\n{self.livro} {self.capitulo}\n\n"
        if self.selecionados:
            conteudo += "\n".join([f"{num}. {texto}" for num, texto in self.selecionados]) + "\n\n"
        conteudo += "Adicione suas anotações aqui."

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.txt_nota = wx.TextCtrl(panel, value=conteudo, style=wx.TE_MULTILINE | wx.HSCROLL)
        sizer.Add(self.txt_nota, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        btn_salvar = wx.Button(panel, label="Salvar Nota")
        btn_salvar.Bind(wx.EVT_BUTTON, lambda event: self.salvarNota(btn_salvar))
        
        btn_cancelar = wx.Button(panel, label="Cancelar")
        btn_cancelar.Bind(wx.EVT_BUTTON, lambda event: self.fecharJanela(frame))

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

        caminho = os.path.join(os.path.dirname(__file__), "dados", "notas.json")
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
        else:
            dados = []

        dados.append(nota)

        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        wx.MessageBox("Nota salva com sucesso!", "Confirmação", wx.OK | wx.ICON_INFORMATION)

        frame_atual = btn_salvar.GetParent().GetTopLevelParent()
        frame_atual.Destroy()

