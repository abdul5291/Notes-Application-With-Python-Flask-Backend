from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
  with open("data.txt", 'r') as f:
    data = f.read().splitlines()
  return render_template("index.html", data = data)

@app.route("/create", methods= ["GET", "POST"])
def create():
  if request.method == "POST":
    print(request.form.get('title'))
    print(request.form.get('content'))
    with open("data.txt", 'a') as f:
      f.write(f'''\n{request.form.get('title')} | {request.form.get('content')}''')
  return render_template("create.html")

@app.route("/edit/<int:line_id>", methods = ["GET", "POST"])
def edit(line_id):
  with open("data.txt", "r") as file:
    lines = file.read().splitlines()

    if request.method == "POST":
      new_title = request.form.get("title")
      new_content = request.form.get("content")
      new_content = new_content.replace("\n", " ").replace("\r", " ")
      lines[line_id] = f"{new_title} | {new_content}"

      with open("data.txt", "w") as file:

        for line in lines:
          file.write(line + "\n")
      return redirect(url_for("home"))
  
  current_text = lines[line_id]
  if "|" in current_text:
    current_title, current_content = current_text.split("|", 1)
  else:
    current_title = ""
    current_content = current_text
  return render_template("edit.html", line_id = line_id, title = current_title, content = current_content)

@app.route("/delete/<int:line_id>", methods = ["POST"] )
def delete(line_id):
  with open("data.txt", 'r') as f:
    data = f.read().splitlines()
    
    if 0 <= line_id < len(data):
      del data[line_id]

      with open("data.txt", 'w') as file:
        for line in data:
          file.write(line + "\n")
    return redirect(url_for('home'))

app.run(debug=True)