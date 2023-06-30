from gradio_client import Client
import os

def chatbot_api(req):

    hfapi = os.environ["HFAPIKEY"]
    hfsprepo = ""

    #client = Client("http://127.0.0.1:7860")
    client = Client(hfsprepo, hf_token=hfapi)
    result = client.predict(
        req,  # str representing string value in '输入需求' Textbox component
        api_name="/predict"
    )

    return result

print(chatbot_api("test"))
