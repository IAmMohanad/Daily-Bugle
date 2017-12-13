$( document ).ready(function() {
	$.ajax({
	  type: 'GET',
	  url: '/article/1/comments',
	  data : {
	    'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
	  },
	  success: loadAllComments,
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
					'author_id': 1,
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
					'author_id': 1,
					'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
					},
				success : GetAllLikes,
				error : printError
	});

	});
	$('#send').on('submit', function(event){
		event.preventDefault();
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

function loadAllComments(data, textStatus, jqHXR){
	$.each(data, function(i, comment) {
		var div = $("<div id="+ comment.pk +">")
		$("#commentsContainer").append(div);
		$("#"+comment.pk).append('<ul class="list-group">');
			var Comment = $("<textarea id='Comment' disabled='true' class='form-control'></textarea>").text(comment.text);
        $("#"+comment.pk).append(Comment);
			var AuthorName = $("<li class='list-group-item' id= 'AuthorName' ></li>").text("Author: " + comment.author);
				$("#"+comment.pk).append(AuthorName);
			var AuthorEmail = $("<li class='list-group-item' id= 'AuthorEmail' ></li>").text("email : " + comment.email);
				$("#"+comment.pk).append(AuthorEmail);
			var pub_date = $("<li class='list-group-item' id='pub_date' ></li>").text("Publication_date : " + comment.pub_date);
				$("#"+comment.pk).append(pub_date);
	    var DeleteButton= '<button type="submit" class="btn btn-warning deleteComment" name="DeleteButton">Delete</button>';
	      $("#"+comment.pk).append(DeleteButton);
		$("#"+comment.pk).append('</ul>');
		})
  }

function SendComment() {
	  var $FormData = $('#send :input');
	  var ListOfFormData = {};

	  $FormData.each(function() {
	      ListOfFormData[this.name] = $(this).val();
		  console.log("List of type: "+this.name +" inside values " +ListOfFormData[this.name]);
	  });
	    $.ajax({
	        url : "/article/1/comments",
	        type : "POST",
	        data : {
						'text':ListOfFormData['name'],
						'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
					},
	        success : AddComment,
	        error : printError
	  });
	};
function printError( req, status, err ) {
   console.log('An issue has occured See error --->', status, err)
  }
function AddComment(data, textStatus, jqHXR){
		NewCommentAdded= data['text'];
		pk=data['id'];
		var div = $("<div id="+pk +">")
		$("body").append(div);
		var text = $("<li id= 'name' ></li>").text("name: "+ NewCommentAdded.toString());
		$("#"+pk).append(text);
		var DeleteButton=    "<input type= submit value= Delete name=DeleteButton>";
		$("#"+pk).append(DeleteButton);
	}



function deleteComment(data, textStatus, jqHXR){
		var myNode = document.getElementById(data['id']);
		$('#'+data['id']).remove();
	}
function GetAllLikes(data, textStatus, jqHXR){
	$(".Like").find('#likes').text("Total Likes:"+ data['totalLikes']);
	$(".Like").find('#dislikes').text("Total DisLikes:"+ data['totalDisLikes']);
}
