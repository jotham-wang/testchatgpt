import os
import sys
import datasets
import openai
import pandas as pd
from llama_index.query_engine import PandasQueryEngine
from huggingface_hub import hf_hub_download
import time
import logging
import re
import json
from prompt_templates import CHATGPT_PROMPT_TMPL


def kwfromhf(inputkws):
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    os.environ["OPENAI_API_KEY"] = os.environ["OPENAIAPIKEY"]
    hfapi = os.environ["HFAPIKEY"]
    hfdsrepo = "tinypace/sampletextcase"

    kwresult = datasets.load_dataset(hfdsrepo, data_files=inputkws, use_auth_token=hfapi)
    kwlist = kwresult['train']['text']

    kwstring = "\n".join(kwlist)

    return kwstring


def summarize_keywords(inputreq, inputkws):
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    os.environ["OPENAI_API_KEY"] = os.environ["OPENAIAPIKEY"]
    openaiapi = os.environ["OPENAIAPIKEY"]
    cmpmdl = "gpt-3.5-turbo-16k"

    start_time = time.time()
    openai.api_key = openaiapi
    messages = [
        {"role": "system",
         "content": "你是一个专业的需求分析人员，可以根据输入的需求文档总结出相关的业务功能和业务规则。"},
        {"role": "user", "content": "以下用triple backticks括起来的内容是输入的需求文档：```" + inputreq + "```"},
        {"role": "assistant",
         "content": "以下用triple backticks括起来的内容是业务功能列表，业务功能列表的格式是：<业务功能名称>:<业务功能描述>。：```" + inputkws + "```"},
        {"role": "user",
         "content": "根据需求文档用一句话总结出其相关的业务描述，然后根据这句话在业务功能列表中选择出最相关的一个或一组业务功能（逐字逐句地），然后针对每个业务功能，从需求文档中找出相关的所有业务规则. "
                    "输出json格式为：{业务功能名称:{1：业务规则,2：业务规则},业务功能名称:{1：业务规则,2：业务规则}. "}
    ]
    completion = openai.ChatCompletion.create(
        model=cmpmdl,
        temperature=0,  # 0 - 2
        # max_tokens=512,
        # n=2,
        messages=messages
    )

    resultstring = completion.choices[0].message.content

    end_time = time.time()
    execution_time = end_time - start_time
    logging.info("openai.ChatCompletion execution_time:" + str(execution_time))

    logging.info("> [query] Total prompt token usage: " + str(completion.usage.prompt_tokens) + " tokens")
    logging.info("> [query] Total completion token usage: " + str(completion.usage.completion_tokens) + " tokens")
    logging.info("Keyword from ChatGPT: " + resultstring)

    start_index = resultstring.find('{')
    if start_index < 0:
        kwfromgpt = ""
    else:
        end_index = resultstring.rfind('}') + 1
        json_string = resultstring[start_index:end_index]
        kwfromgpt = json.loads(json_string)

    return kwfromgpt


def get_sample_tc(keyword, excel_file, sheet):
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    os.environ["OPENAI_API_KEY"] = os.environ["OPENAIAPIKEY"]
    hfapi = os.environ["HFAPIKEY"]
    hfdsrepo = "tinypace/sampletextcase"

    defaultexcelfile = "Default.xlsx"

    # -------------------找到所有与keyword相关的测试用例--------------------
    try:
        localfilepath = hf_hub_download(repo_id=hfdsrepo, filename=excel_file, repo_type="dataset", token=hfapi)
    except Exception as e:
        print("读取样例TC文件失败，使用Default文件：", str(e))
        localfilepath = hf_hub_download(repo_id=hfdsrepo, filename=defaultexcelfile, repo_type="dataset", token=hfapi)

    df = pd.read_excel(localfilepath, sheet_name=sheet)
    # print(df.to_string())
    query_engine = PandasQueryEngine(df=df, verbose=True)
    tcresult = query_engine.query(
        "选择出关于" + keyword + "的所有测试用例。以json的格式用unicode输出以下字段内容: 测试场景, 用例ID, 用例名称, 测试数据, 测试步骤, 预期结果, 重要程度")
    # ------------------------------------------------------------------
    logging.info("Selected TCs by Keyword: \n" + tcresult.response)

    return tcresult.response


def query_chatgpt(inputreq, sampletc):
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    os.environ["OPENAI_API_KEY"] = os.environ["OPENAIAPIKEY"]
    openaiapi = os.environ["OPENAIAPIKEY"]
    cmpmdl = "gpt-3.5-turbo-16k"

    # -------------------由chatgpt编写出相关的测试用例----------------------
    if inputreq == "" or  inputreq == "{}":
        return ""

    start_time = time.time()

    prompttext = CHATGPT_PROMPT_TMPL

    openai.api_key = openaiapi
    completion = openai.ChatCompletion.create(
        model=cmpmdl,
        temperature=0,  # 0 - 2
        # max_tokens=2048,
        # n=2,
        messages=[
            {"role": "system",
             "content": "你是一个专业的测试设计人员，可以根据需求文档编写测试用例。你参考样例测试用例，结合需求文档中的业务规则，以json的形式输出一系列测试用例。"},
            {"role": "assistant",
             "content": "以下用triple backticks括起来的内容是json格式的样例测试用例：```" + sampletc + "```"},
            {"role": "user", "content": "以下用triple backticks括起来的内容是输入的需求文档：```" + inputreq + "```"},
            {"role": "user",
             "content": prompttext},
        ]
    )
    # ------------------------------------------------------------------
    tcfromgpt = completion.choices[0].message.content

    end_time = time.time()
    execution_time = end_time - start_time
    logging.info("openai.ChatCompletion execution_time:" + str(execution_time))

    logging.info("> [query] Total prompt token usage: " + str(completion.usage.prompt_tokens) + " tokens")
    logging.info("> [query] Total completion token usage: " + str(completion.usage.completion_tokens) + " tokens")
    logging.info("TCs generated by ChatGPT:\n" + tcfromgpt.strip())

    return tcfromgpt


def chatbot(req):
    kwlist = kwfromhf("keywords.txt")
    keywords = summarize_keywords(req, kwlist)
    if len(keywords) == 0:
        return "", "无法根据输入的需求文档总结出有效的测试用例，请在需求文档中描述业务场景和规则。"

    sampletcs, tcs = [], []
    pattern = r'\[(.*?)\]'

    for key in keywords:
        keyreq = keywords[key]
        if len(keyreq) == 0:
            continue

        sampletc = get_sample_tc(key, key + ".xlsx", "Sheet1")
        sampletclist = re.findall(pattern, sampletc)
        sampletcs = sampletcs + sampletclist

        tc = query_chatgpt(str(keyreq), sampletc)
        tclist = re.findall(pattern, tc.replace("\n", ""))
        tcs = tcs + tclist

    return sampletcs, tcs
