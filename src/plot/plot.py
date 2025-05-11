import sys
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

def main():
    parser = argparse.ArgumentParser(description="Plotador de gráficos de dados numéricos.")
    parser.add_argument("csv", help="Caminho para o arquivo CSV de entrada")
    parser.add_argument("--colunas", required=True, help="Colunas a serem usadas, separadas por vírgulas")
    parser.add_argument("--tipo", required=True, choices=["densidade", "linha", "correlacao", "boxplot"],
                        help="Tipo de gráfico: densidade | linha | correlacao | boxplot")
    parser.add_argument("--saida", help="Caminho do arquivo para salvar a imagem (ex: graficos/saida.png)")

    args = parser.parse_args()

    # Lê o CSV
    try:
        df = pd.read_csv(args.csv)
    except Exception as e:
        print(f"Erro ao ler o CSV: {e}")
        sys.exit(1)

    selected_columns = [col.strip() for col in args.colunas.split(",")]
    valid_columns = [col for col in selected_columns if col in df.columns]

    if not valid_columns:
        print("Nenhuma coluna válida foi fornecida.")
        sys.exit(1)

    tipo_grafico = args.tipo.lower()

    plt.figure(figsize=(10, 6))

    if tipo_grafico == "densidade":
        palette = sns.color_palette("husl", len(valid_columns))
        min_value = float("inf")
        max_value = float("-inf")

        for idx, col in enumerate(valid_columns):
            series = df[col].dropna()
            if series.empty:
                print(f"[Aviso] Coluna '{col}' está vazia. Ignorando.")
                continue
            sns.kdeplot(series, label=col, color=palette[idx], fill=True)
            min_value = min(min_value, series.min())
            max_value = max(max_value, series.max())

        plt.xlim(min_value, max_value)
        plt.title("Distribuições (KDE)")
        plt.xlabel("Valor")
        plt.ylabel("Densidade")

    elif tipo_grafico == "linha":
        for col in valid_columns:
            series = df[col].dropna().reset_index(drop=True)
            plt.plot(series, label=col)
        plt.title("Gráfico de Linha")
        plt.xlabel("Índice")
        plt.ylabel("Valor")

    elif tipo_grafico == "correlacao":
        corr = df[valid_columns].corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", square=True)
        plt.title("Mapa de Correlação")
        plt.tight_layout()
        if args.saida:
            salvar_grafico(args.saida)
        return  # Não exibe se salvar, já encerrado

    elif tipo_grafico == "boxplot":
        df_box = df[valid_columns].dropna()
        sns.boxplot(data=df_box)
        plt.title("Boxplot das Colunas Selecionadas")
        plt.xlabel("Coluna")
        plt.ylabel("Valor")

    # Elementos comuns
    if tipo_grafico not in ["correlacao", "boxplot"]:
        plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if args.saida:
        salvar_grafico(args.saida)
    else:
        plt.show()


def salvar_grafico(path_saida):
    try:
        os.makedirs(os.path.dirname(path_saida), exist_ok=True)
        plt.savefig(path_saida)
        print(f"Gráfico salvo em: {path_saida}")
    except Exception as e:
        print(f"Erro ao salvar a imagem: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
