import pandas as pd
import matplotlib
matplotlib.use("Agg")  # ✅ Utilise le backend non-GUI adapté aux serveurs
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

# 🔧 Fonction pour convertir une figure matplotlib en image base64
def fig_to_base64(fig):
    buf = BytesIO()
    fig.tight_layout(pad=2)
    fig.savefig(buf, format="png", dpi=150, bbox_inches='tight')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return encoded

# 📊 Fonction principale qui génère les deux graphiques
def generate_graphs(csv_path='chocolate_sales.csv'):
    df = pd.read_csv(csv_path)
    df.columns = [col.strip() for col in df.columns]

    sns.set_style("whitegrid")

    # ✅ Graphique 1 : Top 20 produits (log scale)
    product_counts = df['product'].value_counts().head(20)
    fig1 = plt.figure(figsize=(10, 8))
    sns.barplot(x=product_counts.index, y=product_counts.values, color="steelblue")
    plt.title("Nombre de ventes par type de chocolat ", fontsize=16)
    plt.xlabel("Produit", fontsize=14)
    plt.ylabel("Nombre de ventes", fontsize=14)
    plt.yscale('log')
    plt.xticks(rotation=90)
    graph1_base64 = fig_to_base64(fig1)

    # ✅ Graphique 2 : Top 15 vendeurs par montant total (log scale)
    df_grouped = df.groupby('sales_person')['amount_in_dh'].sum().reset_index()
    df_grouped = df_grouped.sort_values(by='amount_in_dh', ascending=False).head(15)
    fig2 = plt.figure(figsize=(10, 5))
    sns.barplot(x='sales_person', y='amount_in_dh', data=df_grouped, color="steelblue")
    plt.title("Top 15 acheteurs ", fontsize=16)
    plt.xlabel("acheteurs", fontsize=14)
    plt.ylabel("Montant total (DH, log)", fontsize=14)
    plt.yscale('log')
    plt.xticks(rotation=90)
    graph2_base64 = fig_to_base64(fig2)

    return graph1_base64, graph2_base64
