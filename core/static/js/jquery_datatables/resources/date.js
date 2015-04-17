jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "date-es-pre": function ( a ) {
        if (a == '') {
            return 0;
        }
        var esDate = a.split('-');
        return (esDate[2] + esDate[1] + esDate[0]) * 1;
    },

    "date-es-asc": function ( a, b ) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "date-es-desc": function ( a, b ) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
});