// The root uri for rest services
var rootURL = "http://lab.gsi.dit.upm.es/webapps/7/semantic-web-services/rest/similarity";

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
	$('#d1').html(data.similarityResult[0].value);
	$('#d2').html(data.similarityResult[1].value);
	$('#d3').html(data.similarityResult[2].value);
	$('#d4').html(data.similarityResult[3].value);
	$('#d5').html(data.similarityResult[4].value);
}

// serialize all the data fields into a JSON string
function toJSON() {
	return JSON.stringify({
		"concept_1": $('#Concept_1').val(), 
		"concept_2": $('#Concept_2').val()
		});
}