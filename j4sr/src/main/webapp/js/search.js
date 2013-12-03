// The root uri for rest services
var rootURL = "http://demos.gsi.dit.upm.es/gsimatch/rest/semantic/search";

$(document).ready(function() {
	
	$(document).on('mouseenter','.result_box',function(){
		$(this).css("border-color","#1ba1e2");
	});
	
	$(document).on('mouseleave','.result_box',function(){
		$(this).css("border-color","#dceaf4");
	});
	
	$('#result_div').sortable();
	
});

function search() {
	var URI = rootURL;
	
	URI = URI +'?q={city: "'+$('#city').val()+'", salary:'+$('#salary').val();
	//URI = URI + '/'+'query?';
	URI = URI + ', skill:"' + $('#skill').val() + '", level:"' + $('#level').val()+'"}';
	$.ajax({
		type: 'GET',
		contentType: 'application/json',
		url: URI,
		success: function(candidates){
			
			display(candidates);
		},
		error: function(jqXHR, textStatus, errorThrown){
			alert('computing error: '+URI + textStatus);
		}
	});

}

function display(candidates){
	
	var resultDiv = document.getElementById("result_div");
	resultDiv.innerHTML = '';
	for(var i = 0;i < candidates.length;i=i+3){
		var cans = new Array();
		for(var j=0;j<3;j++){
			cans[j] = candidates[i+j];
		}
		$("#result_div").append(rendering(cans));
	}
	
}


function rendering(candidates) {
	
	var $row = $("<div>",{class:"row-fluid"});
	var $ul = $("<ul>",{class:"thumbnails"});
	for(var i=0;i<candidates.length;i++){
		$ul.append(renderData(candidates[i]));
	}
	$row.append($ul);
	
	return $row;	
}

function renderData(candidate){
	
	var $li=$("<li>",{class:"span4"});
	var $divThumbnail = $("<div>", {class: "thumbnail"});
	var $divResultBox = $("<div>", {class: "result_box"});
	
	var $divRow1 = $("<div>", {class: "row-fluid"});
	var $divRow11 = $("<div>", {class: "span5 offset1"});
	$divRow11.append($("<p class='data'></p>").text("City: "+candidate.city));
	var $divRow12 = $("<div>", {class: "span6"});
	$divRow12.append($("<p class='data'></p>").text("Salary: "+candidate.salary));
	$divRow1.append($divRow11);
	$divRow1.append($divRow12);
	$divResultBox.append($divRow1);
	
	
	var $divRow2 = $("<div>", {class: "row-fluid"});
	var $divRow21 = $("<div>", {class: "span5 offset1"});
	$divRow21.append($("<p class='data'></p>").text("Skill: "+candidate.skill));
	var $divRow22 = $("<div>", {class: "span6"});
	$divRow22.append($("<p class='data'></p>").text("Level: "+candidate.level));
	$divRow2.append($divRow21);
	$divRow2.append($divRow22);
	$divResultBox.append($divRow2);
	
	var $divRow3 = $("<div>", {class: "row-fluid"});
	var $divRow31 = $("<div>", {class: "span11 offset1"});
	$divRow31.append($("<p class='data'></p>").text("Similarity: "+candidate.sim));
	$divRow3.append($divRow31);
	$divResultBox.append($divRow3);
	
	$divThumbnail.append($divResultBox);
	$li.append($divThumbnail);
	
	return $li;
	
}
