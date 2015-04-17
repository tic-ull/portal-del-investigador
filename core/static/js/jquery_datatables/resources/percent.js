(function() {
    var regex = /<span .*>\s*(.*)\%\s*<\/span>/;

    function getCleanText(text) {
        var rmatch = regex.exec(text);
        if (rmatch && rmatch.length == 2) {
            var percentage = rmatch[1];
        }
        else {
            percentage = text;
        }
        return percentage.trim()
    }

  jQuery.extend( jQuery.fn.dataTableExt.oSort, {
	  "percent-asc": function ( a, b ) {
          var x = parseFloat(getCleanText(a));
          var y = parseFloat(getCleanText(b));
          return ((x < y) ? -1 : ((x > y) ?  1 : 0));
	  },

	  "percent-desc": function ( a, b ) {
          var x = parseFloat(getCleanText(a));
          var y = parseFloat(getCleanText(b));
		  return ((x < y) ?  1 : ((x > y) ? -1 : 0));
	  }
  } );

}());