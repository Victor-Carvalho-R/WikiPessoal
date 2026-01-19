#! /home/victor/ProjetoWiki/.venv/bin/python3

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os


app = Flask(__name__)
path = os.getcwd()

# ler data.json
def get_data():
    with open(f"{path}/data.json", "r") as data_json:
        try:
            data = json.load(data_json)
        except:
            data = {"Documentos": {}, "Tags": {}}
    
    return data

# escrever em data.json
def set_data(data):
    with open(f"{path}/data.json", "w") as data_json:
        json.dump(data, data_json, indent=4)

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

@app.route("/manage-tags", methods=["GET"])
def open_create_tag():
    tags_content = get_tag_documents()
    return render_template("manage-tags.html", highlight="manage-tags", tags_content=tags_content)

@app.route("/edit-tag", methods=["GET"])
def open_edit_tag():
    tags_list = list_tags()
    return render_template("edit-tag.html", highlight="edit-tag", tags_list=tags_list)

# Visualizar documento
@app.route("/document", methods=["GET"])
def open_document():
    # ler data.json
    data = get_data()

    # organizar dados do documento
    doc_title = request.args.get("doc_title")
    docs_data = data["Documentos"]
    doc_data = (doc_title, docs_data[doc_title])

    return render_template("document.html", doc_data=doc_data)

# Criar documento
@app.route("/create-doc", methods=["POST"])
def create_doc():
    # ler data.json
    data = get_data()
    
    # Pegar e tratar conteúdo do documento
    content = request.form["doc-content"]
    content = content.replace("<p><br></p>", "\n")
    content = content.strip()
    content = content.replace( "\n", "<p><br></p>")

    # criar registro do documento
    docs_data = data["Documentos"]
    doc_title = request.form["doc-title"]
    selected_tags = json.loads(request.form["selected-tags"])
    docs_data[doc_title] = {"aud": "", "img": "", "txt": content, "vid": "", "tags": selected_tags}
    
    # adicionar nome do documento na tag
    tags_data = data["Tags"]
    for tagname in docs_data[doc_title]["tags"]:
        if not doc_title in tags_data[tagname]:
            tags_data[tagname].append(doc_title)

    # escrever em data.json
    data["Documentos"] = docs_data
    data["Tags"] = tags_data
    set_data(data)

    # pegar lista de documentos e tags
    docs_list = list_docs()
    tags_list = list_tags()
    
    return render_template("home.html", highlight="home", tags_list=tags_list, docs_list=docs_list)

# Editar documento
@app.route("/edit-doc", methods=["POST"])
def edit_doc():
    # pegar lista de documentos e tags
    tags_list = list_tags()
    docs_list = list_docs()

    # verificar se tem algum documento e guardar suas informações
    try:
        doc_title = request.form["doc"]
        doc_info = [doc for doc in docs_list if doc[0] == doc_title]
        doc_info = doc_info[0]
    except:
        doc_info = None

    return render_template("create-document.html", highlight="create-document", tags_list=tags_list, doc_info=doc_info)

# Deletar documento
@app.route("/delete-doc", methods=["POST"])
def delete_doc():
    # ler data.json
    data = get_data()
    
    # vriando variáveis para dados do documento
    docs_data = data["Documentos"]
    doc_title = request.form["doc"]
    selected_tags = docs_data[doc_title]["tags"]

    # deletar documento da tag
    tags_data = data["Tags"]
    for tagname in selected_tags:
        tags_data[tagname].remove(doc_title)


    docs_data.pop(doc_title)

    # escrever em data.json
    data["Documentos"] = docs_data
    data["Tags"] = tags_data
    set_data(data)

    # pegar lista de documentos e tags
    docs_list = list_docs()
    tags_list = list_tags()

    return render_template("home.html", highlight="home", tags_list=tags_list, docs_list=docs_list)

# Criar tag
@app.route("/manage-tags/create", methods=["POST"])
def create_tag():
    # ler data.json
    data = get_data()

    # criando registro da tag
    tags_data = data["Tags"]
    tag = request.form["tag-name"]
    tags_data[tag] = []

    # escrever em data.json
    data["Tags"] = tags_data
    set_data(data)

    # pegar lista de documentos e tags
    tags_content = get_tag_documents()

    return render_template("manage-tags.html", highlight="manage-tags", tags_content=tags_content)

# Deletar tag
@app.route("/manage-tags/delete", methods=["POST"])
def delete_tag():
    # ler data.json
    data = get_data()
    
    # criando variáveis para tags
    tags_data = data["Tags"]
    tag = request.form["tag"]

    # deletar tag do documento
    docs_data = data["Documentos"]
    for docname in tags_data[tag]:
        docs_data[docname]["tags"].remove(tag)

    # registro da tag deletado
    tags_data.pop(tag)

    # escrever em data.json
    data["Tags"] = tags_data
    data["Documentos"] = docs_data
    set_data(data)

    # pegar lista de documentos e tags
    tags_content = get_tag_documents()

    return render_template("manage-tags.html", highlight="manage-tags", tags_content=tags_content)

# Registrar tags recebidas do JS
@app.route("/manage-tags/registrar", methods=["POST"])
def registrar_tag():
    # ler data.json
    data = get_data()

    # pegando lista de tags
    tags_data = data["Tags"]
    tags = tags_data.keys()
    
    # verificar se tag existe. Caso não, criar o registro
    dados = request.get_json()
    tag = dados["tag"]
    if tag in tags:
        validacao = 0 # comunicar ao js que tag não será criada pois já existe
    else:
        validacao = 1 # comunicar ao js que tag será criada
        tags_data[tag] = []

        # escrever em data.json
        data["Tags"] = tags_data
        set_data(data)

    return jsonify({"validacao": validacao})


# Listar documentos
def list_docs():
    # ler data.json
    data = get_data()

    # organizar informações dos documentos
    docs_data = data["Documentos"]
    doc_data = []
    doc_names = docs_data.keys()
    for doc_name in doc_names:
        doc_tags = docs_data[doc_name]["tags"]
        doc_txt = docs_data[doc_name]["txt"]
        doc_data.append((doc_name, doc_tags, doc_txt))

    return doc_data

# Listar tags
def list_tags():
    # ler data.json
    data = get_data()

    # pegar lista de tags
    tags_data = data["Tags"]
    tags_name = tags_data.keys()

    return tags_name

def get_tag_documents():
    # ler data.json
    data = get_data()

    # pegar tags
    tags_data = data["Tags"]
    print(tags_data)

    return tags_data


# atualizar as tags com o nome dos documentos
def update_tag_docname(docname, selected_tags, action):
    # ler data.json
    data = get_data()

    # atualizar lista de documentos da tag
    tags_data = data["Tags"]
    for tag in selected_tags:
        if not docname in tags_data[tag]:
            if action == "append":
                tags_data[tag].append(docname)
            elif action == "remove":
                tags_data[tag].remove(docname)
    
    # escrever em data.json
    data["Tags"] = tags_data
    set_data(data)

# Iniciar programa
if __name__ == '__main__':
    CORS(app)
    app.run(debug=True)
