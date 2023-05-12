#!/usr/bin/env python3
import os
import openai
import subprocess

openai_key_location = os.environ['HOME']+'/.openai_key'
messages = []

def read_conf():
    with open(openai_key_location, "r") as file:
        content = file.readline().strip()
    return content


def query_gpt(prompt):
    messages.append({'role':'user','content':prompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    messages.append({'role':'system','content':response["choices"][0]["message"]["content"]})
    return response["choices"][0]["message"]["content"]

def run_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output, error

if __name__ == "__main__":
    openai_key = read_conf()
    openai.api_key = openai_key
    
    while True:
        user_input = input("$ ")
    
        if user_input.lower() == "exit":
            break
        if user_input.lower()[:4] == "save":
            with open(user_input[5:], "w") as file:
                file.write(str(messages))
                print("> Saved!")
            continue
        if user_input.lower()[:4] == "load":
            with open(user_input[5:], "r") as file:
                file_contents = file.read()
                messages = eval(file_contents)
                print("> Loaded!")
                continue
        if user_input.lower() == "clear":
            os.system('clear')
            continue
        if user_input.lower() == "history":
            for message in messages:
                print(f"{message['role']}: {message['content']}")
            continue
        if user_input.lower()[:3] == "run":
            output, error = run_command(user_input[4:])
            print(output.decode("utf-8"))
            continue

        response = query_gpt(user_input)
        print(f"> {response.strip()}")
