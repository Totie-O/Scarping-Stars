import random
from termcolor import colored
from simpleeval import simple_eval
from C2_data_scraping_lookup import Star
import time

class Bot:
    ## Use this class variable to set the delay before each bot output
    wait = 0.2

    def __init__(self, runtype='once'):
        self.q = ''
        self.a = ''
        self.runtype = runtype
    
    def _think(self, s):
        return s

    def _say(self, s):
        time.sleep(Bot.wait)
        print(colored(s, 'blue'))

    def _run_once(self):
        self._say(self.q)
        self.a = input()
        self._say(self._think(self.a))

    def _run_looped(self):
        self._say(self.q)
        while True:
            self.a = input()
            if self.a.lower() in ['exit', 'quit', 'x', 'q']:
                break
            self._say(self._think(self.a))

    def run(self):
        if self.runtype == 'once':
            self._run_once()
        elif self.runtype == 'looped':
            self._run_looped()


class HelloBot(Bot):
    def __init__(self, runtype='once'):
        super().__init__(runtype)
        self.q = 'What\'s you name?'
    
    def _think(self, s):
        return f'Hello {s}!'
    
class GreetingBot(Bot):
    def __init__(self, runtype='once'):
        super().__init__(runtype)
        self.q = 'How are you today?'
        
    def _think(self, s):
        if 'good' in s.lower():
            return 'I\'m feeling good too!'
        else:
            return 'Sorry to hear that.'    
        
class FavoriteColorBot(Bot):
    def __init__(self, runtype='once'):
        super().__init__(runtype)
        self.q = 'What\'s your favorite color?'
        
    def _think(self, s):
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'purple']
        return f'You like {s}? That\'s a great color. My favorite color is {random.choice(colors)}.'
    
class CalcBot(Bot):
    def __init__(self, runtype='once'):
        super().__init__(runtype)
        self.q = "Through recent upgrade I can do calculation now. Input some arithmetic expression to try." 
        if self.runtype == 'looped':
            self.q = self.q + " Type 'exit', 'quie', 'x', 'q' to quit."

    def _think(self, s):
        result = simple_eval(s)
        return f'Done. Result = {result}'

    # The first level answer 
    # 
    # def run(self):
    #     self._say(self.q)
    #     while True:
    #         self.a = input()
    #         if self.a.lower() in ['exit', 'quit', 'x', 'q']:
    #             break
    #         self._say(self._think(self.a))

        
class FavoriteStar(Bot):
    def __init__(self, runtype='once'):
        super().__init__(runtype)
        self.q = "Tell me the corresponding zodiac sign, and I can provide you with the corresponding information."
        if self.runtype == 'looped':
            self.q = self.q + " Type 'exit', 'quie', 'x', 'q' to quit."

    def _think(self, s):
        result = Star(s)
        return f'Done. {result}'


if __name__ == '__main__':
    h = HelloBot()
    g = GreetingBot()
    f = FavoriteColorBot()
    c = CalcBot('looped')
    f_stars =  FavoriteStar()

    h.run()
    g.run()
    f.run()
    f_stars.run()
    c.run()



    
