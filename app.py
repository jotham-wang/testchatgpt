from pipeline import chatbot
import os
import gradio as gr

username = os.environ["USERNM"]
userpassword = os.environ["USERPW"]

if __name__ == '__main__':
    iface = gr.Interface(fn=chatbot,
                         inputs=[gr.Textbox(lines=4, label="输入需求")],
                         outputs=[gr.Textbox(label="测试用例库输出"),
                                  gr.Textbox(label="ChatGPT输出")],
                         allow_flagging="never",
                         title="Tinypace Test Case Generator"
                         )

    iface.launch(share=False, auth=(username, userpassword))
    # iface.launch(share=False)