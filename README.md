# Genestack Tools

## TLDR
This project is a test exercise for the Bioinformatics Data Scientist position at Genestack.  
It demonstrates how to fetch, process, and analyze microarray datasets efficiently using the provided assistant classes and functions.

Genestack Tools is a Python package for efficient analysis of biological data, with a focus on microarray experiments.  
It provides robust functionality for fetching GEO datasets, normalizing data, running differential expression analyses (e.g., limma), visualizing results, and querying external databases such as GenBank.

## Features

- Automatic download and parsing of GEO datasets
- Organize data using `AnnData` objects for efficient handling
- Normalization and filtering of expression data
- Differential expression analysis with limma, supporting batch correction
- Built-in visualization for expression distributions and volcano plots
- Query results in external databases directly from the assistant
- Extensible design with abstract `Assistent` class and specialized `MicroarrayExpressionAssistent`

## Installation

The project uses Poetry for dependency management.

```bash
poetry install
```

## Testing

All tests are located in the `tests/` directory.  
You can run them using Poetry:

```bash
poetry run pytest
```

## Usage

All functionalities are demonstrated in the Jupyter notebook:  
`notebooks/midgut_microarray_analysis_i3c_vs_dmso.ipynb`  

The notebook shows how to fetch GEO datasets, organize and normalize the data, run differential expression analysis with limma, visualize results, and query external databases using the assistant classes.

**Note:** To use the `answer_question` function of `MicroarrayExpressionAssistent`, you need a `.env` file in the project directory containing a valid token from OpenRouter.
