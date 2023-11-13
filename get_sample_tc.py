import os
import sys
import pandas as pd
from llama_index.query_engine import PandasQueryEngine
from huggingface_hub import hf_hub_download
import logging


def get_sample_tc(excel_file, sheet, keyword=None):
    # 已知keyword没有使用，是因为下面的暂时屏蔽1
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    os.environ["OPENAI_API_KEY"] = os.environ["OPENAIAPIKEY"]
    hfapi = os.environ["HFAPIKEY"]
    hfdsrepo = "tinypace/sampletextcase"

    defaultexcelfile = "默认.xlsx"

    # -------------------找到所有与keyword相关的测试用例--------------------
    try:
        localfilepath = hf_hub_download(repo_id=hfdsrepo, filename=excel_file, repo_type="dataset", token=hfapi)
    except Exception as e:
        print("读取样例TC文件失败，使用默认测试用例文件：", str(e))
        localfilepath = hf_hub_download(repo_id=hfdsrepo, filename=defaultexcelfile, repo_type="dataset", token=hfapi)

    df = pd.read_excel(localfilepath, sheet_name=sheet)
    # print(df.to_string())
    query_engine = PandasQueryEngine(df=df, verbose=True)
    tcresult = query_engine.query(
        # ---- 暂时屏蔽1： 由于目前pandasqueryengine并不能理解keyword的语义，只是单纯将输入作为一个限制条件，所以导致总是筛选不出正确的案例，故暂时去掉 ----
        # "选择出关于" + keyword + "的所有测试用例。以json的格式用unicode输出以下字段内容: 用例编号, 测试场景, 用例名称, 前置条件, 测试数据, 测试步骤, 预期结果, 重要程度")
        # ---- end of 暂时屏蔽1 ------
        "选择出关于的所有测试用例。以json的格式用中文输出以下字段内容: 用例编号, 测试场景, 用例名称, 前置条件, 测试数据, 测试步骤, 预期结果, 重要程度")
    # ------------------------------------------------------------------
    logging.info("Selected TCs by Keyword: \n" + tcresult.response)

    return tcresult.response

