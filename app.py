from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
import gradio as gr
import openai
import sys
import os
import logging
import pinecone
from gpt_index.data_structs.data_structs import PineconeIndexStruct
from gpt_index.indices.query.vector_store.queries import GPTPineconeIndexQuery


os.environ["OPENAI_API_KEY"] = os.environ.get("APIKEY")
username = os.environ.get("USERNM")
userpassword = os.environ.get("USERPW")
ebdmdl = os.environ["EMBEDDINGMDL"]
vector_store = "local"   # or "pinecone"
indexfile = 'dataset\\index-test.json'

pinecone.init(api_key=os.environ["PINECONEAPIKEY"], environment=os.environ['PINECONEENV'])
indexname = os.environ["PINECONEINDEX"]

def chatbot(input_text):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name=ebdmdl, max_tokens=num_outputs))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)


    if vector_store == "pinecone":
        pinecone_index = pinecone.Index(indexname)

    elif vector_store == "local":
        index = GPTSimpleVectorIndex.load_from_disk(indexfile, service_context=service_context)
    else:
        print("unknown vector store")
        exit()

    #print(str(index)[:300])

    #response = index.query(input_text, response_mode="compact")
    response = GPTPineconeIndexQuery(input_text, pinecone_index=pinecone_index,
                                  service_context=service_context)

    #print("Input Text:\n" + input_text + "\nResponse Text:" + str(response))

    prompttext = "create test cases according to the following business processes and rules:\n”" + input_text + "”\ntake the following supporting information into consideration：\n”" + str(response.response).lstrip("\n") + "”\npay attention to the following principles：\n  1. if the supporting information indicates that there is no clear answer, ignore the supporting information.\n  2. always respond in Chinese."

    logging.info("Prompt:\n" + str(prompttext).strip())

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        #n=2,
        messages=[
            {"role": "system", "content": "you are a helpful assistant in generating test cases."},
            {"role": "system", "content": "you will say no to the user if the question is not within your domain."},
            {"role": "system", "content": "you will translate the answers to Chinese as needed."},
            {"role": "user", "content": prompttext},
        ]
    )

    completiontext = completion.choices[0].message.content.lstrip("\n")

    logging.info("> [query] Total prompt token usage: " + str(completion.usage.prompt_tokens) + " tokens")
    logging.info("> [query] Total completion token usage: " + str(completion.usage.completion_tokens) + " tokens")
    logging.info("Completion:\n" + str(completiontext).strip())

    return str(response).strip(), str(completiontext).strip()

iface = gr.Interface(fn=chatbot,
                     inputs=gr.inputs.Textbox(lines=7, label="Enter your text"),
                     outputs=["text", "text"],
                     title="Test Case Generation Chatbot"
                     )

iface.launch(share=False, auth = (username, userpassword))