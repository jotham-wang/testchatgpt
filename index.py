from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext, GPTPineconeIndex
from langchain import OpenAI
import gradio as gr
import openai
import sys
import os
import pinecone


os.environ["OPENAI_API_KEY"] = os.environ["APIKEY"]
ebdmdl = os.environ["EMBEDDINGMDL"]
indexfile = 'dataset\\index-test.json'

pinecone.init(api_key=os.environ["PINECONEAPIKEY"], environment=os.environ['PINECONEENV'])
indexname = os.environ["PINECONEINDEX"]


def construct_index(directory_path, vector_store):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    # prepare model
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name=ebdmdl, max_tokens=num_outputs))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    # prepare docs and pinecone
    if not isEmpty(directory_path):
            documents = SimpleDirectoryReader(directory_path, file_metadata=get_file_metadata).load_data()

            if vector_store == "pinecone": # prepare pinecone if needed
                pinecone_index = pinecone.Index(indexname)
    else:
        print("directory invalid or empty")
        exit()

    # build index
    if directory_path == 'docs':    # rebuild index
        if vector_store == "pinecone":
            pinecone_index.delete(delete_all=True)
            indexpinecone = GPTPineconeIndex.from_documents(documents, pinecone_index=pinecone_index,
                                                            service_context=service_context)
        elif vector_store == "local":
            indexsimple = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        else:
            print("unknown vector store")
            exit()

    elif directory_path == 'newdocs':    # insert index

        if vector_store == "pinecone":
            indexpinecone = GPTPineconeIndex.from_documents(documents, pinecone_index=pinecone_index,
                                                            service_context=service_context)

        elif vector_store == "local":
            indexsimple = GPTSimpleVectorIndex.load_from_disk(indexfile, service_context=service_context)
            for doc in documents:
                indexsimple.insert(doc)
            indexsimple.save_to_disk(indexfile)

        else:
            print("unknown vector store")
            exit()

    else:
        print("unknown directory")
        exit()

    # return index
    if vector_store == "pinecone":
        return indexpinecone
    elif vector_store == "local":
        return indexsimple
    else:
        print("unknown vector store")
        exit()

# Define a fucntion to check whether
def isEmpty(path):
    if os.path.exists(path) and not os.path.isfile(path):
        # Checking if the directory is empty or not
        if not os.listdir(path):
            print("Empty directory")
            return True
        else:
            print("docs to be processed: " + str(os.listdir(path)))
            return False
    else:
        print("The path is either for a file or not valid")
        return True


# Define a function to extract metadata from each file
def get_file_metadata(file_path):
    # Extract file name and extension
    file_name, file_extension = os.path.splitext(file_path)
    # Return a dictionary with the metadata
    return {'name': file_name, 'extension': file_extension}


# main function

inputdir = input("Type the source dir of docs (default to \'newdocs\' for insert, or \'docs\' for rebuild): ") or "newdocs"
vecotrstore = input("Type the vector store to be used (default to \'pinecone\' for insert, other options include \'local\' : ") or "local"

index = construct_index(inputdir, vecotrstore)