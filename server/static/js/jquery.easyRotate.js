/*
 *	jquery.easyRotate 1.0 - 3-11-2010
 * author: Jordan Andree (jordan@noblegiant.com)
 * http://noblegiant.com
 *
 *	Written to ease the implementation of element rotation for cross-browser support
 *	Feel free to do whatever you want with this file
 *
 */
(function ($) {
	
	// base function
	$.fn.extend({
		easyRotate: function(options) {
		
			// default config 
			var defaults = {
				degrees: 0  
			};
			
			// extend the options
			var options = $.extend(defaults, options);
			
			// return function
			return this.each(function() {
					
				// the object 
				var obj = this;
				
				// the degrees param
				var deg = options.degrees;
								
				// calculations to get our matrix
				var deg2radians = Math.PI * 2 / 360;
				var rad = deg * deg2radians;
				var costheta = Math.cos(rad);
				var sintheta = Math.sin(rad);
			 
				// vars for cosin and sin
				var a = parseFloat(costheta).toFixed(8);
				var c = parseFloat(-sintheta).toFixed(8);
				var b = parseFloat(sintheta).toFixed(8);
				var d = parseFloat(costheta).toFixed(8);
				
				// the matrix string
				var matrix = "matrix(" + a + ", " + b + ", " + c + ", " + d + ", 0, 0);";
				
				// if IE filters are present
				if (obj.filters) {

					obj.style.filter = "progid:DXImageTransform.Microsoft.Matrix(sizingMethod='auto expand');";
					obj.filters.item(0).M11 = costheta;
					obj.filters.item(0).M12 = -sintheta;
					obj.filters.item(0).M21 = sintheta;
					obj.filters.item(0).M22 = costheta;
					
				// else for Safari, Firefox, etc
				} else {
					obj.setAttribute("style",   "position:absolute; -moz-transform:  " + matrix + 
														"; -webkit-transform:  " + matrix + 
														"; -o-transform: " + matrix + "");

														
				}
				

				
			
			});	
		}
	});
})(jQuery);


