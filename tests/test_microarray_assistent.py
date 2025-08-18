from genestack_tools.microarray_assistent import MicroarrayExpressionAssistent


# tests here are not thorally written, they are mostly to check that __init__ works fine
def test_init_only():
    base_url = "https://example.com"
    headers = {"Authorization": "Bearer test"}
    ass = MicroarrayExpressionAssistent(base_url=base_url, headers=headers)
    assert isinstance(ass, MicroarrayExpressionAssistent)
    assert ass.base_url == base_url
    assert ass.headers == headers
    assert ass.adata is None
    assert ass.fit is None
    assert ass.top_table is None
    assert ass.design is None


def test_methods_exist():
    base_url = "https://example.com"
    headers = {"Authorization": "Bearer test"}
    ass = MicroarrayExpressionAssistent(base_url=base_url, headers=headers)
    assert hasattr(ass, "get_data")
    assert hasattr(ass, "initiate_adata")
    assert hasattr(ass, "normalize_data")
    assert hasattr(ass, "run_limma")
    assert hasattr(ass, "answer_question")


def test_answer_question_callable():
    base_url = "https://example.com"
    headers = {"Authorization": "Bearer test"}
    ass = MicroarrayExpressionAssistent(base_url=base_url, headers=headers)
    assert callable(ass.answer_question)


def test_run_limma_callable():
    base_url = "https://example.com"
    headers = {"Authorization": "Bearer test"}
    ass = MicroarrayExpressionAssistent(base_url=base_url, headers=headers)
    assert callable(ass.run_limma)
