import wx
import os
import json
import ui


class BuscaBiblica:
    def __init__(
        self,
        parent,
        termo,
        json_files,
        versoes_selecionadas,
        abrir_callback,
        voltar_callback
    ):
        self.parent = parent
        self.termo = termo.lower()
        self.json_files = json_files
        self.versoes_selecionadas = versoes_selecionadas
        self.abrir_callback = abrir_callback
        self.voltar_callback = voltar_callback
        self.executar()

    def executar(self):
        resultados = []

        base = os.path.join(os.path.dirname(__file__), "dados", "versions")

        for versao in self.versoes_selecionadas:
            arquivo = self.json_files[versao]
            caminho = os.path.join(base, arquivo)
            try:
                with open(caminho, "r", encoding="utf-8-sig") as f:
                    biblia = json.load(f)

                for livro in biblia:
                    for c_idx, cap in enumerate(livro["chapters"]):
                        for v_idx, vers in enumerate(cap):
                            if self.termo in vers.lower():
                                resultados.append({
                                    "versao": versao,
                                    "livro": livro["name"],
                                    "capitulo": c_idx,
                                    "versiculo": v_idx,
                                    "texto": vers
                                })
            except Exception:
                pass

        if not resultados:
            wx.MessageBox("Nenhum resultado encontrado.", "Busca")
            return

        if self.parent:
            try:
                self.parent.Destroy()
            except Exception:
                pass

        self.exibirResultados(resultados)

    def exibirResultados(self, resultados):
        frame = wx.Frame(None, title="Resultados da Busca", size=(650, 400))
        panel = wx.Panel(frame)

        sizer = wx.BoxSizer(wx.VERTICAL)

        # 🔹 TEXTO NO TOPO COM QUANTIDADE
        qtd = len(resultados)
        texto_topo = wx.StaticText(
            panel,
            label=f"{qtd} resultado{'s' if qtd > 1 else ''} encontrado{'s' if qtd > 1 else ''} para a busca \"{self.termo}\""
        )
        sizer.Add(texto_topo, 0, wx.ALL, 10)

        # 🔹 LISTA DE RESULTADOS
        lista = wx.ListBox(panel)

        for i, r in enumerate(resultados, start=1):
            lista.Append(
                f"{i}. {r['versao']} - {r['livro']} {r['capitulo']+1}:{r['versiculo']+1} - {r['texto']}"
            )

        sizer.Add(lista, 1, wx.EXPAND | wx.ALL, 10)

        # 🔹 BOTÕES
        btn_abrir = wx.Button(panel, label="Abrir")
        btn_voltar = wx.Button(panel, label="Voltar ao Menu Bíblia")

        sizer.Add(btn_abrir, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizer.Add(btn_voltar, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        panel.SetSizer(sizer)

        def abrir(event):
            idx = lista.GetSelection()
            if idx == wx.NOT_FOUND:
                ui.message("Nenhum resultado selecionado.")
                return
            self.abrir_callback(resultados[idx])
            frame.Destroy()

        def voltar(event):
            frame.Destroy()
            if self.voltar_callback:
                wx.CallAfter(self.voltar_callback)

        btn_abrir.Bind(wx.EVT_BUTTON, abrir)
        btn_voltar.Bind(wx.EVT_BUTTON, voltar)

        frame.Show()

