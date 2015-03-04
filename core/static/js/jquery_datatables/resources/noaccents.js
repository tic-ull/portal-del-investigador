(function() {
    var regex = /<a href=".*">(.*)<\/a>/;
    var dictionary = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ü": "U"};

    function getCleanText(text) {
        var match = regex.exec(text);
        if (match.length == 2) {
            var x = match[1];        
        }
        else {
            x = text;
        }
        x = x.toUpperCase();
        for (var key in dictionary) {
            x = x.replace(key, dictionary[key]);
        }
        return x;
    }

    function accent_sort(a, b) {
        var x = getCleanText(a);
        var y = getCleanText(b);
        if (x < y) {
          return -1;
        }
        if (x > y) {
          return 1;
        }
	    return 0;
  }

  jQuery.extend( jQuery.fn.dataTableExt.oSort, {
	  "noaccents-asc": function ( a, b ) {
		  return accent_sort(a,b);
	  },

	  "noaccents-desc": function ( a, b ) {
		  return accent_sort(a,b) * -1;
	  }
  } );

}());
