# Accessible Bible Blind

**Autor:** Aldenor Neto  

---

## 📖 Descrição

O **Accessible Bible Blind** é um complemento para o NVDA desenvolvido para oferecer **leitura totalmente acessível da Bíblia**, com múltiplas versões bíblicas, navegação eficiente por teclado, sistema avançado de anotações e recursos pensados especificamente para usuários com deficiência visual.

A aplicação funciona inteiramente com **dados locais em formato JSON**, garantindo rapidez, estabilidade e funcionamento offline.

---

## 📚 Versões Bíblicas Disponíveis

Atualmente, o complemento conta com **10 versões da Bíblia**, organizadas por segmento:

### ✝️ Segmento Católico
- Bíblia **Pastoral**
- Bíblia **Ave Maria**
- Bíblia de **Jerusalém**
- Bíblia **CNBB**

### ✝️ Segmento Evangélico
- **Almeida Revista e Atualizada (ARA)**
- **Almeida Revista e Corrigida (ARC)**
- **Almeida Corrigida e Fiel (ACF)**
- **Nova Versão Internacional (NVI)**
- **Nova Tradução na Linguagem de Hoje (NTLH)**

### ✝️ Testemunhas de Jeová
- **Tradução do Novo Mundo**

---

## 🗂 Estrutura dos Dados

Os arquivos bíblicos estão organizados no diretório `dataset/globalPlugins`, utilizando a seguinte estrutura JSON:

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

Essa estrutura permite acesso direto aos **livros, capítulos e versículos**, facilitando buscas e navegação.

---

## ⚙️ Funcionalidades

### 📖 Navegação Bíblica

Fluxo padrão de leitura:

1. Seleção da versão bíblica
2. Escolha do livro
3. Seleção do capítulo
4. Leitura dos versículos

Durante a leitura, o usuário pode:

* Avançar ou retroceder capítulos
* Trocar de versão bíblica
* Trocar de livro
* Retornar ao menu principal
* Criar anotações a partir de versículos específicos

Após o primeiro acesso, é exibida a opção **“Continuar leitura”**, permitindo retomar exatamente o ponto onde o usuário parou.

---

### 🔍 Busca por Trecho Bíblico

O complemento inclui um sistema de **busca textual** que permite:

* Digitar um termo ou trecho bíblico
* Selecionar em quais versões a busca será realizada
  (por padrão, **todas as 10 versões vêm marcadas**)
* Exibição de uma lista acessível de resultados
* Abertura direta da leitura bíblica a partir do trecho selecionado

Esse recurso facilita estudos comparativos entre versões.

---

### 📝 Sistema de Anotações (CRUD)

O sistema de anotações permite **criar, visualizar, editar e excluir notas** pessoais.

Principais recursos:

* Seleção de **nenhum, um ou mais versículos** para compor a anotação
* Associação da nota à versão, livro e capítulo
* Armazenamento local no arquivo `notas.json`

Estrutura do arquivo de anotações:

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

1. Seleção dos versículos desejados
2. Definição do título da anotação
3. Inserção do conteúdo descritivo
4. Salvamento automático no JSON

---

## ⌨️ Teclas de Atalho

O complemento oferece **atalhos de teclado para navegação rápida**, todos configuráveis pelo usuário.

### Atalho padrão de ativação

* **NVDA + Shift + I** → Abre o menu principal do Bíblia Acessível

### Atalhos disponíveis durante a leitura

* **NVDA + V** → Trocar versão bíblica
* **NVDA + L** → Lista de livros
* **NVDA + ,** → Capítulo anterior
* **NVDA + .** → Próximo capítulo

### Personalização dos atalhos

Todos os atalhos podem ser **alterados livremente pelo usuário** em:

```
Menu NVDA → Preferências → Definir comandos → Bíblia Acessível
```

---

## 📁 Estrutura de Diretórios

O complemento segue **rigorosamente o template oficial de addons do NVDA**, garantindo compatibilidade, organização e facilidade de manutenção.

---

## ♿ Acessibilidade

O desenvolvimento do **Accessible Bible Blind** prioriza:

* Navegação 100% via teclado
* Compatibilidade total com o leitor de telas NVDA
* Interface simples, clara e objetiva
* Foco na autonomia do usuário com deficiência visual

---
