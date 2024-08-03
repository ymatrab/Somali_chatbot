from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_openai import OpenAI
from authentification import verify_connection,get_memory,message_from_chat


import os
os.environ["OPENAI_API_KEY"] = ''

from langchain_openai import ChatOpenAI
###
llm = ChatOpenAI(model="gpt-4o-mini")

# from openai import OpenAI

def get_session_history(user_id: str, conversation_id: str):
    return SQLChatMessageHistory(f"{user_id}--{conversation_id}", "sqlite:///memory.db")

def add_messages_to_history(message_history, message: dict):
    if message['role'] == 'user':
        message_history.add_message(HumanMessage(message['text']))
    else:
        message_history.add_message(AIMessage(message['text']))
    return message_history

def get_output(input,user_id,conversation_id,file_path=None):
    if not verify_connection(user_id):
        return {'response':'verify your auth please'}
    else:
        #set memory
        memory=get_memory(conversation_id)
        if memory['user_id'] != user_id:
            return {'response':'something worng !'}
        else:
          history=[]
          if memory:
              for chat in memory['chat']:
                try:  
                  message = message_from_chat(chat)
                  history.append(message)
                except Exception as e:
                    print(e)
                    pass
          message_history = get_session_history(123, 1)
          if message_history.messages:
              message_history.clear()
          for message in history:
              message_history=add_messages_to_history(message_history,message)
          message_history = get_session_history(123, 1)

          #process input
          
          if file_path:
              file_path=file_path
              content=gpt_ocr('user_id',file_path,auth=True)
              input = 'nuxurka sawirka:\n'+ content + input
          
          prompt = ChatPromptTemplate.from_messages(
              [
                  MessagesPlaceholder(variable_name="history"),
                  ("human", "{input}"),
              ]
          )
          runnable = prompt | llm

          with_message_history = RunnableWithMessageHistory(
          runnable,
          get_session_history,
          input_messages_key="input",
          history_messages_key="history",
          history_factory_config=[
                  ConfigurableFieldSpec(
                      id="user_id",
                      annotation=str,
                      name="User ID",
                      description="Unique identifier for the user.",
                      default="",
                      is_shared=True,
                  ),
                  ConfigurableFieldSpec(
                      id="conversation_id",
                      annotation=str,
                      name="Conversation ID",
                      description="Unique identifier for the conversation.",
                      default="",
                      is_shared=True,
                  ),
              ],
          )
      
          response=with_message_history.invoke(
              {"input": f"{input}"},
              config={"configurable": {"user_id": f"{123}", "conversation_id": f"{1}"}},
              )
          return response


def chat_with_image(input,user_id,file_paths,auth=None):
    if not auth:
      if not verify_connection(user_id):
          return {'response':'verify your auth please'}
    from openai import OpenAI
    client = OpenAI()
    if isinstance(file_paths, str):
        file_paths = [file_paths]
    content = [{"type": "text", "text": f"{input}"}]
    
    # Append images to the content
    for file_path in file_paths:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"{file_path}",
            },
        })
    

    message={
      "role": "user",
      "content": content
    }
    
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        message
    ],
    max_tokens=500,
    )

    return response.choices[0].message.content

def gpt_ocr(user_id,file_paths,auth=None):
    input="Extract text from the image/s"
    return chat_with_image(input,user_id,file_paths,auth=None)