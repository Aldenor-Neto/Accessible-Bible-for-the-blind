import wx
import ui
import globalPluginHandler
import webbrowser


from . import notas


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def script_openBibleMenu(self, gesture):
        self.showMenu()

    script_openBibleMenu.__doc__ = _("Menu principal do Bíblia Acessível")
    script_openBibleMenu.category = _("Bíblia Acessível")

    def showMenu(self):
        wx.CallLater(0, self.exibirMenu)

    def exibirMenu(self):
        self.dialog = wx.Dialog(
            None,
            title="Bem vindo ao Bíblia Acessível",
            size=(300, 200)
        )

        panel = wx.Panel(self.dialog)
        sizer = wx.BoxSizer(wx.VERTICAL)

        btn_biblias = wx.Button(panel, label="Bíblias")
        btn_biblias.Bind(wx.EVT_BUTTON, self.abrirBiblia)

        btn_anotacoes = wx.Button(panel, label="Anotações")
        btn_anotacoes.Bind(wx.EVT_BUTTON, self.abrirAnotacoes)

        btn_fale_conosco = wx.Button(panel, label="Fale Conosco")
        btn_fale_conosco.Bind(wx.EVT_BUTTON, self.abrirFaleConosco)

        sizer.Add(btn_biblias, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(btn_anotacoes, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(btn_fale_conosco, 0, wx.EXPAND | wx.ALL, 10)


        panel.SetSizerAndFit(sizer)
        self.dialog.ShowModal()

    def abrirFaleConosco(self, event):
        mensagem = (
            "Você será direcionado para um formulário onde poderá entrar em contato conosco.\n\n"
            "No formulário você poderá enviar dúvidas, sugestões ou relatar bugs."
        )

        resposta = wx.MessageBox(
            mensagem,
            "Fale Conosco",
            wx.OK | wx.CANCEL | wx.ICON_INFORMATION
        )

        if resposta == wx.OK:
            webbrowser.open(
                "https://docs.google.com/forms/d/e/1FAIpQLScxAAYPoIF6hq2ZK-FIBUTqfsQixSkwCdtxF475wbfP-tFfSg/viewform?usp=sharing&ouid=104944239672742422494"
            )
            self.dialog.Destroy()

    def script_listaLivros(self, gesture):
        try:
            from .biblia import BIBLIA_ATIVA
            if BIBLIA_ATIVA and BIBLIA_ATIVA.btn_anterior:
                frame = BIBLIA_ATIVA.btn_anterior.GetParent().GetParent()
                wx.CallAfter(BIBLIA_ATIVA.voltarEscolhaLivro, frame)
            else:
                ui.message("Leitura não está aberta.")
        except Exception:
            ui.message("Erro ao abrir a lista de livros.")

    script_listaLivros.__doc__ = _("Selecionar lista de livros da Bíblia")
    script_listaLivros.category = _("Bíblia Acessível")

    def script_mudarVersao(self, gesture):
        try:
            from .biblia import BIBLIA_ATIVA
            if BIBLIA_ATIVA and BIBLIA_ATIVA.btn_anterior:
                frame = BIBLIA_ATIVA.btn_anterior.GetParent().GetParent()
                wx.CallAfter(BIBLIA_ATIVA.voltarEscolhaVersao, frame)
            else:
                ui.message("Leitura não está aberta.")
        except Exception:
            ui.message("Erro ao abrir a seleção de versões.")

    script_mudarVersao.__doc__ = _("Selecionar versão da Bíblia")
    script_mudarVersao.category = _("Bíblia Acessível")

    def script_capituloAnterior(self, gesture):
        try:
            from .biblia import BIBLIA_ATIVA
            if BIBLIA_ATIVA and hasattr(BIBLIA_ATIVA, "capitulo_selecionado"):
                wx.CallAfter(
                    BIBLIA_ATIVA.alternarCapitulo,
                    -1,
                    BIBLIA_ATIVA.btn_anterior.GetParent().GetParent()
                )
            else:
                ui.message("Leitura não está aberta.")
        except Exception:
            ui.message("Leitura não está aberta.")

    script_capituloAnterior.__doc__ = _("Ir para o capítulo anterior")
    script_capituloAnterior.category = _("Bíblia Acessível")

    def script_proximoCapitulo(self, gesture):
        try:
            from .biblia import BIBLIA_ATIVA
            if BIBLIA_ATIVA and hasattr(BIBLIA_ATIVA, "capitulo_selecionado"):
                wx.CallAfter(
                    BIBLIA_ATIVA.alternarCapitulo,
                    1,
                    BIBLIA_ATIVA.btn_proximo.GetParent().GetParent()
                )
            else:
                ui.message("Leitura não está aberta.")
        except Exception:
            ui.message("Leitura não está aberta.")

    script_proximoCapitulo.__doc__ = _("Ir para o próximo capítulo")
    script_proximoCapitulo.category = _("Bíblia Acessível")

    def abrirBiblia(self, event):
        from .biblia import Biblias
        try:
            Biblias().script_openBible()
        finally:
            self.dialog.Destroy()

    def abrirAnotacoes(self, event):
        try:
            notas.NotasStorage(self).exibirNotas()
        finally:
            self.dialog.Destroy()

    __gestures = {
        "kb:NVDA+shift+i": "openBibleMenu",
        "kb:NVDA+l": "listaLivros",
        "kb:NVDA+v": "mudarVersao",
        "kb:NVDA+,": "capituloAnterior",
        "kb:NVDA+.": "proximoCapitulo",
    }
