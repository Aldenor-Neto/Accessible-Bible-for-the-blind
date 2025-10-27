# Accessible Bible Blind

**Versão:** 2.1
**Autor:** Aldenor Neto
**Compatibilidade:** NVDA 2022.4 a 2025.1

---

## 📖 Descrição

O **Accessible Bible Blind** é um complemento para NVDA que permite a leitura acessível da Bíblia em diferentes versões, oferecendo suporte completo à navegação por teclado e recursos de anotações pessoais.

A aplicação utiliza um banco de dados local em **JSON**, garantindo acesso rápido e estruturado aos livros, capítulos e versículos de seis versões bíblicas:

* **Versões católicas**: Ave Maria, Jerusalém
* **Versões protestantes**: Nova Versão Internacional (NVI), Almeida Corrigida e Fiel, Almeida Revista e Atualizada, Tradução do Novo Mundo

Os arquivos JSON estão organizados dentro do diretório `dataset` na pasta `globalPlugins`. Cada arquivo segue a estrutura:

```json
[
    {
        "abbrev": "",
        "name": "",
        "chapters": [
            [
                "Texto do versículo"
            ]
        ]
    }
]
```

---

## ⚙️ Funcionalidades

### Navegação bíblica

1. Seleção da versão bíblica.
2. Escolha do livro.
3. Seleção do capítulo.
4. Escolha do versículo.

O trecho selecionado é exibido em uma caixa de texto, permitindo:

* Navegação entre capítulos (anterior/próximo)
* Troca de versão ou livro
* Retorno ao menu principal
* Criação de anotações a partir do trecho bíblico

Após o primeiro acesso, é exibido um botão **“Continuar leitura”**, permitindo que o usuário retome o ponto em que parou.

---

### Sistema de Anotações (CRUD)

O complemento inclui um sistema para **criar, visualizar, editar e excluir anotações**, armazenadas no arquivo `notas.json` em `dataset/globalPlugins`. Estrutura do JSON:

```json
[
    {
        "titulo": "",
        "versao": "",
        "livro": "",
        "capitulo": 0,
        "versiculos": [
            {
                "numero": 0,
                "texto": ""
            }
        ],
        "descricao": ""
    }
]
```

Fluxo para criação de uma nota:

1. Definição do título da nota
2. Inserção do conteúdo em uma caixa de edição
3. Salvamento automático no JSON

---

### Estrutura de Diretórios

O complemento segue a **mesma organização do template oficial do NVDA**

---

### Acessibilidade

Todas as funcionalidades foram desenvolvidas priorizando:

* Navegação completa via teclado
* Compatibilidade total com o NVDA
* Experiência de leitura fluida para usuários com deficiência visual
