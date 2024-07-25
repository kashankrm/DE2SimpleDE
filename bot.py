from utils import chat_completion as chat_model
import time

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

    def print_add_history(self, role, name, content):
        print(f"{name}: {content}\n")
        self.add_to_history(role, name, content)

    def talk(self, prompt, role=None, name=None, scratchpad_flag=False):
        history = self.history
        if scratchpad_flag:
            scratchpad_message = self.scratchpad
            history = history + [{"role": "assistant", "name": "bot", "content": "My temporary scratchpad is:\n" + scratchpad_message}]
        message = self.chat_completion(prompt, self.model_name, history, role, name)
        time.sleep(0.5)
        return message

    def assign_history(self, history):
        self.history = history
        return self.history

    def delete_history(self, i=None):
        if i is None:
            self.history = []
        else:
            del self.history[i]
        return self.history


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
