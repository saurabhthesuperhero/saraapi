from googletrans import Translator
from unidecode import unidecode

# translator = Translator()
# x = translator.translate("hello", dest="portuguese")
# print(unidecode(f" {format(x.pronunciation)}  This is how you will say  "))
import wikipedia
result = wikipedia.summary("who is vijay ", sentences=2)
print(unidecode(result)) 