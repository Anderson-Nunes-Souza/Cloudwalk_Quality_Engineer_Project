# Quake Log Parser

Este repositório contém um script Python que lê um arquivo de log de jogos, processa informações sobre jogadores e suas ações, e exibe os resultados de cada jogo.

## Estrutura do Projeto

- `assets/`: Pasta que deve conter o arquivo de log do jogo (`qgames.log`).
- `qgames.log`: Arquivo de log do jogo que será lido e processado pelo script.

## Requisitos

- Python 3.6 ou superior

## Instruções de Uso

1. Coloque o arquivo de log (`qgames.log`) na pasta `assets`.
2. Execute o script Python.

## Descrição do Script

O script realiza as seguintes ações:

1. **Leitura do Arquivo de Log**
   - A função `readfile` lê o conteúdo do arquivo de log localizado na pasta `assets` e retorna uma lista de linhas do arquivo.

2. **Identificação do Início de um Jogo**
   - A função `identifiesStartGame` verifica se uma linha do log indica o início de um novo jogo. Se sim, inicializa um novo dicionário para armazenar informações do jogo atual.

3. **Coleta de Informações dos Jogadores**
   - A função `collectsPlayersInfo` coleta informações sobre os jogadores a partir das linhas do log que indicam mudanças no estado do jogador.

4. **Coleta de Informações de Mortes**
   - A função `collectsKillInformation` processa as linhas do log que indicam mortes, atualizando o contador de mortes de cada jogador e o contador total de mortes do jogo.

5. **Verificação do Tipo de Morte**
   - A função `verifyKillByMeans` verifica e atualiza o tipo de arma ou meio utilizado para a morte.

6. **Identificação do Fim de um Jogo**
   - A função `identifiesEndGame` verifica se uma linha do log indica o fim de um jogo e adiciona as informações coletadas à lista de jogos.

7. **Exibição dos Resultados**
   - A função `showResults` exibe os resultados processados em formato JSON, mostrando as estatísticas de cada jogo.

## Execução do Script

Para executar o script, certifique-se de ter o arquivo de log na pasta `assets` e execute o seguinte comando no terminal:

```bash
python script.py
