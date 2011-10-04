/*****

PureeData.net
Ted Hayes 2010/2011


******/

var DEBUGMODE = false;

var host = "http://pureedata.net/";
var isConnecting = false;
var connectFirstObject;
var connectSecondObject;

var objects;
var connections;

function trace(what) {
	if(DEBUGMODE){
		$('#traceBox').append(what+"<br />");
	}
}

function Point(x,y){
	this.x = x;
	this.y = y;
}

function objSubmit(){
    addObj($('#addObjField').val());
}

function msgSubmit(){
    addMsg($('#addMsgField').val());
}

function errorAnimation(what){
	what.effect("highlight", {color:'#9E1616'}, 2000);
}

function addObj(what) {
	//trace("addObj: "+what);
	var objStem = what.split(' ')[0];
	if(objStem in objectDictionary){
	    $.ajax({
	        type: "POST",
	        url: host+"pd",
	        data: {
	        	cmd: 'obj',
				obj: what,
				x: '50',
				y: '50'
			},
	        success: function (result) {
	          trace("addObj success: "+result);
	          makeNewObject(jQuery.parseJSON(result)[0]);
	        },
	        error: function (result) {
	          trace("addObj error: "+result);
	          errorAnimation($('#addObjField'));
	        }
	    });
	} else {
		// TODO: show error message
		errorAnimation($('#addObjField'));
		$('#addObjField').val('Add Object');
	}
}

function addMsg(what) {
	$.ajax({
		type : "POST",
		url : host + "pd",
		data : {
			cmd : 'msg',
			msg : what,
			x : 50,
			y : 50
		},
		success : function(result) {
			makeNewObject(jQuery.parseJSON(result)[0]);
		},
		error : function(result) {
			trace("addMsg error: " + result);
		}
	});
	$('#addObjField').val('Add Message');
}

function clearPatch() {
	trace("clearPatch()");
    $.ajax({
        type: "POST",
        url: host+"pd",
        data: {
        	cmd: 'clear'
        },
        success: function (result) {
          trace("clear success: "+result);
          //getCurrentObjectList();
          objects = [];
          $(".pdObject").remove();
        },
        error: function (result) {
          trace("clear error: "+result);
        }
    });
}

function getCurrentObjectList(){
	objects = [];
    $.ajax({
        type: "GET",
        url: host+"list",
        success: function (result) {
          var stuff = jQuery.parseJSON(result);
          objects = stuff.objects;
          connections = stuff.connections;
          //traceList();
          updateGUI();
        },
        error: function (result) {
          trace(result.responseText.substr(4));
        }
    });
}

var obj_gui_html = "<div class='draggable pdObject ui-corner-all'></div>";
var msg_gui_html = "<div class='draggable pdObject pdMessage'></div>";
var obj_inlet_html = "<div class='iolet inlet'></div>";
var obj_outlet_html = "<div class='iolet outlet filled'></div>";
var obj_del_html = "<div class='objDelete'>X</div>"

function makeNewObject(obj){	
	var which_html;
	var numInlets, numOutlets;
	
	if(obj.type == 'obj'){
		which_html = obj_gui_html;
		var objStem = obj.content.split(' ')[0];
		numInlets = objectDictionary[objStem].inlets;
		numOutlets = objectDictionary[objStem].outlets;
	} else {
		which_html = msg_gui_html;
		numInlets = 1;
		numOutlets = 1;
	}
	var special = false;
	if(obj.content == "send~ left" || obj.content == "send~ right"){
		// special!
		special = true;
	}
	
	// var deleteButton = $(obj_del_html)
		// .click(deleteClick);	
	
    theObj = $(which_html)
        .attr('id', obj.id)
        .html(obj.content)
        .css({'left':obj.x+'px', 'top':obj.y+'px'})
        //.append(deleteButton)
        .hover(objectOver, objectOut);
    
    if(!special){
    	// Disabled until backend deleting works
    	//theObj.append(deleteButton);
    } else {
    	// apply special class
    	theObj.addClass('specialObject');
    }
    
    var i = 0;
    var l = 0;
    for (i=0; i<numInlets; i++){
    	l = (16 * i) + 6;
    	theInlet = $(obj_inlet_html)
			.css({'left':l+'px'})
			.attr('id', i)
			.attr('objectid', obj.id)
			.click(endConnect);
		theObj.append(theInlet);
    }
    
    for (i=0; i<numOutlets; i++){
    	l = (16 * i) + 6;
    	theOutlet = $(obj_outlet_html)
			.css({'left':l+'px'})
			.attr('id', 0)
			.attr('objectid', obj.id)
			.click(startConnect);
		theObj.append(theOutlet);
    }
    
    if(obj.type == 'msg'){
    	theObj.click(messageClick);
    }
   
    $("body").append(theObj);
    makeDraggable();
}

function messageClick(e){
	var id = $(this).attr('id');
	$.post(host+'pd', {cmd:'msgclick',id:id}, function(result){
		trace("messageClick result: "+result);
	});
}

function objectOver(e){
	//trace("objectOver: "+$(this).children('.objDelete'));
	$(this).children('.objDelete').show();
}

function objectOut(e){
	$(this).children('.objDelete').hide();
}

function deleteClick(e){
	var id = $(this).parent('.pdObject').attr('id');
	//deleteObject(id);
}

function disconnect(id){
	$.post(host+'pd', {cmd:'disconnect',id:id}, function(r){
		// disconnect success
		trace('disconnect success: r:'+r);
		info = $.parseJSON(r);
		connections.pop(info.id);
		$('.line[id='+info.id+']').remove();
	}, function(r){
		// error
	});
}

function startConnect(e){
	isConnecting = true;
	connectFirstObjectID = $(this).attr('objectid');
	connectFirstOutletNum = $(this).attr('id');
	connectFirstObject = $(this);
	$('.inlet').css({'cursor':'pointer'});
	e.stopPropagation();	// stop message objects from triggering "click" event
}

function endConnect(e){
	//trace("endConnect");
	if(isConnecting){
		isConnecting = false;
		$('.inlet').css({'cursor':'default'});
		connectSecondObject = $(this);
		// post connect command
	    $.ajax({
	        type: "POST",
	        url: host+"pd",
	        data: {
				cmd: 'connect',
				firstID: connectFirstObject.attr('objectid'),
				outlet: connectFirstObject.attr('id'),
				secondID: $(this).attr('objectid'),
				inlet: $(this).attr('id')
			},
	        success: function (result) {
	          trace("result: "+result);
	          var o1 = connectFirstObject.parent();
	          var o2 = connectSecondObject.parent();
	          var c = jQuery.parseJSON(result);
	          trace("connect success: "+c);
	          connections.push(c);
	          var id = parseInt(c.id);
	          
	          drawConnection(id, o1, connectFirstObject.attr('id'), o2, connectSecondObject.attr('id'));
	        },
	        error: function (result) {
	          trace("connect error: "+result);
	        }
	    });
	}
	e.stopPropagation();	// stop message objects from triggering "click" event
}

function drawConnection(id, o1, outlet, o2, inlet){
	// draw line
	var out = o1.children('.outlet#'+outlet);
	var firstPoint = new Point(out.offset().left, out.offset().top);
	var inl = o2.children('.inlet#'+inlet);
	var secondPoint = new Point(inl.offset().left, inl.offset().top);
	
	//var update = false;
	
	// if($('.line#'+id).length > 0){
		// // this line already exists, update it
		// update = true;
	// }
	
	var l = drawLine(firstPoint, secondPoint, id);
	// if(!update)
	l.attr('id', id);
}

function quitPd(){
	$.post(host+'pd', {cmd:'quit'});
}

function drawLine(pt1, pt2, id){
	var dx = pt2.x - pt1.x;
	var dy = pt2.y - pt1.y; 
	var h = Math.sqrt(Math.pow(dx,2) + Math.pow(dy,2));
	var thetaRad = Math.atan2(dy, dx);
	var thetaDeg = thetaRad * 180 / Math.PI;
	//trace("("+pt1.x+","+pt1.y+"), ("+pt2.x+","+pt2.y+") h: "+h+" / theta: "+thetaDeg);
	var l = lesser(pt1.x, pt2.x) + 6;	// centered on iolet
	var t = lesser(pt1.y, pt2.y);
	//trace("t: "+t+" / l: "+l);
	var theLine;
	var update = false;
	//trace('id: '+id+' len: '+$('.line#'+id).length);
	if($('.line[id='+id+']').length > 0){
		// this line already exists, update it
		update = true;
		theLine = $('.line[id='+id+']');
	} else {
		theLine = $("<hr class='line' />");
	}
	//theLine = $("<hr class='line' />")
	theLine.easyRotate({
     		degrees: thetaDeg
		})
		.css({
			// not sure why, but these also have to be set to make offset() work
			'left':l+'px',
			'top':t+'px',
			'width':h+'px'
		});
	if(!update)
		$("body").append(theLine);
	theLine.offset({
			top:t,
			left:l
		})
		.click(lineClick);
	return theLine;
}

function lineClick(){
	//trace("line clicked");
	if($('#disconnectCB').is(':checked')){
		disconnect($(this).attr('id'));
	}
}

function updateGUI(){
	//clearPatch();
    if(!objects || objects.length < 1)
        return;
    for(var i=0; i < objects.length; i++){
    	//trace()
        if($('#'+i).attr('id')) {
        	//trace("updateGUI old object: "+i);
        } else {
        	//trace("updateGUI new object: "+i);
        	makeNewObject(objects[i]);
        }
    }
    makeDraggable();
    drawAllConnections();
}

function drawAllConnections(){
	for(ci in connections){
		// javascript uses values for for..in instead of keys. Thanks, assholes.
		//console.log(connections);
		var c = connections[ci];
		//trace('c: '+c);
		//console.log(c);
		var o1 = $('#'+c.firstID);
		var o2 = $('#'+c.secondID);
		//trace("drawAllConnections: firstID: "+c.firstID+" / second: "+c.secondID+" / "+o1+" / "+o2);
		drawConnection(c.id, o1, c.outlet, o2, c.inlet);
	}
}

function traceList(){
    if(!objects || objects.length < 1)
        return;
    for(var i=0; i < objects.length; i++){
        trace("object "+objects[i].id+": "+objects[i].type+"> "+objects[i].content+" / x: "+objects[i].x+" / y: "+objects[i].y);
    }
}

function makeDraggable(){
    $(".draggable").draggable({
    	start: objectStartDrag,
    	drag:  objectDrag,
    	stop:  objectStopDrag
    });
}

function objectStartDrag(e, ui){
	//e.stopPropagation();	// stop message objects from triggering "click" event
	//return false;
}

function objectDrag(e, ui){
	// called as object is dragged; update all lines connected to this object
	// ui contains:
		// Object
		// helper: c.fn.c.init[1]
			// 0: HTMLDivElement
		// context: HTMLDivElement
		// length: 1
		// offset: Object
			// left: 349
			// top: 179
		
			// left: 353
			// top: 183
		// position: Object
			// left: 349
			// top: 179

	var id = $(e.target).attr('id');
	// get connections to this object
	for (ci in connections){
		var c = connections[ci];
		if(c.firstID == id || c.secondID == id){
			// redraw all connections attached to this object
			drawConnection(c.id, $('#'+c.firstID), c.outlet, $('#'+c.secondID), c.inlet);
		}
	}
}

function objectStopDrag(e){
	var id = $(this).attr('id');
	var x = $(this).offset().left;
	var y = $(this).offset().top;
	trace("stopDrag: "+x+" / "+y);
	$.post(host+'pd', {
		cmd:'move',
		id:id,
		x:x,
		y:y
	});
	//e.stopPropagation();	// stop message objects from triggering "click" event
	return false;
}

function deleteObject(id){
	$('#'+id).remove();
	$.post(host+'pd', {cmd:'delObject', id:id});
}

function setDSP(to){
	$.ajax({
        type: "POST",
        url: host+"pd",
        data: {
        	cmd: 'dsp',
        	dsp: to
        },
        success: function (result) {
          //trace("setDSP success: "+result);
        },
        error: function (result) {
          //trace("setDSP error: "+result);
        }
    });
}

function dspClick(){
	var val;
	if($(this).is(':checked')){
		// turn on dsp
		setDSP(1);
	} else {
		// turn off dsp
		setDSP(0);
	}
}

function lesser(a, b){
	if(a<b)
		return a;
	else
		return b;
}

function submitEnter(field, e) {
	var keycode, val;
	if(window.event)
		keycode = window.event.keyCode;
	else if(e)
		keycode = e.which;
	else
		return true;
	val = field.value;

	if(keycode == 13) {
		if(field.name == "obj") {
			addObj(val);
		} else if(field.name == "msg") {
			addMsg(val);
		}
	} else {
		return true;
	}
}

function tagFieldChange(val){
	if(val.length > 0 && val != "Click here to add tags"){
		
	} else {

	}
}

function disconnectClick(e){
	if($('#disconnectCB').is(':checked')){
		$('.line').css({
			'cursor':'pointer'
		});
	} else {
		$('.line').css({
			'cursor':'default'
		});
	}
}

$(function() {
	//// MAIN ////
    //$("#dspCheckbox").button().click(dspClick);
    $('#infoBox').dialog({
    	modal	: true,
    	title	: 'About PuréeData',
    	width	: 600
    });
    $('#creditsBox').dialog({
    	autoOpen: false,
    	modal	: true,
    	title	: 'Credits',
    	width	: 600
    });
    $('#helpBox').dialog({
    	autoOpen: false,
    	//modal	: true,
    	title	: 'Help!',
    	width	: 600
    });
    $('#creditsButton').button().click(function(){
    	$('#creditsBox').dialog('open');
    });
    $('#helpButton').button().click(function(){
    	$('#helpBox').dialog('open');
    });
    $('#infoButton').button().click(function(){
    	$('#infoBox').dialog('open');
    });
    $('#listenButton').button().click(function(){
    	//window.open('http://pureedata.net:8000/pureedata.mp3', '_blank');
    	window.open('http://pureedata.net/static/pureedata.pls', '_blank');
    });
    $("#disconnectCB").button().click(disconnectClick);
	//clearPatch();
	getCurrentObjectList();
	//updateGUI();
	//drawLine(new Point(50, 50),new Point(70, 60));
});