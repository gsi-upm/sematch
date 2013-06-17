// The root uri for rest services
var rootURL = "http://localhost:8080/semantic-services/rest/search";

$(document).ready(function() {
	
	
	$('#skill_level').mouseenter(function() {
		$('#skill_level').css("background","#00A0B1");
	});

	$('#skill_level').mouseleave(function() {
		$('#skill_level').css("background","#008299");
	});
	
	$('#city_salary').mouseenter(function() {
		$('#city_salary').css("background","#A700AE");
	});

	$('#city_salary').mouseleave(function() {
		$('#city_salary').css("background","#8C0095");
	});
	
	$('#title').mouseenter(function() {
		$('#title').css("background","#BF1E4B");
	});

	$('#title').mouseleave(function() {
		$('#title').css("background","#AC193D");
	});
	
	$(document).on('mouseenter','.result_box',function(){
		$(this).css("padding","7px");
		$(this).css("border-style","solid");
		$(this).css("border-width","3px");
		$(this).css("border-color","#094AB2");
	});
	
	$(document).on('mouseleave','.result_box',function(){
		$(this).css("border-style","none");
		$(this).css("padding","10px");
	});
	
});

function search() {
	var URI = rootURL;
	
	URI = URI + '/'+'query?city='+$('#city').val()+'&salary='+$('#salary').val();
	//URI = URI + '/'+'query?';
	URI = URI + '&skill=' + $('#skill').val() + '&level=' + $('#level').val();
	
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
	for ( var i = 0; i < candidates.length; i++) {
		rendering(candidates[i]);
	}
}


function rendering(candidate) {

	//declare the attributes.
	var attBox = document.createAttribute("class");
	attBox.value = "result_box";

	//result box
	var box = document.createElement("div");
	box.setAttributeNode(attBox);
	//box.appendChild(renderResultBoxData(candidate.uri));
	box.appendChild(renderResultBoxData(candidate.city));
	box.appendChild(renderResultBoxData(candidate.salary));
	box.appendChild(renderResultBoxData(candidate.skill));
	box.appendChild(renderResultBoxData(candidate.level));
	box.appendChild(renderResultBoxData(candidate.sim));

	var resultDiv = document.getElementById("result_div");
	resultDiv.appendChild(box);
}

function renderResultBoxData(data){
	
	var element = document.createElement("p");
	var aElement = document.createAttribute("class");
	aElement.value = "result_box_data";
	element.setAttributeNode(aElement);
	element.innerHTML = data;
	return element;
	
}