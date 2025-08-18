import matplotlib.pyplot as plt
import numpy as np
from genestack_tools.microarray_assistent import MicroarrayExpressionAssistent

def plot_expression_distribution(assistent: MicroarrayExpressionAssistent) -> None:
    if assistent.adata is None:
        print("No AnnData available. Run initiate_adata() first.")
        return
    plt.hist(assistent.adata.X.flatten(), bins=50)
    plt.xlabel("Expression values")
    plt.ylabel("Frequency")
    plt.title("Distribution of expression values")
    plt.show()


def plot_volcano(assistent: MicroarrayExpressionAssistent) -> None:
    if not hasattr(assistent, "top_table") or assistent.top_table is None:
        print("No top_table available. Run run_limma() first.")
        return
    top_table = assistent.top_table
    color = np.where(np.abs(top_table["log2FoldChange"]) < 1, "grey", "blue")
    plt.figure(figsize=(8, 6))
    plt.scatter(
        top_table["log2FoldChange"],
        -np.log10(top_table["adj_pvalue"]),
        alpha=0.5,
        c=color
    )
    plt.axhline(y=-np.log10(0.05), color='r', linestyle='--')
    plt.xlabel("log2FoldChange")
    plt.ylabel("-log10(p-value)")
    plt.title("Volcano plot: I3C vs DMSO (all genes)")
    plt.grid(True)
    plt.show()
