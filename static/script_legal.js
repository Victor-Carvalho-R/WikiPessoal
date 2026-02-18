// Muda de página e modifica a seleção na barra lateral

// Guarda o nome da tag no formulário
function delete_tag(button) {
    const tag = button.parentElement.parentElement.firstElementChild.textContent;
    button.form.elements["tag"].value = tag;
}

function edit_document(button) {
    const doc_title = button.parentElement.parentElement.parentElement.firstElementChild.firstElementChild.textContent;
    button.form.elements["doc"].value = doc_title;
}

function toggle_tag(div_tag) {
    div_tag.classList.toggle('selected');
}

function get_selected_tags(button) {
    const selected_tags = Array.from(document.querySelectorAll('.selected')).map(el => el.textContent);
    button.form.elements["selected-tags"].value = JSON.stringify(selected_tags);
}

function search_documents(search) {
    const doc_cards = document.querySelectorAll('.document-card');
    const lower_search = search.toLowerCase();
    const lower_search_array = lower_search.split(" ");
    
    for (const search_word of lower_search_array) {
        for (const doc_card of doc_cards) {
            doc_content = doc_card.children;
            doc_title = doc_content[0].firstElementChild.textContent.toLowerCase();
            doc_txt = doc_content[1].textContent.toLowerCase();
            doc_span = doc_content[0].lastElementChild.children;
            
            if (!doc_title.includes(search_word) && !doc_txt.includes(search_word)) {
                for (const span of doc_span) {
                    doc_tag = span.textContent.toLowerCase()
                    if (!doc_tag.includes(search_word)) {
                        doc_card.parentElement.classList.add("hidden");
                    } else {
                        doc_card.parentElement.classList.remove("hidden");
                        break;
                    }
                }
            } else {doc_card.parentElement.classList.remove("hidden")}
        }
    }
}

function search_tags(search) {
    const tag_instances = document.querySelectorAll('.tag-instance');
    const lower_search = search.toLowerCase();
    
    for (const tag_instance of tag_instances) {
        tag_name = tag_instance.firstElementChild.firstElementChild.textContent;
        lower_tag_name = tag_name.toLowerCase()
        
        if (!lower_tag_name.includes(lower_search)) {
            tag_instance.parentElement.classList.add("hidden");
        } else {tag_instance.parentElement.classList.remove("hidden")}
    }
}

async function get_ai_output(button) {
    const prompt = document.getElementById("ai-input").value

    if (prompt) {
        document.getElementById("ai-wait-message").classList.remove("hidden")

        try {
            const response = await fetch('http://127.0.0.1:5000/api', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt: prompt })
            });

            const ai_output = await response.json();
            console.log("Resposta do Python:", ai_output.output);
            const ai_content_block = document.getElementsByClassName("ai-content-block")[0]
            ai_content_block.firstElementChild.innerHTML = ai_output.output
            ai_content_block.classList.remove("hidden")
            
            document.getElementById("ai-wait-message").classList.add("hidden")
        } catch (error) {
            console.error("Erro ao conectar:", error);
        }    
    }
}

function hide_ai_output() {
    const ai_content_block = document.getElementsByClassName("ai-content-block")[0]
    ai_content_block.firstElementChild.innerHTML = ""
    ai_content_block.classList.add("hidden")
}

function create_tag_via_create_document(button) {
    const tag_nova = button.parentElement.firstElementChild.value
    const div_tags = document.getElementById("tag-selector")
    
    fetch("http://localhost:5000/manage-tags/registrar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({tag: tag_nova})
    })
    .then(res => res.json())
    .then(data => {
        if (data.validacao) {
            div_tags.innerHTML += "<div class='tag-option' onclick='toggle_tag(this)'>" + tag_nova + "</div>"
        }
    });
}