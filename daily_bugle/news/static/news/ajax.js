function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

//Page refresh will trigger an Jquery listeners on teh article.html or index.html page.
$( document ).ready(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    }
  });

    //A page refresh will trigger this ajax request and load all the comments on the page.
    $.ajax({
  	  type: 'GET',
  	  url: '/article/'+article_id_value+'/comments',//URL used to send the http request to the view fucntion 'comment'
  	  data : {
  	    'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
  	  },
  	  success: loadAllComments,//Fucntion to load all the comments on the page
  	  dataType: 'json',
  	  error:  printError
  	});

    //A page refresh will trigger this ajax request and load all the Likes and dislikes on the page.
	$.ajax({
		type: 'GET',
		url: '/article/'+article_id_value+'/likes',//A http request is sent to the 'AllLikes' view function
		data : {
			'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
		},
		success: getAllLikesAndDislikes,//This will populate the article.html page with all the likes and dislikes
		dataType: 'json',
		error:  printError
	});

	$('#good').click(function(){//When the like button is selected, and ajax call will be sent to update the database.

		$.ajax({
				url : "/article/"+article_id_value+"/addorDislike/1",
				type : "POST",
				data : {
					'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
					},
				success : getAllLikesAndDislikes,
				error : printError
	           });
	});
$('#bad').click(function(){//When the dislike button is selected, and ajax call will be sent to update the database.

		$.ajax({
				url : "/article/"+article_id_value+"/addorDislike/0",
				type : "POST",
				data : {
					'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
					},
				success : getAllLikesAndDislikes,
				error : printError
	           });

	});
	$('#send').on('submit', function(event){//When the user selects clicks on the 'add comment' button on the article page it will update the databse with the new comments.
        var $FormData = $('#send :input');
        var ValuesOfComment = {};
        $FormData.each(function() {
  	      ValuesOfComment[this.name] = $.trim($(this).val());
  	    });

        if (ValuesOfComment['name'] ==""){//This will promt the user if an empty comment was added.
            event.preventDefault();
            alert("No comment was added")
        }
        else{
    		event.preventDefault();//This disables the browser post request for a form.
    		SendComment(article_id_value);//This function will call an ajax request and update the comments on the databse.
        }
	});
	$(document).on('click',"[name='DeleteButton']",function(){//I am using the JQuery 'on' as the button 'DeleteButton' is added dynmaically inside the fucntion 'LoadPageProducts'

    var pkval=$(this).parent().attr("id");//Every comment is added in a div where the id of that div is the id of the comment.
		$.ajax({
			type: 'DELETE',//Sending a Delete request.
			url: '/article/'+article_id_value+'/comments/'+pkval,//Passing the id of the comment as part of the url will help identify which comment to delete.
			data : {
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: deleteComment,//This function will update the the html page by deleting the comments dynmaically
			dataType: 'json',
			error:  printError
		});
	});
});
//Loading all the comments dynmaically on the article.html page.
function loadAllComments(data, textStatus, jqHXR){
	$.each(data, function(i, comment) {
		var div = $("<div id="+ comment.pk +">")//The id of the comment will be used as the div id attrubute.
		$("#commentsContainer").append(div);
		$("#"+comment.pk).append('<ul class="list-group">');
			var Comment = $("<textarea id='Comment' disabled='true' class='form-control'></textarea>").text(comment.text);
        $("#"+comment.pk).append(Comment);
			var AuthorName = $("<li class='list-group-item' id= 'AuthorName' ></li>").text("Author: " + comment.author);
				$("#"+comment.pk).append(AuthorName);
			var AuthorEmail = $("<li class='list-group-item' id= 'AuthorEmail' ></li>").text("Email : " + comment.email);
				$("#"+comment.pk).append(AuthorEmail);
			var pub_date = $("<li class='list-group-item' id='pub_date' ></li>").text("Publication date : " + comment.pub_date);
				$("#"+comment.pk).append(pub_date);
	    var DeleteButton= '<button type="submit" class="btn btn-warning deleteComment" name="DeleteButton">Delete</button>';
	      $("#"+comment.pk).append(DeleteButton);
		$("#"+comment.pk).append('</ul>');
		})
  }
//This function will be called from a succesful ajax request, it will send the comment to the view function that will update the comment on the database
function SendComment(article_id_value) {
	  var $FormData = $('#send :input');//using Jquery to retieve all the form data values
	  var ListOfFormData = {};
	  $FormData.each(function() {
	      ListOfFormData[this.name] = $(this).val();
          if(this.name=='name')//This is the name value of the input field of the comment.
          {
              $('#Name').val("")//This will remove the comment after the clicking on 'addComment'
          }
	  });
      NewComment=ListOfFormData['name']//NewComment will have the new comment
	    $.ajax({
	        url : "/article/"+article_id_value+"/comments",
	        type : "POST",
	        data : {
						'text':NewComment,//Passing the new comment as part of the POST request
						'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
					},
	        success : AddComment,//This function will update the html page dynmaically
	        error : printError
	  });
	};
function printError( req, status, err ) {//Error is printed showing any details about the cause of the issue.
   console.log('An issue has occured See error --->', status, err)
  }
function AddComment(data, textStatus, jqHXR){//Adding a comment will empty the 'commentscontainer' on the article.html and will then call the fucntion loadAllComments to load all the comments.
	$("#commentsContainer").empty();
  console.log(data);
  $.each(data, function(i, comment) {
		var div = $("<div id="+ comment.pk +">")//The id of the comment will be used as the div id attrubute.
		$("#commentsContainer").append(div);
		$("#"+comment.pk).append('<ul class="list-group">');
			var Comment = $("<textarea id='Comment' disabled='true' class='form-control'></textarea>").text(comment.text);
        $("#"+comment.pk).append(Comment);
			var AuthorName = $("<li class='list-group-item' id= 'AuthorName' ></li>").text("Author: " + comment.author);
				$("#"+comment.pk).append(AuthorName);
			var AuthorEmail = $("<li class='list-group-item' id= 'AuthorEmail' ></li>").text("Email : " + comment.email);
				$("#"+comment.pk).append(AuthorEmail);
			var pub_date = $("<li class='list-group-item' id='pub_date' ></li>").text("Publication date : " + comment.pub_date);
				$("#"+comment.pk).append(pub_date);
	    var DeleteButton= '<button type="submit" class="btn btn-warning deleteComment" name="DeleteButton">Delete</button>';
	      $("#"+comment.pk).append(DeleteButton);
		$("#"+comment.pk).append('</ul>');
  });
}
function deleteComment(data, textStatus, jqHXR){//This function will dynmaically delete the comment on the article page.
		$('#'+data['id']).remove();
	}
	//Fucntion is called when the user; clicks the like/dislike button also when a page refresh occurs.
function getAllLikesAndDislikes(data, textStatus, jqHXR){//This fucntion will populate the likes count and dislikes count on the article.html page.
	if (data['updated']){
		$("#good").html('<span class="glyphicon glyphicon-thumbs-up"></span> '+data['totalLikes']);
		$("#bad").html('<span class="glyphicon glyphicon-thumbs-down"></span> '+data['totalDisLikes']);
	}
	else if(!data['updated']){
		$("#good").html('<span class="glyphicon glyphicon-thumbs-up"></span> '+data['totalLikes']);
		$("#bad").html('<span class="glyphicon glyphicon-thumbs-down"></span> '+data['totalDisLikes']);
	}
}
