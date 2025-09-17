# Bíblia Acessível

Este é um addon para o NVDA (NonVisual Desktop Access) que permite aos usuários navegar e interagir com diferentes versões da Bíblia, incluindo uma funcionalidade para selecionar capítulos e versículos. O addon oferece uma interface acessível com o uso de caixas de diálogo para escolher livros, capítulos e versículos, e exibe o conteúdo da Bíblia de maneira estruturada e fácil de ler.

## Funcionalidades

- **Escolha de versão**: O usuário pode escolher entre diferentes versões da Bíblia, como "Católica", "Católica - Ave Maria", "Evangélica - Almeida Corrigida e Fiel", "Evangélica - Almeida Revisada Imprensa Bíblica" e "Evangélica - NVI".
- **Seleção de livro**: Após escolher a versão, o usuário pode selecionar um livro da Bíblia.
- **Seleção de capítulo**: O usuário pode escolher um capítulo do livro selecionado.
- **Seleção de versículo**: Ao escolher um versículo, o conteúdo exibido na caixa de texto começa a partir do versículo selecionado até o fim do capítulo.
- **Exibição de conteúdo**: O conteúdo do capítulo ou do trecho selecionado é exibido em uma caixa de texto somente leitura.
- **Navegação**: O usuário pode navegar entre os capítulos, voltar ao livro ou selecionar uma nova versão da Bíblia.

## Requisitos

- NVDA (NonVisual Desktop Access)
- Versão miníma do NVDA 2022.4

## Estrutura do Projeto

O projeto contém as seguintes principais funcionalidades e arquivos:

- **`globalPluginHandler`**: O principal handler do addon que controla a navegação entre as versões da Bíblia, livros, capítulos e versículos.
- **Arquivos JSON**: O conteúdo da Bíblia em diferentes versões. Exemplos de arquivos JSON incluem:
  - `catolica.json`
  - `evangelica - Almeida Corrigida e Fiel.json`
  - `evangelica - Almeida Revisada Imprensa Bíblica.json`
  - `evangelica - NVI.json`
  - `catolica - Ave Maria.json`

- **Caixas de diálogo wxWidgets**: Usadas para interações com o usuário para escolher a versão da Bíblia, livro, capítulo e versículo.

## Como Usar

1. **Ativar o addon**:
   - No NVDA, pressione `NVDA + Shift + I` para abrir a Bíblia Interativa.
   
2. **Escolher a versão**:
   - Será exibida uma caixa de diálogo para selecionar a versão da Bíblia. As opções incluem as versões mencionadas anteriormente.

3. **Escolher o livro**:
   - Após selecionar a versão, o addon apresentará uma lista de livros para o usuário escolher.

4. **Escolher o capítulo**:
   - O usuário pode então escolher um capítulo do livro selecionado.

5. **Escolher o versículo**:
   - Após escolher um capítulo, o usuário pode selecionar um versículo específico. A exibição do conteúdo começará no versículo escolhido até o final do capítulo.

6. **Navegar**:
   - É possível navegar entre os capítulos ou voltar para selecionar um novo livro ou versão.

## Exemplo de Uso

- Após escolher a versão da Bíblia "Católica" e o livro "João", capítulo 3, o usuário pode escolher o versículo 16. O conteúdo exibido será:

```
16. Com efeito, de tal modo Deus amou o mundo, que lhe deu seu Filho único, para que todo o que nele crer não pereça, mas tenha a vida eterna.
17. Pois Deus não enviou o Filho ao mundo para condená-lo, mas para que o mundo seja salvo por ele.
18. Quem nele crê não é condenado, mas quem não crê já está condenado, porque não crê no nome do Filho único de Deus.
...
```

