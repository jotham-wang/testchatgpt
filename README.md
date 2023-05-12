# testchatgpt

### 目录和文件的作用：
1. 设置环境参数：.env/default.env
2. 运行脚本：app.py
3. prompt提示模板：prompt_templates.py
4. 依赖库：requirements.txt
5. 把gradio api包了一层的api调用方式：chatbot_api.py

### 使用的技术组件：
1. 前端：gradio
2. 知识库：huggingface dataset
3. 知识库索引：llama-gpt GPTPandasIndex
4. 大模型：gpt-3.5-turbo
5. 部署：huggingface.co

### 部署方法：
1. 登录huggingface.co打开space：https://huggingface.co/spaces/tinypace/testcase
2. 在space右上的files tab中上传依赖库requirements.txt和主程序app.py
3. 上传知识库中的测试用例excel：https://huggingface.co/datasets/tinypace/sampletextcase
4. 更新知识库中的索引文件：https://huggingface.co/datasets/tinypace/sampletextcase/blob/main/keywords.txt
5. 设置环境参数（参考本地的default.env文件）
6. 如果需求要的话，调整prompt提示模板：https://huggingface.co/spaces/tinypace/testcase/blob/main/prompt_templates.py
7. 等待系统自动打包成docker镜像并部署

### 使用方法：
1. 登录huggingface.co打开space：https://huggingface.co/spaces/tinypace/testcase
2. 右上进入app tab
3. 输入一段需求的文字
4. 点击submit
5. 程序会首先搜索知识库中的案例，结果呈现在output1
6. 程序会带着知识库的信息进一步产生测试案例，结果呈现在output2
7. 如果需要的话，调整prompt提示模板，等待系统重新自动打包部署