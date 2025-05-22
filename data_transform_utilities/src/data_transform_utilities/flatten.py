import pandas as pd


def _flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(_flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def flatten(df):
    """
    Função que extrai colunas aninhadas e cria novas colunas. Esse processo
    mantêm o padrão de nome da coluna mãe como prefixo.
    Args:
        df: Dataframe - Dataframe pandas com colunas aninhadas
    Returns:
        Dataframe com as colunas aninhadas extraídas.
    """
    flat_rows = []
    nested_columns = [col for col in df.columns if any(isinstance(row, dict) for row in df[col])]
    for _, row in df.iterrows():
        flat_row = {}
        for col in df.columns:  # Itera sobre todas as colunas
            if col in nested_columns and isinstance(row[col], dict):
                flat_data = _flatten_dict(row[col], col)
                flat_row.update(flat_data)
            else:
                flat_row[col] = row[col]  # Preserva colunas que não são dicts
        flat_rows.append(flat_row)
    return pd.DataFrame(flat_rows)