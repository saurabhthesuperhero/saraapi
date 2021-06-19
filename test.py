from googletrans import Translator
from unidecode import unidecode
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
warnings.filterwarnings("ignore", category=UserWarning, module='wikipedia')

# translator = Translator()
# x = translator.translate("hello", dest="portuguese")
# print(unidecode(f" {format(x.pronunciation)}  This is how you will say  "))
import wikipedia
def wiki():
    try:
        result = wikipedia.summary("study", sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e :
        # print(e)
        return "helo"+repr(e)[5:]
    else:
        return "lol"        
# print(unidecode(result)) 
print(wiki())