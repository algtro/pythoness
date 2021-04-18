from flask import Flask, render_template, request

import data as app_data

app = Flask(__name__)
app.secret_key = '90f5bbad727de239db9ed3fc0bd633776ee6ca59e35e02c6'
model = app_data.Model()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        answer = int(request.form.get('answer'))
        model.result(answer)
    return render_template("index.html",
                           user_history=model.user_history,
                           )


@app.route("/test/", methods=['POST'])
def start_test():
    return render_template("test.html",
                           pythonesses=model.pythonesses,
                           guess_min=app_data.GUESS_MIN,
                           guess_max=app_data.GUESS_MAX,
                           user_history=model.user_history,
                           )


if __name__ == '__main__':
    app.run()
