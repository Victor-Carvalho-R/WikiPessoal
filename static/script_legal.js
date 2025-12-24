// Muda de página e modifica a seleção na barra lateral

// Guarda o nome da tag no formulário
function delete_tag(button) {
    const tag = button.parentElement.parentElement.firstElementChild.textContent;
    button.form.elements["tag"].value = tag;
}

function edit_document(button) {
    const doc_title = button.parentElement.parentElement.parentElement.parentElement.firstElementChild.firstElementChild.textContent;
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
            doc_title = doc_content[0].textContent.toLowerCase();
            doc_txt = doc_content[2].textContent.toLowerCase();
            doc_span = doc_content[1].children;
            
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

function get_ai_output(button) {
    const prompt = document.getElementById("ai-input").value
    console.log(prompt)
    if (prompt) {
        const systemInstruction = `
            Você é um assistente de escrita para uma Wiki. 
            Sua tarefa é transformar as informações recebidas em conteúdo formatado para HTML.
            REGRAS:
            1. Use tags como <h2>, <p>, <ul>, <li>, <strong> conforme necessário.
            2. Não inclua as tags <html>, <head> ou <body>. Apenas o conteúdo interno.
            3. Seja enciclopédico e formal.
            4. Retorne APENAS o código HTML, sem explicações antes ou depois.
        `;

        document.getElementById("ai-wait-message").classList.remove("hidden")

        fetch('http://localhost:11434/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                model: 'llama3.1:latest',
                prompt: prompt,
                system: systemInstruction,
                stream: false
            }),
        })
        .then(response => {
            if (!response.ok) throw new Error('Erro na rede ou CORS');
            return response.json();
        })
        .then(data => {
            console.log(data.response)
            const ai_content_block = document.getElementsByClassName("ai-content-block")[0]
            ai_content_block.firstElementChild.innerHTML = data.response
            ai_content_block.classList.remove("hidden")

        })
        .catch(error => {
            console.error("Erro ao chamar o Ollama:", error);
            alert("Certifique-se de que o Ollama está rodando com OLLAMA_ORIGINS='*'");
        })
        .finally(() => {
            document.getElementById("ai-wait-message").classList.add("hidden")
        });
    } else {
        console.log("prompt para a ia errado, seu merda")
    }
}

function hide_ai_output() {
    const ai_content_block = document.getElementsByClassName("ai-content-block")[0]
    ai_content_block.firstElementChild.innerHTML = ""
    ai_content_block.classList.add("hidden")
}