#! /home/victor/Documents/ProjetoWiki/venvWiki/bin/python3

from flask import Flask, render_template, request
import json


app = Flask(__name__)
path = "/home/victor/Documents/ProjetoWiki/"

# Abrir home 
@app.route('/')
def index():
    docs_list = list_docs()
    tags_list = list_tags()

    return render_template('home.html', highlight="home", tags_list=tags_list, docs_list=docs_list)

# GETS
@app.route("/create-doc", methods=["GET"])
def open_create_doc():
    tags_list = list_tags()
    return render_template("create-document.html", highlight="create-document", tags_list=tags_list)

@app.route("/edit-doc", methods=["GET"])
def open_edit_doc():
    docs_list = list_docs()
    return render_template("edit-document.html", highlight="edit-document", docs_list=docs_list)

@app.route("/create-tag", methods=["GET"])
def open_create_tag():
    return render_template("create-tag.html", highlight="create-tag")

@app.route("/edit-tag", methods=["GET"])
def open_edit_tag():
    tags_list = list_tags()
    return render_template("edit-tag.html", highlight="edit-tag", tags_list=tags_list)

@app.route("/document", methods=["GET"])
def open_document():
    doc_title = request.args.get("doc_title")
    with open(f"{path}/data/documents.json", "r") as docs_json:
        try:
            docs_data = json.load(docs_json)
        except:
            docs_data = {}
    doc_data = (doc_title, docs_data[doc_title])
    return render_template("document.html", doc_data=doc_data)

# Criar documento
@app.route("/create-doc", methods=["POST"])
def create_doc():
    with open(f"{path}/data/documents.json", "r") as docs_json:
        try:
            docs_data = json.load(docs_json)
        except:
            docs_data = {}
    
    title = request.form["doc-title"]
    content = request.form["doc-content"]
    selected_tags = json.loads(request.form["selected-tags"])
    docs_data[title] = {"aud": "", "img": "", "txt": "", "vid": "", "tags": selected_tags}
    docs_data[title]["txt"] = content

    with open(f"{path}/data/documents.json", "w") as docs_json:
        json.dump(docs_data, docs_json, indent=4)

    docs_list = list_docs()
    tags_list = list_tags()
    
    return render_template("create-document.html", highlight="create-document", tags_list=tags_list, docs_list=docs_list)

# Editar documento
@app.route("/edit-doc", methods=["POST"])
def edit_doc():
    docs_list = list_docs()
    try:
        doc_title = request.form["doc"]
        doc_content = [doc for doc in docs_list if doc[0] == doc_title]
        doc_content = doc_content[0]
    except:
        doc_content = None
    tags_list = list_tags()
    return render_template("create-document.html", highlight="create-document", tags_list=tags_list, doc_content=doc_content)

# Deletar documento
@app.route("/delete-doc", methods=["POST"])
def delete_doc():
    doc_title = request.form["doc"]

    with open(f"{path}/data/documents.json", "r") as docs_json:
        docs_data = json.load(docs_json)
        
        docs_data.pop(doc_title)

    with open(f"{path}/data/documents.json", "w") as docs_json:
        json.dump(docs_data, docs_json, indent=4)

    docs_list = list_docs()
    tags_list = list_tags()

    return render_template("edit-document.html", highlight="edit-document", tags_list=tags_list, docs_list=docs_list)

# Criar tag
@app.route("/create-tag", methods=["POST"])
def create_tag():
    tag = request.form["tag-name"]

    # mudando tags.json
    with open(f"{path}/data/tags.json", "r") as tags_json:
        try:
            tags_data = json.load(tags_json)
        except:
            tags_data = {}

    tags_data[tag] = []

    with open(f"{path}/data/tags.json", "w") as tags_json:
        json.dump(tags_data, tags_json, indent=4)

    docs_list = list_docs()
    tags_list = list_tags()

    return render_template("create-tag.html", highlight="create-tag", tags_list=tags_list, docs_list=docs_list)

# Deletar tag
@app.route("/delete-tag", methods=["POST"])
def delete_tag():
    tag = request.form["tag"]

    with open(f"{path}/data/tags.json", "r") as tags_json:
        tags_data = json.load(tags_json)
        
        tags_data.pop(tag)

    with open(f"{path}/data/tags.json", "w") as tags_json:
        json.dump(tags_data, tags_json, indent=4)

    docs_list = list_docs()
    tags_list = list_tags()

    return render_template("edit-tag.html", highlight="edit-tag", tags_list=tags_list, docs_list=docs_list)

# Listar documentos
def list_docs():
    with open(f"{path}/data/documents.json", "r") as docs_json:
        try:
            docs_data = json.load(docs_json)
            doc_data = []
            for doc_name in docs_data.keys():
                doc_tags = docs_data[doc_name]["tags"]
                doc_txt = docs_data[doc_name]["txt"]
                doc_data.append((doc_name, doc_tags, doc_txt))
        except:
            doc_data = []
    return doc_data

# Listar tags
def list_tags():
    with open(f"{path}/data/tags.json", "r") as tags_json:
        try:
            tags_data = json.load(tags_json)
            tags_name = tags_data.keys()
        except:
            tags_name = ""
    
    return tags_name

# Iniciar programa
if __name__ == '__main__':
    app.run(debug=True)
