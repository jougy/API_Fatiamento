# Calculadora de Impressão 3D
Este projeto é uma aplicação web em Python, usando o Flask, para calcular o custo e o tempo estimado de impressão 3D a partir de um arquivo STL.

## Funcionalidades
- Upload de Arquivo STL: O usuário pode fazer upload de um arquivo .stl contendo o modelo 3D.
- Cálculo de Volume: O volume da peça é calculado com base no modelo STL.
- Estimativa de Tempo e Preço: O tempo e o custo de impressão são estimados considerando configurações definidas, como densidade e diâmetro do filamento.
## Pré-requisitos
- Python 3.6 ou superior
- Bibliotecas: Flask, NumPy, e numpy-stl
## Instalação das Bibliotecas
Para instalar as bibliotecas necessárias, execute:
```
pip install Flask numpy numpy-stl
```
## Estrutura de Arquivos
- app.py: Arquivo principal da aplicação, que contém a lógica do Flask e as funções de cálculo.
- templates/index.html: Página principal da aplicação.
- static/style.css: Arquivo de estilo para o layout da página.
### Configuração
Certifique-se de que a pasta uploads exista na raiz do projeto ou crie-a antes de iniciar o servidor.

## Variáveis de Configuração em app.py
- UPLOAD_FOLDER: Pasta onde os arquivos STL enviados serão armazenados temporariamente.
- PRECO_FILAMENTO, PESO_FILAMENTO, DENSIDADE_FILAMENTO, DIAMETRO_FILAMENTO, VELOCIDADES_IMPRESSAO, LUCRO: Variáveis que configuram os parâmetros de custo e tempo de impressão.
## Execução
Para iniciar o servidor Flask, execute:
```
python app.py
```
A aplicação estará disponível em http://localhost:5000.

## Uso
Acesse a aplicação via web e faça upload do arquivo STL.
Após o upload, os resultados de volume, tempo estimado e preço serão exibidos na tela.