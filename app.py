from pipeline import chatbot
import gradio as gr

if __name__ == '__main__':
    iface = gr.Interface(fn=chatbot,
                         inputs=[gr.inputs.Textbox(lines=4, label="输入需求")],
                         outputs=[gr.outputs.Textbox(label="测试用例库输出"),
                                  gr.outputs.Textbox(label="ChatGPT输出")],
                         allow_flagging="never",
                         title="Tinypace Test Case Generator"
                         )

    # iface.launch(share=False, auth=(username, userpassword))
    iface.launch(share=False)
