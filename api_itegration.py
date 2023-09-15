import os
import openai
import requests
import psycopg2
from datetime import datetime


openai.api_key="sk-5MZeWv2NZzOpFq***xXMWWeNZy"


QUESTION="tell me interesting 1 fact about RSA algorithm each fact in maximum 30 words"
SYSTEM_COMMAND="you are helpfull assisstent who gives just 1 fact"




def conversation_assistant_user(question:str, system_command:str):
    try:
        print('prompt   time --- ', datetime.now())
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", max_tokens=100, n=1, temperature=0.8,
            messages=[
                {"role": "user", "content": question},
                {"role": "system", "content" : system_command}
                    ])
        # print(response1)
        print(response.choices[0].message.content)
        return(response.choices[0].message.content)  
    except Exception as e:
        print('API CONNECTION ERROR \n', e)
        #conversation_assistant_user(system_role_prompt, system_role_expected_answer_format, question)

