from flask import Flask
from sudoku.views import top, new_record, index

app = Flask(__name__)

app.add_url_rule("/", view_func=index)
app.add_url_rule("/top/<n>/", view_func=top)
app.add_url_rule("/add_record/", view_func=new_record, methods=["POST"])
app.run()
