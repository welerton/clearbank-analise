# ClearBank — Análise Financeira com Python

Projeto de análise de dados desenvolvido como desafio final do módulo de Python aplicado à análise de dados.

## Descrição

O notebook processa o histórico de transações da fintech ClearBank (`transacoes.csv`), realizando:

- Leitura e validação de dados com o módulo nativo `csv`
- Limpeza automática de registros inválidos (campos vazios, datas mal formatadas, valores inválidos)
- Cálculo de métricas financeiras mensais (crédito, débito, saldo, média, maior e menor valor)
- Identificação de transações suspeitas (acima de R$ 10.000,00)
- Exportação do relatório em `relatorio.json`
- Relatório formatado exibido no terminal

## Arquivos

| Arquivo | Descrição |
|---|---|
| `desafio-final.ipynb` | Notebook principal com todo o pipeline de análise |
| `transacoes.csv` | Arquivo de entrada com transações (incluindo registros inválidos para teste) |
| `relatorio.json` | Gerado automaticamente ao executar o notebook |
| `analise_pandas.py` | Versão alternativa usando pandas (opcional) |
| `grafico.png` | Gráfico de barras gerado pelo matplotlib (opcional) |

## Como executar

### Google Colab
1. Acesse [colab.research.google.com](https://colab.research.google.com)
2. Faça upload de `desafio-final.ipynb` e `transacoes.csv`
3. Vá em **Runtime → Run all**

### Jupyter Notebook local
```bash
pip install pandas matplotlib notebook
jupyter notebook desafio-final.ipynb
```
Execute todas as células em ordem (Kernel → Restart & Run All).

### Script pandas (opcional)
```bash
pip install pandas
python analise_pandas.py
```

## Saídas geradas

- **Terminal**: relatório com resumo por mês, transações suspeitas e estatísticas de limpeza
- **`relatorio.json`**: relatório completo em formato JSON com métricas mensais
- **`grafico.png`**: gráfico de barras com créditos, débitos e saldo por mês (requer matplotlib)

## Requisitos

- Python 3.10 ou superior
- `pandas` e `matplotlib` apenas para os requisitos opcionais (já disponíveis no Google Colab)
