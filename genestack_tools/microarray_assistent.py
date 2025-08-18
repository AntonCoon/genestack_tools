from typing import Dict, Optional, Type

import GEOparse
import inmoose
import pandas as pd
import patsy
import scanpy as sc
from anndata import AnnData

from genestack_tools.assistent import Assistent
from genestack_tools.custom_types import AskModelRequest, AskModelResponse
from genestack_tools.llm_api import T, ask_model


class MicroarrayExpressionAssistent(Assistent):
    def __init__(
        self,
        base_url: str,
        headers: Dict[str, str],
        response_format: Type[T] = AskModelResponse,
    ):
        self.gse = None
        self.gpl = None
        self.adata: Optional[AnnData] = None
        self.base_url = base_url
        self.headers = headers
        self.response_format = response_format
        self.fit = None
        self.design = None
        self.top_table = None

    def get_data(self, gse_id: str, gpl_id: Optional[str] = None) -> None:
        self.gse = GEOparse.get_GEO(gse_id, how="full", silent=True)
        if gpl_id is None:
            gpl_id = list(self.gse.gpls.keys())[0]
        self.gpl = self.gse.gpls[gpl_id]

    def initiate_adata(
        self, group_pattern: str = "I3C|DMSO", exclude: str = "M_MidR3_Ind"
    ) -> None:
        pheno = self.gse.phenotype_data
        expr = self.gse.pivot_samples("VALUE")

        mask = pheno["source_name_ch1"].str.contains(
            group_pattern, case=False, na=False
        )
        mask &= pheno["source_name_ch2"] != exclude
        pheno_sub = pheno.loc[mask]
        expr_sub = expr[pheno_sub.index]

        groups = pheno_sub["source_name_ch1"].apply(
            lambda x: "I3C" if "I3C" in x else "DMSO"
        )

        def get_batch(x):
            for tag in ["MidR1", "MidR2", "MidR3"]:
                if tag in str(x):
                    return tag
            return "other"

        batches = pheno_sub["source_name_ch1"].apply(get_batch)
        clinical = pd.DataFrame(
            {"batch": batches, "group": groups}, index=expr_sub.columns
        )

        platform_table = self.gpl.table
        gene_ids = platform_table.set_index("ID").loc[expr_sub.index, "INTERNAL_GENE"]

        self.adata = AnnData(
            X=expr_sub.T,
            obs=clinical,
            var=pd.DataFrame({"gene_name": gene_ids.values}, index=expr_sub.index),
        )
        self.adata.var["probe_id"] = expr_sub.index.values

    def data_overview(self) -> None:
        if self.adata is None:
            print("No AnnData available. Run initiate_adata() first.")
            return
        print(self.adata)
        print(self.adata.obs)

    def normalize_data(self, lognorm: bool = True, filter_zeros: bool = True) -> None:
        if self.adata is None:
            print("No AnnData available. Run initiate_adata() first.")
            return
        self.adata.raw = self.adata
        if filter_zeros:
            sc.pp.filter_genes(self.adata, min_counts=0.001)
        if lognorm:
            sc.pp.log1p(self.adata)

    def run_limma(
        self,
        formula: str = "~ 0 + group",
        coef_name: str = "group[DMSO]",
        verbose: bool = True,
    ):
        if self.adata is None:
            print("No AnnData available. Run initiate_adata() first.")
            return None
        self.adata.obs["batch"] = self.adata.obs["batch"].astype(str)
        self.adata.obs["group"] = self.adata.obs["group"].astype(str)
        design = patsy.dmatrix(formula, self.adata.obs)
        fit = inmoose.limma.lmFit(self.adata.X.T, design)
        fit = inmoose.limma.eBayes(fit)
        top_table = inmoose.limma.topTable(fit, number=300, coef=coef_name)
        self.design = design
        self.fit = fit
        self.top_table = top_table
        if verbose:
            print(design)
            print(top_table)
        return fit

    def answer_question(self, question: str, *args, **kwargs) -> str:
        request = AskModelRequest(question=question, args=args, kwargs=kwargs)
        return ask_model(
            request=request,
            base_url=self.base_url,
            headers=self.headers,
            response_format=self.response_format,
        )
