import re
# Imported the Flask class
from flask import Flask
from flask import request
# import sys
# sys.path.append('../')
import initial_histogram as histogram
import setup
import random
# Made a new instance of the Flask class, with name of the module being the
# variable so Flask knows attributes, files, etc. The reason we use '__name__'
# instead of '__main__' is because if this file was imported, it wouldn't be
# main anymore, which would cause a whole lot of errors. '__name__' is dynamic
app = Flask(__name__)
first_order_table = setup.setupFirstOrder()
second_order_table = None

# Creating a new base/home http route
@app.route("/")
def home_route():
    return (
        '<img src="https://i.dlpng.com/static/png/6866331_thumb.webp" />'\
        "<h1>Hello, Welcome to Shane's Drake Lyric Generator API!</h1> <br/><br/> "\
        "<h3>Feel free to visit:</h3><br/>"\
        "<b>GET: /random/</b> - <br/><pre>For a randomly generated Drake Lyric</pre><br/>"\
        "<b>GET: /random?{originality}/</b> - <br/><pre>For a generated Drake Lyric, where {originality} is a boolean that represents how much do you want the <br/>generated lyric to be like one of his actual lyrics; where 'false' would give you a lyric that sounds very similar to his existing lyrics, <br/>and 'true' would give you a vaguely Drake-like lyrics. <b><i>Example: '/random?originality=true'</i></b></pre> <br/>"\
        "<b>GET: /random?{originality}&{length}/</b> - <br/><pre>Similar to '/random/{originality}/', but {length} is an integer that represent how long do you want the lyric to be. <b><i>Example: '/random?originality=2&length=140/'</i></b></pre> <br/>"
    )

@app.route("/random")
def random_sentence_route():
    originality = request.args.get('originality') if request.args.get('originality') else ""
    length = request.args.get('length') if request.args.get('length') else ""
    is_second_order = (originality == "true")
    generated_sentence = setup.generate(
        first_order = not is_second_order,
        num_words = int(length) if length.isdigit() else 140, 
        table= second_order_table if is_second_order else first_order_table
    )
    return '<h1>Drake Generator says:</h1> </b></b>' + generated_sentence + '... <br/><br/><img src="https://scstylecaster.files.wordpress.com/2016/04/drake-odell-beckham1.jpg">'

    # index = random.randint(1, 10)
    # return histogram.random_word_histogram_with_word_frequency_factor(index)

if __name__ == "__main__":
    app.run()
    second_order_table = setup.setupSecondOrder()
