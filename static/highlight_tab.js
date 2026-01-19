function highlight_tab(pageId) {
    const pageIds = ["home", "create-document", "manage-tags"]

    for (let id = 0; id < pageIds.length; id++) {
        if (pageIds[id] !== pageId) {
            document.getElementById('nav-'+pageIds[id]).classList.remove("active");
            
        }
    }
    document.getElementById('nav-'+pageId).classList.add("active");
}