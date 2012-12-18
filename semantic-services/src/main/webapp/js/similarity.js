// The root uri for rest services
var rootURL = "http://localhost:8080/semantic-services/rest/similarity";

$('#btnCompute').click(function() {
	computeSimilarity();
	return false;
});

$('#btnReset').click(function() {
	reset();
	return false;
});

function reset() {
	$('#d1').html("0");
	$('#d2').html("0");
	$('#d3').html("0");
	$('#d4').html("0");
	$('#d5').html("0");
}

function computeSimilarity() {
	$.ajax({
		type: 'GET',
		contentType: 'application/json',
		url: rootURL+'/'+$('#Concept_1').val()+'/'+$('#Concept_2').val(),
		success: function(data){
			renderDetails(data);
		},
		error: function(jqXHR, textStatus, errorThrown){
			alert('computing error: ' + textStatus);
		}
	});
}


//display the result.
function renderDetails(data) {
	$('#d1').html(data[0].value);
	$('#d2').html(data[1].value);
	$('#d3').html(data[2].value);
	$('#d4').html(data[3].value);
	$('#d5').html(data[4].value);
}

// serialize all the data fields into a JSON string
function toJSON() {
	return JSON.stringify({
		"concept_1": $('#Concept_1').val(), 
		"concept_2": $('#Concept_2').val()
		});
}