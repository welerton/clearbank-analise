"""
Requisito Opcional 1 — Versão alternativa com pandas.
Executa a mesma análise do desafio-final.ipynb usando pd.read_csv() e groupby.
"""

import json
from datetime import datetime

import pandas as pd

ARQUIVO_CSV = 'transacoes.csv'
LIMITE_SUSPEITO = 10_000.00


def _fmt_brl(valor: float) -> str:
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def carregar_e_limpar(caminho: str) -> tuple[pd.DataFrame, int]:
    df_bruto = pd.read_csv(caminho, dtype=str)
    total_linhas = len(df_bruto)

    df = df_bruto.copy()

    # id numérico
    df['id'] = pd.to_numeric(df['id'], errors='coerce')
    df = df.dropna(subset=['id'])
    df['id'] = df['id'].astype(int)

    # cliente_id não vazio
    df = df[df['cliente_id'].notna() & (df['cliente_id'].str.strip() != '')]

    # data formato AAAA-MM-DD
    df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d', errors='coerce')
    df = df.dropna(subset=['data'])

    # tipo válido
    df['tipo'] = df['tipo'].str.strip().str.lower()
    df = df[df['tipo'].isin(['credito', 'debito'])]

    # valor numérico e positivo
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    df = df.dropna(subset=['valor'])
    df = df[df['valor'] > 0]

    invalidas = total_linhas - len(df)
    df['mes'] = df['data'].dt.strftime('%Y-%m')

    return df, invalidas


def calcular_metricas(df: pd.DataFrame) -> pd.DataFrame:
    credito = df[df['tipo'] == 'credito'].groupby('mes')['valor'].sum().rename('total_credito')
    debito  = df[df['tipo'] == 'debito'].groupby('mes')['valor'].sum().rename('total_debito')
    qtd     = df.groupby('mes')['valor'].count().rename('quantidade')
    media   = df.groupby('mes')['valor'].mean().rename('media')
    maior   = df.groupby('mes')['valor'].max().rename('maior_valor')
    menor   = df.groupby('mes')['valor'].min().rename('menor_valor')

    resumo = pd.concat([qtd, credito, debito, media, maior, menor], axis=1).fillna(0)
    resumo['saldo'] = resumo['total_credito'] - resumo['total_debito']
    return resumo.sort_index()


def exibir_relatorio_pandas(df: pd.DataFrame, resumo: pd.DataFrame, invalidas: int) -> None:
    mais_antiga = df['data'].min()
    mais_recente = df['data'].max()
    dias = (mais_recente - mais_antiga).days

    print('=' * 50)
    print('    ANÁLISE FINANCEIRA (pandas) — CLEARBANK')
    print('=' * 50)
    print(f'Período: {mais_antiga.strftime("%d/%m/%Y")} → {mais_recente.strftime("%d/%m/%Y")} ({dias} dias)')
    print(f'Transações válidas  : {len(df)}')
    print(f'Transações inválidas: {invalidas}')
    print()

    print('===== RELATÓRIO MENSAL (pandas) =====')
    for mes, m in resumo.iterrows():
        print()
        print(f'Mês: {mes}')
        print(f'  Transações : {int(m["quantidade"])}')
        print(f'  Total crédito: {_fmt_brl(m["total_credito"])}')
        print(f'  Total débito : {_fmt_brl(m["total_debito"])}')
        print(f'  Saldo        : {_fmt_brl(m["saldo"])}')
        print(f'  Média        : {_fmt_brl(m["media"])}')
        print(f'  Maior valor  : {_fmt_brl(m["maior_valor"])}')
        print(f'  Menor valor  : {_fmt_brl(m["menor_valor"])}')
    print()

    suspeitas = df[df['valor'] > LIMITE_SUSPEITO]
    print('===== TRANSAÇÕES SUSPEITAS (pandas) =====')
    if not suspeitas.empty:
        for _, s in suspeitas.iterrows():
            print(f'ID: {s["id"]} | Cliente: {s["cliente_id"]} | '
                  f'Data: {s["data"].strftime("%Y-%m-%d")} | Valor: {_fmt_brl(s["valor"])}')
    else:
        print('Nenhuma transação suspeita encontrada.')
    print()


def salvar_json_pandas(df: pd.DataFrame, resumo: pd.DataFrame, invalidas: int) -> None:
    suspeitas = df[df['valor'] > LIMITE_SUSPEITO]

    dados = {
        'gerado_em': datetime.today().strftime('%Y-%m-%d'),
        'fonte': 'pandas',
        'total_transacoes_validas': len(df),
        'total_transacoes_invalidas': invalidas,
        'resumo_mensal': {
            mes: {
                'quantidade': int(m['quantidade']),
                'total_credito': round(m['total_credito'], 2),
                'total_debito': round(m['total_debito'], 2),
                'saldo': round(m['saldo'], 2),
                'media': round(m['media'], 2),
                'maior_valor': round(m['maior_valor'], 2),
                'menor_valor': round(m['menor_valor'], 2),
            }
            for mes, m in resumo.iterrows()
        },
        'transacoes_suspeitas': [
            {
                'id': int(s['id']),
                'cliente_id': s['cliente_id'],
                'data': s['data'].strftime('%Y-%m-%d'),
                'tipo': s['tipo'],
                'valor': s['valor'],
            }
            for _, s in suspeitas.iterrows()
        ],
    }

    with open('relatorio_pandas.json', 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print('Relatório pandas salvo em: relatorio_pandas.json')


if __name__ == '__main__':
    df, invalidas = carregar_e_limpar(ARQUIVO_CSV)
    resumo = calcular_metricas(df)
    exibir_relatorio_pandas(df, resumo, invalidas)
    salvar_json_pandas(df, resumo, invalidas)
