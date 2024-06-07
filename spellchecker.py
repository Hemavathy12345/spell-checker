from flask import Flask, render_template, request
import enchant
import requests

app = Flask(__name__)
dictionary = enchant.Dict("en_US")
api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_spelling():
    text = request.form['text']
    words = text.split()
    corrected_words = []
    word_definitions = []

    for word in words:
        if not dictionary.check(word):
            suggestion = dictionary.suggest(word)[0]
            corrected_words.append(suggestion)
        else:
            suggestion = word
            corrected_words.append(word)
        
        # Fetch definition
        response = requests.get(api_url + suggestion)
        if response.status_code == 200:
            definition = response.json()[0]['meanings'][0]['definitions'][0]['definition']
        else:
            definition = "No definition found."
        
        word_definitions.append((suggestion, definition))
    
    return render_template('result.html', words=word_definitions)

if __name__ == '__main__':
    app.run(debug=True)
