from get_sample_tc import get_sample_tc
import os
import gradio as gr

username = os.environ["USERNM"]
userpassword = os.environ["USERPW"]

if __name__ == '__main__':
    iface = gr.Interface(fn=get_sample_tc,
                         inputs=[gr.Textbox(label="输入测试用例库文件名（读取Sheet1）")],
                         outputs=[gr.Textbox(label="测试用例库输出json")],
                         allow_flagging="never",
                         title="Tinypace Sample Test Case Reader"
                         )

    iface.launch(share=False, auth=(username, userpassword))
    # iface.launch(share=False)