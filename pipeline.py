from datetime import datetime, timedelta
import random
from utils import chat_completion as chat_model, html2text, search_with_sites, download_page
import asyncio
import requests
import time
from dotenv import load_dotenv
import os
load_dotenv()


def get_news( query, from_date, sort_by='popularity'):
    api_key = os.getenv('NEWS_API_KEY')
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'from': from_date,
        'sortBy': sort_by,
        'apiKey': api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.status_code, 'message': response.text}

#Bot class takes model name and has a scractpad
class Bot:
    def __init__(self, model_name):
        self.model_name = model_name
        self.scratchpad = ""
        self.chat_completion = chat_model
        self.history = []

    
    def add_to_history(self, role, name, content):
        assert role in ["system", "assistant", "user"], "Role must be one of system, assistant, user"
        message = {"role": role, "name": name, "content": content}
        self.history.append(message)
        return self.history
    
    def print_add_history(self,role,name,content):
        print(f"{name}: {content}\n")
        self.add_to_history(role,name,content)

    def talk(self, prompt, role=None, name=None, scratchpad_flag=False):
        history = self.history
        if scratchpad_flag:
            scratchpad_message = self.scratchpad
            history = history + [{"role": "assistant", "name": "bot", "content": "My temporary scratchpad is:\n"+scratchpad_message}]
        message = self.chat_completion(prompt, self.model_name, history, role, name)
        time.sleep(0.5)
        return message

    def assign_history(self, history):
        self.history = history
        return self.history

    def delete_history(self,i=None):
        if i is None:
            self.history = []
        else:
            del self.history[i]
        return self.history
    

class Pipe:
    def __init__(self, inputs, outputs, prompt):
        self.inputs = inputs
        self.outputs = outputs
        self.prompt = prompt
        self.bot = None
        self.output = None
    
    def set_bot(self, bot):
        self.bot = bot
    
    def run(self):
        assert self.bot is not None, "Bot must be set before running the pipe"
        prompt = self.prompt
        for input in self.inputs:
            prompt += input
        self.output = self.bot.talk(prompt)
        return self.output 

# coversation class uses Bot class to create a conversation wth user
class Conversation:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.hooks = []
        self.run_conversation = True
        self.add_hook(self.quit_hook)
    
    def add_hook(self, hook):
        self.hooks.append(hook)
    
    def handle_hooks(self, message):
        for hook in self.hooks:
            triggered = hook(message)
            if triggered:
                return True
        return False    
    def quit_hook(self, message):
        if message == "quit":
            print("quit hook triggered")
            self.run_conversation = False
            return True
        return False
    
    def start_conversation(self):
        # print("Bot: Hello, I am a chatbot. What is your name?\n")
        # self.bot.add_to_history("system", "bot", "Hello, I am a chatbot. What is your name?")
        
        while self.run_conversation:
            print("You: ", end="")
            user_input = ""
            while user_input == "":
                inp = input().strip()
                if inp == "":
                    continue
                else:
                    user_input = inp
            
            skip = self.handle_hooks(user_input)
            if skip:
                continue
            self.bot.add_to_history("user", "user", user_input)
            print("\nBot: ", end="")
            bot_output = self.bot.talk(user_input, "user", "user")
            self.bot.add_to_history("assistant", "bot", bot_output)
            print(bot_output+"\n")
class DE2A2DEBot(Bot):
    def __init__(self, model_name):
        super().__init__(model_name)

    def transcribe(self, text):
        prompt = (
            "You are a German language tutor specializing in A2 level. Your task is to rewrite the provided text "
            "in a simpler form so that A2 level students can understand it. After simplifying the text, provide a list of difficult "
            "words along with their meanings in English. Ensure the simplified text retains the original meaning as much as possible."
        )
        self.print_add_history("system", "user_admin", prompt)
        self.print_add_history("user", "user_ex", text)
        ans = self.talk("", "assistant", "tutor")
        return ans

