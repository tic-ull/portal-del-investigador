tinyMCE.init({
    mode : "specific_textareas",
    theme : "modern",
    language: "es",
    docs_language : 'es',
    editor_deselector: "simpleTextArea",
    paste_auto_cleanup_on_paste : true,
    toolbar1 : "undo redo | bold italic underline | alignleft aligncenter alignright alignjustify | outdent indent | cut copy paste | cleanup code | bullist numlist | image link unlink",
    plugins : "table spellchecker paste searchreplace contextmenu link image code",
    cleanup: true,
    cleanup_on_startup: true,
    width : "100%",
    force_p_newlines : false
});
