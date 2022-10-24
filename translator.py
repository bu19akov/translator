import requests
from bs4 import BeautifulSoup
import argparse


class Translator:
    def __init__(self):
        self.language_from = None
        self.language_to = None
        self.word = None
        self.languages = ("Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish", "Portuguese", "Romanian", "Russian", "Turkish")

    def parsing(self):
        parser = argparse.ArgumentParser(description="This is translator. Available languages: arabic, german, english, spanish, french, hebrew, japanese, dutch, polish, portuguese, romanian, russian, turkish")
        parser.add_argument("language_from", help="Type your language.")
        parser.add_argument("language_to", help="Type the language you want to translate to.")
        parser.add_argument("word", help="Type the word you want to translate.")
        args = parser.parse_args()
        if not args.language_to in [i.lower() for i in self.languages] and args.language_to != "all":
            print(f"Sorry, the program doesn't support {args.language_to}")
            exit()
        elif not args.language_from in [i.lower() for i in self.languages]:
            print(f"Sorry, the program doesn't support {args.language_from}")
            exit()
        self.language_from = self.languages.index(args.language_from.capitalize())
        self.language_to = self.languages.index(args.language_to.capitalize()) if args.language_to != "all" else "all"
        self.word = args.word

    def translate(self, lang):
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = "https://context.reverso.net/translation/" + self.languages[self.language_from].lower() + "-" + self.languages[lang].lower() + "/" + self.word
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(f"Sorry, unable to find {self.word}")
            exit()
        soup = BeautifulSoup(r.content, 'html.parser')
        translations = [i.text for i in soup.find('span', {'class': 'display-term'})]
        phrases = "\n".join([i.text.replace("\r", "").replace("\n", "").strip() for i in soup.find('section', id="examples-content").find_all('span', class_="text")[:2]])
        str = ""
        str += f"\n{self.languages[lang]} Translations:\n"
        for i in translations:
            str += i + "\n"
        str += f"\n{self.languages[lang]} Examples:\n"
        str += phrases + "\n"
        return str

    def to_file(self):
        str = ""
        if self.language_to == "all":
            for lang in range(0, 13):
                if lang == self.language_from:
                    continue
                else:
                    str += self.translate(lang)
        else:
            str += self.translate(self.language_to)
        with open(f"{self.word}.txt", "w") as file:
            file.write(str)
        with open(f"{self.word}.txt", "r") as file:
            print(file.read())


translator = Translator()
translator.parsing()
translator.to_file()

