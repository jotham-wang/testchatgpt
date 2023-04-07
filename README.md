# testchatgpt
testchatgpt

目录和文件的作用：
1. 设置环境参数：.env/default.env
2. 本地知识库库dataset：dataset/
3. 全量知识库（用于rebuild）：docs/
4. 增量知识库（用于insert）：newdocs/
5. 建立本地库脚本：index.py
6. 运行脚本：app.py

使用的技术组件：
1. 前端：gradio
2. 本地知识库大模型：text-embedding-ada-002
3. completion大模型：gpt-3.5-turbo
4. dataset：local文件（pinecone还没有调通）