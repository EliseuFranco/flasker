from flask import Flask, request, render_template


#Instancia do flask
app = Flask(__name__, static_folder="static", template_folder="templates")





@app.route("/")
def index():
    favorites = ["Pepperoni", "Margarida", 2,5,6]
    stuff = "This is a <strong>bold text</strong>"
    return render_template("index.html", stuff = stuff, lista = favorites)


@app.route("/user/<name>")
def user(name):
   return render_template("user.html", user=name)

# CREATING CUSTOM ERROR PAGE

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal server error 
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)