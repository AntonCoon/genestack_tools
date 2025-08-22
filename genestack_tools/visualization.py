import numpy as np
import plotly.express

from genestack_tools.microarray_assistent import MicroarrayExpressionAssistent


def plot_expression_distribution(assistent: "MicroarrayExpressionAssistent") -> None:
    if assistent.adata is None:
        print("No AnnData available. Run initiate_adata() first.")
        return

    values = assistent.adata.X.flatten()
    fig = plotly.express.histogram(
        x=values,
        nbins=50,
        title="Distribution of Expression Values",
        labels={"x": "Expression values", "y": "Frequency"},
        opacity=0.7,
    )
    fig.update_layout(bargap=0.05, template="plotly_white")
    fig.show()


def plot_volcano(assistent: "MicroarrayExpressionAssistent") -> None:
    if not hasattr(assistent, "top_table") or assistent.top_table is None:
        print("No top_table available. Run run_limma() first.")
        return

    top_table = assistent.top_table.copy()
    top_table["color_group"] = [
        "|log2FC|>=1" if abs(x) >= 1 else "|log2FC|<1"
        for x in top_table["log2FoldChange"]
    ]

    fig = plotly.express.scatter(
        top_table,
        x="log2FoldChange",
        y=-np.log10(top_table["adj_pvalue"]),
        color="color_group",
        color_discrete_map={"|log2FC|<1": "grey", "|log2FC|>=1": "blue"},
        hover_name=top_table.index,
        labels={
            "x": "log2FoldChange",
            "y": "-log10(adj_pvalue)",
            "color_group": "Regulation",
        },
        title="Volcano plot: I3C vs DMSO (all genes)",
    )

    fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="red")
    fig.update_traces(marker=dict(size=6, opacity=0.7))
    fig.show()
