import os

import gradio as gr
import openai
import pandas as pd
from gpt_index.indices.struct_store import GPTPandasIndex
from huggingface_hub import hf_hub_download


def excel_gpt(req, keyword, excel_file, sheet):
    os.environ["OPENAI_API_KEY"] = os.environ["OPENAIAPIKEY"]
    openaiapi = os.environ["OPENAIAPIKEY"]
    cmpmdl = os.environ["COMPLETIONGMDL"]
    hfapi = os.environ["HFAPIKEY"]
    hfrepo = os.environ["HFREPO"]

    # -------------------找到所有与keyword相关的测试用例--------------------
    localfilepath = hf_hub_download(repo_id=hfrepo, filename=excel_file, repo_type="dataset", token=hfapi)
    df = pd.read_excel(localfilepath, sheet_name=sheet)
    # print(df.to_string())
    index = GPTPandasIndex(df=df)
    tc = index.query("选择出关于" + keyword + "的所有测试用例", verbose=True)
    # ------------------------------------------------------------------

    # -------------------由chatgpt编写出相关的测试用例----------------------
    openai.api_key = openaiapi
    completion = openai.ChatCompletion.create(
        model=cmpmdl,
        temperature=0,  # 0 - 2
        max_tokens=2048,
        # n=2,
        messages=[
            {"role": "system",
             "content": "你是一个专业的测试设计人员，可以根据需求文档编写测试用例。你参考样例测试用例，结合需求文档中的业务规则，以markdown的形式输出一系列测试用例。"},
            {"role": "assistant", "content": "以下是样例测试用例：```" + tc.response + "```"},
            {"role": "user", "content": "以下是输入的需求文档：```" + req + "```"},
            {"role": "user",
             "content": "根据输入的需求文档生成一套关于" + keyword + "的测试用例。请忽略掉样例测试用例中与需求文档无关的测试用例。"},
        ]
    )
    # ------------------------------------------------------------------

    return completion.choices[0].message.content


def chatbot(req):
    return excel_gpt(req, "银行转账", "samepletestcase.xlsx", "Sheet1")


username = os.environ.get("USERNM")
userpassword = os.environ.get("USERPW")

iface = gr.Interface(fn=chatbot,
                     inputs=gr.inputs.Textbox(lines=7, label="Enter your requirements"),
                     outputs=["text"],
                     title="Test Case Generation Chatbot"
                     )

iface.launch(share=False, auth=(username, userpassword))
