$( document ).ready(function() {
	$.ajax({
	  type: 'GET',
	  url: '/article/1/comments',
	  data : {
	    'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
	  },
	  success: LoadPageComments,
	  dataType: 'json',
	  error:  printError
	});
	$.ajax({
		type: 'GET',
		url: '/article/1/likes',
		data : {
			'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
		},
		success: GetAllLikes,
		dataType: 'json',
		error:  printError
	});

	$('#good').click(function(){

		$.ajax({
				url : "/article/1/addorDislike/1",
				type : "POST",
				data : {
					'author_id': 15,
					'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
					},
				success : GetAllLikes,
				error : printError
	});

	});
$('#bad').click(function(){

		$.ajax({
				url : "/article/1/addorDislike/0",
				type : "POST",
				data : {
					'author_id': 15,
					'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
					},
				success : GetAllLikes,
				error : printError
	});

	});
	$('#send').on('submit', function(event){
		event.preventDefault();
		console.log("sedfsdf");
		SendComment();

	});
	$(document).on('click',"[name='DeleteButton']",function(){//I am using the JQuery 'on' as the button 'DeleteButton' is added dynmaically inside the fucntion 'LoadPageProducts'
		var pkval=$(this).parent().attr("id");
		console.log("this is the id of the comment " +pkval)
		$.ajax({
			type: 'DELETE',
			url: '/article/1/comments/'+pkval,
			data : {
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: deleteComment,
			dataType: 'json',
			error:  printError
		});
	});

});

function LoadPageComments(data, textStatus, jqHXR){
	console.log(JSON.stringify(data));

	$.each(data, function(i, comment) {
		console.log(comment.text)
		console.log("id = "+ comment.pk);

		var div = $("<div id="+ comment.pk +">")

		$("body").append(div);
        var Name = $("<li id= 'name' ></li>").text("Comment: " + comment.text);
        $("#"+comment.pk).append(Name);
        var DeleteButton= "<input type= submit value= Delete name=DeleteButton>";
        $("#"+comment.pk).append(DeleteButton);
	})

    // for( i =1; i<Object.keys(data).length; i++)
    // {
    //   console.log(data[i].text);
	//
    //   NameOfItem= data[i]['fields']['text'];
	// 		pk=data[i]['pk'];
    //   console.log("id = "+ pk);
    //   var div = $("<div id="+pk +">")
    //   $("comment").append(div);
    //   var Name = $("<li id= 'name' ></li>").text("Comment: "+ NameOfItem.toString());
    //   $("#"+pk).append(Name);
    //   var DeleteButton= "<input type= submit value= Delete name=DeleteButton>";
    //   $("#"+pk).append(DeleteButton);
    // }
  }
function SendComment() {
		console.log("inside comments");
		var $FormData = $('#send :input');
		console.log("inside comments");

	  var ListOfFormData = {};
		console.log("inside comments");

	  $FormData.each(function() {
	      ListOfFormData[this.name] = $(this).val();
				console.log("inside comments values " +ListOfFormData[this.name]);

	  });
	    $.ajax({
	        url : "/article/1/comments",
	        type : "POST",
	        data : {
						'text':ListOfFormData['name'],
						'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
					},
	        success : addItem,
	        error : printError
	  });
	};
function printError( req, status, err ) {
   console.log('An issue has occured See error --->', status, err)
  }
function addItem(data, textStatus, jqHXR){
		NameOfItem= data['text'];
		pk=data['id'];
		var div = $("<div id="+pk +">")
		$("body").append(div);
		var text = $("<li id= 'name' ></li>").text("name: "+ NameOfItem.toString());
		$("#"+pk).append("<br>")
		$("#"+pk).append(text);
		var DeleteButton=    "<input type= submit value= Delete name=DeleteButton>";
		$("#"+pk).append(DeleteButton);

	}
function deleteComment(data, textStatus, jqHXR){
		var myNode = document.getElementById(data['id']);
		$('#'+data['id']).remove();
	}
function GetAllLikes(data, textStatus, jqHXR){
	console.log("likes" + data['totalLikes'])
	console.log("likes" + data['totalDisLikes'])
	$(".Like").find('#likes').text("Total Likes:"+ data['totalLikes']);
	$(".Like").find('#dislikes').text("Total DisLikes:"+ data['totalDisLikes']);

}
