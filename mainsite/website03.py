from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
def start():
    return render_template("lang.html")

@app.route('/home')
def Home():
    return render_template("home.html")

@app.route('/preface')
def Prologue():
    return render_template("preface.html")

@app.route('/Introduction')
def Introduction():
    return render_template("Introduction.html")

@app.route('/chapter2')
def Chapter2():
    return render_template("chapter2.html")

@app.route('/chapter3')
def Chapter3():
    return render_template("chapter3.html")

@app.route('/chapter4')
def Chapter4():
    return render_template("chapter4.html")

@app.route('/chapter5')
def Chapter5():
    return render_template("chapter5.html")

@app.route('/Conclusion')
def conclusion():
    return render_template("Conclusion.html")

@app.route('/afterword')
def Epilogue():
    return render_template("afterword.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/lang')
def lang():
    return render_template("lang.html")

@app.route('/thuis')
def thuis():
    return render_template("thuis.html")

@app.route('/voorwoord')
def voorwoord():
    return render_template("voorwoord.html")

@app.route('/introductie')
def introductie():
    return render_template("introductie.html")

@app.route('/hoofdstuk2')
def hoofdstuk2():
    return render_template("hoofdstuk2.html")

@app.route('/hoofdstuk3')
def hoofdstuk3():
    return render_template("hoofdstuk3.html")

@app.route('/hoofdstuk4')
def hoofdstuk4():
    return render_template("hoofdstuk4.html")

@app.route('/hoofdstuk5')
def hoofdstuk5():
    return render_template("hoofdstuk5.html")

@app.route('/conclusie')
def conclusie():
    return render_template("conclusie.html")

@app.route('/nawoord')
def nawoord():
    return render_template("nawoord.html")

@app.route('/over')
def over():
    return render_template("over.html")

@app.route('/testing')
def test():
    return render_template("test.html")

if __name__ == "__main__":
    app.run()

