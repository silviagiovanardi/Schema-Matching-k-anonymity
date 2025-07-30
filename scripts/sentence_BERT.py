import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def sentence_bert():

    bert_df = pd.read_csv("data/schema_matching_bert.csv")

    grouped = bert_df.groupby("Dataset")["Similarità"].describe()
    print("\nStatistiche per dataset:")
    print(grouped)

    # Boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=bert_df, x="Dataset", y="Similarità", palette="Set2")
    plt.title("Distribuzione della Similarità (Sentence-BERT) per Dataset", fontsize=14)
    plt.ylabel("Similarità Coseno", fontsize=12)
    plt.xlabel("Dataset", fontsize=12)
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("grafico_matching_bert.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    sentence_bert()
