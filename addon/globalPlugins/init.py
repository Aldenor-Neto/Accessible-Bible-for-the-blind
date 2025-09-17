import wx
import ui
import globalPluginHandler
from . import biblia
from . import notas

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def script_init(self, gesture):
        self.showMenu()

    def showMenu(self):
        # Exibe o menu inicial
        wx.CallLater(0, self.exibirMenu)

    def exibirMenu(self):
        """Criação da interface gráfica para o menu de opções."""
        self.dialog = wx.Dialog(None, title="Bem vindo ao Bíblia Acessível", size=(300, 200))
        panel = wx.Panel(self.dialog)

        # Layout e Botões
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Botão para abrir a Bíblia
        btn_biblias = wx.Button(panel, label="Bíblias")
        btn_biblias.Bind(wx.EVT_BUTTON, self.abrirBiblia)

        # Botão para abrir as anotações
        btn_anotacoes = wx.Button(panel, label="Anotações")
        btn_anotacoes.Bind(wx.EVT_BUTTON, self.abrirAnotacoes)

        # Adicionando os botões ao sizer
        sizer.Add(btn_biblias, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(btn_anotacoes, 0, wx.EXPAND | wx.ALL, 10)

        panel.SetSizerAndFit(sizer)

        # Mostrando o diálogo
        self.dialog.ShowModal()

    def abrirBiblia(self, event):
        """Abre a funcionalidade da Bíblia."""
        try:
            biblia_init = biblia.Biblias()
            biblia_init.script_openBible()
        except Exception as e:
            wx.MessageBox(f"Erro ao abrir a Bíblia: {str(e)}", "Erro", wx.OK | wx.ICON_ERROR)
        finally:
            self.dialog.Destroy()  # Fecha o menu após a seleção

    def abrirAnotacoes(self, event):
        """Abre a funcionalidade de anotações."""
        try:
            notas_init = notas.NotasStorage()
            notas_init.exibirNotas()  # Método esperado para exibir ou gerenciar anotações
        except Exception as e:
            wx.MessageBox(f"Erro ao abrir as anotações: {str(e)}", "Erro", wx.OK | wx.ICON_ERROR)
        finally:
            self.dialog.Destroy()  # Fecha o menu após a seleção

    # Mapeia o gesto para chamar o método 'script_init'
    __gestures = {
        "kb:NVDA+shift+i": "init"
    }
