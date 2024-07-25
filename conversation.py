class Conversation:
    def __init__(self, bot):
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
            print(bot_output + "\n")
