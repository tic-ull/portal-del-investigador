tinyMCE.init({
    mode : "specific_textareas",
    theme : "advanced",
    language: "es",
    docs_language : 'es',
    editor_deselector: "simpleTextArea",
    theme_advanced_toolbar_location : "bottom",
    theme_advanced_toolbar_align : "center",
    theme_advanced_resize_horizontal : true,
    paste_auto_cleanup_on_paste : true,
    theme_advanced_buttons1 : "bold, italic, underline, separator, justifyleft, justifycenter, justifyright, justifyfull, separator, outdent, indent, separator, cut, copy, paste, separator, undo, redo, separator, cleanup, separator, bullist, numlist,separator,image, link,unlink",
    theme_advanced_buttons2 : "",
    theme_advanced_buttons3 : "",
    plugins : "table, spellchecker, paste, searchreplace, contextmenu",
    cleanup: true,
    cleanup_on_startup: true,
    width : "100%",
    force_p_newlines : false
});
