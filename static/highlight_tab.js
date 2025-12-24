function highlight_tab(pageId) {
    let pageIds = ["home", "create-document", "edit-document", "create-tag", "edit-tag"]
    
    for (let id = 0; id < 5; id++) {
        if (pageIds[id] !== pageId) {
            document.getElementById('nav-'+pageIds[id]).classList.remove("active");
            
        }
    }
    document.getElementById('nav-'+pageId).classList.add("active");
}