Projeto RPA - Sistema de Conselhos Aleatórios
Este projeto foi desenvolvido como avaliação final da disciplina de RPA (Robotic Process Automation). O sistema coleta, armazena e processa conselhos aleatórios de uma API pública.

```Sobre o Projeto
O sistema automatiza o processo de:
Coletar conselhos aleatórios da Advice Slip API
Armazenar os dados em um banco SQLite
Processar e analisar as informações coletadas
```

```Funcionalidades
- Coleta de Dados: Requisição automática à API para obter conselhos;
- Armazenamento: Banco de dados local com controle de duplicatas;
- Processamento: Análise estatística dos conselhos armazenados;
- Relatório: Exibição de todos os conselhos e métricas;
```

```Tecnologias Utilizadas
- Python 3
- SQLite para banco de dados
- Requests para consumo de API
- Biblioteca datetime para controle de datas
```

```Como Executar
Certifique-se de ter Python instalado e a biblioteca "requests"

- Execute o arquivo rpa_final.py
- O sistema criará automaticamente o banco de dados e começará a coletar dados
```

```Estrutura do Banco
A tabela conselhos contém:

ID único do conselho
Texto do conselho
Data e hora da coleta
```

```API Utilizada
Advice Slip API - Fornece conselhos aleatórios em formato JSON
https://api.adviceslip.com/
