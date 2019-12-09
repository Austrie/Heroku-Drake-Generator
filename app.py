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
second_order_table = setup.setupSecondOrder()

# Creating a new base/home http route
@app.route("/")
def home_route():
    return re.compile(
        "Hello, Welcome to Shane's Drake Lyric Generator API! \n \n"
        "Feel free to visit:\n"
        "/random/ - For a randomly generated Drake Lyric\n"
        "/random?{originality}/ - For a generated Drake Lyric, where {originality} is a boolean that represents how much do you want the generated lyric to be like one of his actual lyrics; where 'false' would give you a lyric that sounds very similar to his existing lyrics, and 'true' would give you a vaguely Drake-like lyrics. Example: '/random?originality=true' \n"
        "/random?{originality}&{length}/ - Similar to '/random/{originality}/', but {length} is an integer that represent how long do you want the lyric to be. '/random?originality=2&length=140/' \n"
    )

@app.route("/random")
def random_sentence_route():
    originality = request.args.get('originality')
    length = request.args.get('length')
    print "originality: " + str(originality)
    print "originality: " + str(type(originality))
    print "length: " + str(length)
    print "length: " + str(type(length))
    return ""
    # return setup.generate(order=1, table=table)
    # index = random.randint(1, 10)
    # return histogram.random_word_histogram_with_word_frequency_factor(index)

if __name__ == "__main__":
    app.run()
