import ui
import globalPluginHandler
import wx
import os
import json

from . import notas
from .__init__ import GlobalPlugin
from .progress import ReadingProgressManager
from .busca import BuscaBiblica


class Biblias:
    def __init__(self):
        self.progress_manager = ReadingProgressManager()

        self.json_files = {
            "Pastoral": "catolica - pastoral.json",
            "Ave Maria": "catolica - Ave Maria.json",
            "Jerusalém": "catolica - jerusalem.json",
            "CNBB": "catolica - CNBB.json",
            "Almeida Corrigida e Fiel(ACF)": "evangelica - Almeida Corrigida e Fiel(ACF).json",
            "Almeida Revista Atualizada(ARA)": "evangelica - Almeida Revista Atualizada(ARA).json",
            "Almeida Revista e Corrigida(ARC)": "evangelica - Almeida Revista e corrigida(ARC).json",
            "Nova Versão Internacional(NVI)": "evangelica - Nova Versão Internacional(NVI).json",
            "Nova Tradução na Linguagem de Hoje(NTLH)": "evangelica - Nova Tradução na Linguagem de Hoje(NTLH).json",
            "Tradução do novo mundo": "testemunha de jeova - traducao do novo mundo.json"
        }
    
    def script_openBible(self):
        self.menuBiblia()
    
    
    
    def continuarLeitura(self, frame_para_fechar=None):
        """Continua a leitura de onde o usuário parou.

        Se uma janela (frame) de seleção estiver aberta, fecha antes de abrir a leitura.
        """
        progresso_atual = self.progress_manager.get_progress()
        if not progresso_atual:
            wx.MessageBox("Nenhum progresso de leitura encontrado.", "Aviso", wx.OK | wx.ICON_INFORMATION)
            return
        
        try:
            # Fecha a janela de seleção, se fornecida
            if frame_para_fechar is not None:
                try:
                    frame_para_fechar.Destroy()
                except Exception:
                    pass

            # Carrega a versão da Bíblia
            versao = progresso_atual["versao"]
            self.versao_selecionada = versao
            caminho_arquivo = os.path.join(os.path.dirname(__file__), "dados", "versions", self.json_files[versao])
            
            with open(caminho_arquivo, "r", encoding="utf-8-sig") as f:
                self.biblia = json.load(f)
                self.livros = [livro["name"] for livro in self.biblia]
            
            # Encontra o livro
            livro_nome = progresso_atual["livro"]
            for i, livro in enumerate(self.biblia):
                if livro["name"] == livro_nome:
                    self.livro_selecionado = livro
                    self.capitulo_selecionado = progresso_atual["capitulo"] - 1  # Converte para 0-based
                    self.versiculo_inicial = progresso_atual["versiculo"] - 1  # Converte para 0-based
                    wx.CallAfter(self.exibirCapitulo)
                    return
            
            wx.MessageBox(f"Livro '{livro_nome}' não encontrado na versão atual.", "Erro", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"Erro ao continuar leitura: {e}", "Erro", wx.OK | wx.ICON_ERROR)


    def selecionaVersao(self):
        """Exibe uma interface com botões que abrem menus para selecionar a versão da Bíblia."""
        frame = wx.Frame(None, title="Selecione a Versão da Bíblia", size=(400, 350))
        panel = wx.Panel(frame)

        # Dados organizados por religião
        religioes = {
            "Católica": [
                "Pastoral",
                "Ave Maria",
                "Jerusalém",
                "CNBB"
            ],
            "Evangélica": [
                "Almeida Corrigida e Fiel(ACF)",
                "Almeida Revista Atualizada(ARA)",
                "Almeida Revista e Corrigida(ARC)",
                "Nova Versão Internacional(NVI)",
                "Nova Tradução na Linguagem de Hoje(NTLH)"
            ],
            "Testemunha de Jeová": [
                "Tradução do novo mundo"
            ]
        }

        # Mapeamento de arquivos
        self.json_files = {
            "Pastoral": "catolica - pastoral.json",
            "Ave Maria": "catolica - Ave Maria.json",
            "Jerusalém": "catolica - jerusalem.json",
            "CNBB": "catolica - CNBB.json",
            "Almeida Corrigida e Fiel(ACF)": "evangelica - Almeida Corrigida e Fiel(ACF).json",
            "Almeida Revista Atualizada(ARA)": "evangelica - Almeida Revista Atualizada(ARA).json",
            "Almeida Revista e Corrigida(ARC)": "evangelica - Almeida Revista e corrigida(ARC).json",
            "Nova Versão Internacional(NVI)": "evangelica - Nova Versão Internacional(NVI).json",
            "Nova Tradução na Linguagem de Hoje(NTLH)": "evangelica - Nova Tradução na Linguagem de Hoje(NTLH).json",
            "Tradução do novo mundo": "testemunha de jeova - traducao do novo mundo.json"
        }

        # Layout principal
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Criar botões para cada religião
        for religiao, versoes in religioes.items():
            btn_religiao = wx.Button(panel, label=religiao)

            # Menu para as versões da religião
            menu = wx.Menu()
            for versao in versoes:
                item_versao = menu.Append(wx.ID_ANY, versao)
                # Vincular evento para selecionar a versão
                frame.Bind(wx.EVT_MENU, lambda event, v=versao: self.selecionarVersao(v, frame), item_versao)

            # Associar o menu ao botão
            btn_religiao.Bind(wx.EVT_BUTTON, lambda event, m=menu: self.exibirMenu(event.GetEventObject(), m))

            # Adicionar o botão ao layout
            sizer.Add(btn_religiao, flag=wx.ALL | wx.EXPAND, border=10)

        panel.SetSizer(sizer)
        frame.Show()

    def menuBiblia(self):
        frame = wx.Frame(None, title="Bíblia", size=(450, 250))
        panel = wx.Panel(frame)

        sizer = wx.BoxSizer(wx.VERTICAL)

        progresso = self.progress_manager.get_progress()

        # 1️⃣ Continuar leitura
        if progresso:
            btn_continuar = wx.Button(
                panel,
                label=f"Continuar leitura - {progresso['livro']} {progresso['capitulo']}"
            )
            sizer.Add(btn_continuar, 0, wx.EXPAND | wx.ALL, 10)
            sizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.ALL, 5)
            btn_continuar.Bind(wx.EVT_BUTTON, lambda e: self.continuarLeitura(frame))

        # 2️⃣ Selecionar versão
        btn_selecionar = wx.Button(panel, label="Selecionar Versão")
        sizer.Add(btn_selecionar, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.ALL, 5)

        # 3️⃣ Buscar por trecho
        btn_buscar = wx.Button(panel, label="Buscar por Trecho")
        sizer.Add(btn_buscar, 0, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(sizer)

        btn_selecionar.Bind(
    wx.EVT_BUTTON,
    lambda e, f=frame: (f.Destroy(), self.selecionaVersao())
)
        btn_buscar.Bind(
    wx.EVT_BUTTON,
    lambda e, f=frame: (f.Destroy(), self.abrirJanelaBusca(None))
)

        frame.Show()

    def abrirResultadoBusca(self, resultado):
        self.versao_selecionada = resultado["versao"]

        caminho = os.path.join(
            os.path.dirname(__file__),
            "dados",
            "versions",
            self.json_files[self.versao_selecionada]
        )

        with open(caminho, "r", encoding="utf-8-sig") as f:
            self.biblia = json.load(f)

        self.livro_selecionado = next(
            l for l in self.biblia if l["name"] == resultado["livro"]
        )
        self.capitulo_selecionado = resultado["capitulo"]
        self.versiculo_inicial = resultado["versiculo"]

        wx.CallAfter(self.exibirCapitulo)

    def exibirMenu(self, btn, menu):
        """Exibe o menu na posição do botão."""
        btn.PopupMenu(menu)

    def abrirJanelaBusca(self, frame_pai):
        frame = wx.Frame(frame_pai, title="Buscar Trecho Bíblico", size=(450, 400))
        panel = wx.Panel(frame)

        sizer = wx.BoxSizer(wx.VERTICAL)

        txt_busca = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        txt_busca.SetHint("Digite uma palavra ou trecho bíblico")

        sizer.Add(txt_busca, 0, wx.EXPAND | wx.ALL, 10)

        sizer.Add(wx.StaticText(panel, label="Buscar nas versões:"), 0, wx.LEFT | wx.TOP, 10)

        # CHECKBOXES
        self.checkboxes_busca = {}

        for versao in self.json_files.keys():
            cb = wx.CheckBox(panel, label=versao)
            cb.SetValue(True)  # TODAS MARCADAS POR PADRÃO
            self.checkboxes_busca[versao] = cb
            sizer.Add(cb, 0, wx.LEFT | wx.TOP, 10)

        btn_buscar = wx.Button(panel, label="Buscar")
        btn_voltar = wx.Button(panel, label="Voltar ao Menu Bíblia")
        sizer.Add(btn_voltar, 0, wx.EXPAND | wx.ALL, 10)

        sizer.Add(btn_buscar, 0, wx.EXPAND | wx.ALL, 15)

        panel.SetSizer(sizer)

        # Eventos
        txt_busca.Bind(wx.EVT_TEXT_ENTER, lambda e: self.executarBusca(txt_busca.GetValue(), frame))
        btn_buscar.Bind(wx.EVT_BUTTON, lambda e: self.executarBusca(txt_busca.GetValue(), frame))
        btn_voltar.Bind(
    wx.EVT_BUTTON,
    lambda e, f=frame: (f.Destroy(), self.menuBiblia())
)


        frame.Show()
        txt_busca.SetFocus()

    def executarBusca(self, termo, frame):
        termo = termo.strip()
        if not termo:
            ui.message("Digite algo para buscar.")
            return

        versoes_selecionadas = [
            versao for versao, cb in self.checkboxes_busca.items() if cb.GetValue()
        ]

        if not versoes_selecionadas:
            ui.message("Selecione ao menos uma versão para buscar.")
            return

        BuscaBiblica(
            frame,
            termo,
            self.json_files,
            versoes_selecionadas,
            self.abrirResultadoBusca,
            self.menuBiblia
        )

    def selecionarVersao(self, versao, frame):
        """Processa a versão selecionada e continua o fluxo."""
        self.versao_selecionada = versao
        frame.Destroy()  # Fecha a janela de seleção
        wx.CallAfter(self.listar_livros_e_exibir_menu)

    def listar_livros_e_exibir_menu(self):
        """Carrega o arquivo JSON da versão selecionada e exibe a lista de livros."""
        caminho_arquivo = os.path.join(os.path.dirname(__file__), "dados", "versions", self.json_files[self.versao_selecionada])

        try:
            # Altere a codificação para utf-8-sig para lidar com o BOM
            with open(caminho_arquivo, "r", encoding="utf-8-sig") as f:
                self.biblia = json.load(f)
                self.livros = [livro["name"] for livro in self.biblia]

            wx.CallAfter(self.selecionaLivro)
        except Exception as e:
            wx.MessageBox(f"Erro ao carregar a versão da Bíblia: {e}", "Erro")

    def selecionaLivro(self):
        """Exibe um diálogo para o usuário selecionar um livro."""
        with wx.SingleChoiceDialog(None, "Selecione um livro:", "Livros da Bíblia", self.livros) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                escolha = dlg.GetSelection()
                self.livro_selecionado = self.biblia[escolha]
                wx.CallAfter(self.selecionaCapitulo)
            else:
                ui.message("Nenhum livro foi selecionado.")

    def selecionaCapitulo(self):
        """Exibe um diálogo para o usuário selecionar um capítulo do livro escolhido."""
        total_capitulos = len(self.livro_selecionado["chapters"])

        # Criar o diálogo
        dialogo = wx.Dialog(None, title=f"Capítulos de {self.livro_selecionado['name']}", size=(300, 200))
        panel = wx.Panel(dialogo)

        # Criar um SpinCtrl para a seleção numérica
        spin_capitulo = wx.SpinCtrl(panel, value="1", min=1, max=total_capitulos, size=(80, 30))

        # Botão de OK para confirmar
        btn_ok = wx.Button(panel, label="OK")
        btn_ok.SetDefault()  # Define como botão padrão para Enter

        # Layout do painel
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label="Selecione um Capítulo:"), 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(spin_capitulo, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(btn_ok, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        panel.SetSizerAndFit(sizer)

        # Evento para capturar o clique ou Enter no botão OK
        def onConfirm(event):
            dialogo.EndModal(wx.ID_OK)

        btn_ok.Bind(wx.EVT_BUTTON, onConfirm)

        # Evento de tecla para capturar Enter diretamente do SpinCtrl
        def onKeyPress(event):
            if event.GetKeyCode() == wx.WXK_RETURN:  # Se for Enter
                dialogo.EndModal(wx.ID_OK)
            else:
                event.Skip()  # Permite que outras teclas sejam processadas normalmente

        spin_capitulo.Bind(wx.EVT_KEY_DOWN, onKeyPress)

        # Mostrar o diálogo
        if dialogo.ShowModal() == wx.ID_OK:
            # Obter o número do capítulo selecionado
            self.capitulo_selecionado = spin_capitulo.GetValue() - 1  # Ajusta para índice 0-based
            wx.CallAfter(self.selecionaVersiculo)
        else:
            ui.message("Nenhum capítulo foi selecionado.")

    def selecionaVersiculo(self):
        """Exibe um diálogo para o usuário selecionar o versículo inicial do capítulo escolhido."""
        capitulo = self.livro_selecionado["chapters"][self.capitulo_selecionado]
        total_versiculos = len(capitulo)

        # Criar o diálogo
        dialogo = wx.Dialog(None, title=f"Versículos do Capítulo {self.capitulo_selecionado + 1}", size=(300, 200))
        panel = wx.Panel(dialogo)

        # Criar um SpinCtrl para a seleção numérica
        spin_versiculo = wx.SpinCtrl(panel, value="1", min=1, max=total_versiculos, size=(80, 30))

        # Botão de OK para confirmar
        btn_ok = wx.Button(panel, label="OK")
        btn_ok.SetDefault()  # Define como botão padrão para Enter

        # Layout do painel
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label="Selecione o Versículo:"), 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(spin_versiculo, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(btn_ok, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        panel.SetSizerAndFit(sizer)

        # Evento para capturar o clique ou Enter no botão OK
        def onConfirm(event):
            dialogo.EndModal(wx.ID_OK)

        btn_ok.Bind(wx.EVT_BUTTON, onConfirm)

        # Evento de tecla para capturar Enter diretamente do SpinCtrl
        def onKeyPress(event):
            if event.GetKeyCode() == wx.WXK_RETURN:  # Se for Enter
                dialogo.EndModal(wx.ID_OK)
            else:
                event.Skip()  # Permite que outras teclas sejam processadas normalmente

        spin_versiculo.Bind(wx.EVT_KEY_DOWN, onKeyPress)

        # Mostrar o diálogo
        if dialogo.ShowModal() == wx.ID_OK:
            # Obter o número do versículo selecionado
            self.versiculo_inicial = spin_versiculo.GetValue() - 1  # Ajusta para índice 0-based
            wx.CallAfter(self.exibirCapitulo)
        else:
            ui.message("Nenhum versículo foi selecionado.")

    def exibirCapitulo(self):
        """Exibe o conteúdo do capítulo a partir do versículo selecionado."""
        capitulo = self.livro_selecionado["chapters"][self.capitulo_selecionado]
        conteudo = "\n".join(
            [f"{self.versiculo_inicial + i + 1}. {versiculo}" for i, versiculo in enumerate(capitulo[self.versiculo_inicial:])]
        )

        # Salva o progresso atual via gerenciador
        self.progress_manager.update_progress(
            self.versao_selecionada,
            self.livro_selecionado["name"],
            self.capitulo_selecionado + 1,
            self.versiculo_inicial + 1
        )

        frame = wx.Frame(None, title=f"{self.livro_selecionado['name']} - Capítulo {self.capitulo_selecionado + 1}, Versículo {self.versiculo_inicial + 1}", size=(600, 400))
        panel = wx.Panel(frame)

        text_ctrl = wx.TextCtrl(panel, value=conteudo, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        text_ctrl.SetFocus()

        # Botões principais
        btn_anterior = wx.Button(panel, label="Capítulo Anterior")
        btn_proximo = wx.Button(panel, label="Próximo Capítulo")

        # Botão "Mais Opções"
        btn_mais_opcoes = wx.Button(panel, label="Mais Opções")

        # Menu para "Mais Opções"
        menu = wx.Menu()
        item_escolher_livro = menu.Append(wx.ID_ANY, "Livros")
        item_escolher_versao = menu.Append(wx.ID_ANY, "Versões")
        item_menu_inicial = menu.Append(wx.ID_ANY, "Menu Inicial")
        item_criar_nota = menu.Append(wx.ID_ANY, "Criar Nota")

        # Associar o menu ao botão "Mais Opções"
        btn_mais_opcoes.Bind(wx.EVT_BUTTON, lambda event: self.exibirMenu(btn_mais_opcoes, menu))

        # Eventos dos itens do menu
        frame.Bind(wx.EVT_MENU, lambda event: self.voltarEscolhaLivro(frame), item_escolher_livro)
        frame.Bind(wx.EVT_MENU, lambda event: self.voltarEscolhaVersao(frame), item_escolher_versao)
        frame.Bind(wx.EVT_MENU, lambda event: self.menuInicial(frame), item_menu_inicial)
        frame.Bind(wx.EVT_MENU, self.criarNota, item_criar_nota)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(btn_anterior, flag=wx.RIGHT, border=10)
        btn_sizer.Add(btn_proximo, flag=wx.RIGHT, border=10)
        btn_sizer.Add(btn_mais_opcoes, flag=wx.RIGHT, border=10)
        sizer.Add(btn_sizer, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        panel.SetSizer(sizer)

        # Eventos dos botões principais
        btn_anterior.Bind(wx.EVT_BUTTON, lambda event: self.alternarCapitulo(-1, frame))
        btn_proximo.Bind(wx.EVT_BUTTON, lambda event: self.alternarCapitulo(1, frame))

        frame.Show()

    def exibirMenu(self, button, menu):
        """Exibe o menu ao lado do botão 'Mais Opções'."""
        pos = button.GetPosition()
        size = button.GetSize()
        menu_pos = (pos.x, pos.y + size.y)  # Exibe abaixo do botão
        button.GetParent().PopupMenu(menu, menu_pos)

    def menuInicial(self, frame_atual):
        menu = GlobalPlugin()
        menu.exibirMenu()
        frame_atual.Destroy()


    def criarNota(self, event):
        try:
            versao = self.versao_selecionada
            livro = self.livro_selecionado["name"]  # Nome do livro selecionado
            capitulo = self.capitulo_selecionado + 1  # Capítulo (ajustado para começar de 1)
            versiculos = self.livro_selecionado["chapters"][self.capitulo_selecionado]  # Todos os versículos do capítulo
            notas_manager = notas.NotasManager(versao, livro, capitulo, versiculos, self)  # Passa os argumentos para o NotasManager
        except AttributeError as e:
            wx.MessageBox(f"Erro ao criar nota: {e}", "Erro", wx.OK | wx.ICON_ERROR)

    def alternarCapitulo(self, direcao, frame_atual):
        novo_indice = self.capitulo_selecionado + direcao
        if 0 <= novo_indice < len(self.livro_selecionado["chapters"]):
            self.capitulo_selecionado = novo_indice
            self.versiculo_inicial = 0
            frame_atual.Destroy()
            wx.CallAfter(self.exibirCapitulo)
        else:
            ui.message("Não há mais capítulos nessa direção.")

    def voltarEscolhaLivro(self, frame_atual):
        """Fecha a janela atual e retorna para a lista de livros."""
        frame_atual.Destroy()
        wx.CallAfter(self.selecionaLivro)

    def voltarEscolhaVersao(self, frame_atual):
        """Fecha a janela atual e retorna ao menu inicial para selecionar a versão da Bíblia."""
        frame_atual.Destroy()
        wx.CallAfter(self.selecionaVersao)

