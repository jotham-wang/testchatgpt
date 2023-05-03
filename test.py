import os

import openai
import pandas as pd
from gpt_index.indices.struct_store import GPTPandasIndex


def excelGPT(inputtext, excel_file, sheet):
    # my GPT Key
    os.environ["OPENAI_API_KEY"] = os.environ["OPENAIAPIKEY"]
    # Working Directory for training
    root_folder = ''
    openaiapi = os.environ["OPENAIAPIKEY"]
    cmpmdl = os.environ["COMPLETIONGMDL"]
    df = pd.read_excel(excel_file, sheet_name=sheet)
    # print(df.to_string())

    # -------------------------------------------------
    index = GPTPandasIndex(df=df)

    tc = index.query("选择出关于" + inputtext + "的所有测试用例", verbose=True)
    # -------------------------------------------------

    req = "在银行转账服务中，客户需要提供受益人的姓名、账户号码和转账金额等信息。这些信息是必要的，以确保转账服务的准确性和可靠性。在提供这些信息时，客户还应注意确保其准确性和完整性，以免因输入错误的信息而导致转账失败或资金丢失的情况发生。因此，在进行转账操作时，客户应仔细检查所提供的信息，并确保其与实际情况相符。\n" + \
    "在银行转账服务中，客户需要提供以下信息，以确保转账服务的准确性和可靠性：\n" + \
    "- 受益人姓名\n" + \
    "- 受益人账户号码\n" + \
    "- 转账金额\n" + \
    "如果受益人不是本行客户，系统应提示警告：受益人不是本行客户，转账不能及时到账。\n" + \
    "在提供这些信息时，客户还应注意确保其准确性和完整性，以免因输入错误的信息而导致转账失败或资金丢失的情况发生。因此，在进行转账操作时，客户应仔细检查所提供的信息，并确保其与实际情况相符。\n"
    print(req)

    openai.api_key = openaiapi
    completion = openai.ChatCompletion.create(
        model=cmpmdl,
        temperature=0, # 0 - 2
        max_tokens=2048,
        # n=2,
        messages=[
            {"role": "system", "content": "你是一个专业的测试设计人员，可以根据需求文档编写测试用例。你参考样例测试用例，结合需求文档中的业务规则，以markdown的形式输出一系列测试用例。"},
            {"role": "assistant", "content": "以下是样例测试用例：```" + tc.response + "```"},
            {"role": "user", "content": "以下是输入的需求文档：```" + req + "```"},
            {"role": "user", "content": "根据输入的需求文档生成一套关于" + inputtext + "的测试用例。请忽略掉样例测试用例中与需求文档无关的测试用例。"},
        ]

    )

    return completion.choices[0].message.content


print(excelGPT("银行转账", "samepletestcase.xlsx", "Sheet1"))
