formData = {}
url = "/login"
task_list = $("#taskList")
username = window.location.pathname.split("/user/")[1]
post_list_url = "/user/" + username + "/posts"
task_name=''

task_list_generator = ->  
    $.get(post_list_url, (data) ->
      $.each(JSON.parse(data), (key, val) ->
         if (val.task_status == "new")
            task_list.append('<div class="checkbox"><label><input type="checkbox" value="task-name" onclick="task_complete(event)" id="' + val.task_name + '"> ' + val.task_name + '</label></div>') 
         else 
            task_list.append('<div class="checkbox"><label><input type="checkbox" value="task-name" checked=true onclick="task_complete(event)" id="' + val.task_name + '"> <mark>' + val.task_name + '</mark> </label></div>')  
      )
)
task_list_empty = ->   
     task_list.empty()

window.task_complete = (event) ->
    formData["task_title"] = event.target.id
    formData["task_status"] = "completed"
    
    console.log(formData)

    $.ajax post_list_url,
           type: "POST",
           data: formData, 
           success: (data) ->
            task_list_empty()
            task_list_generator()

window.onload = task_list_generator()


$("#task").click(() ->
    
    formData["task_title"] = $('#newTask').val()
    formData["task_status"] = "new"
    
    console.log(formData)

    $.ajax  post_list_url,
            type: "POST",
            data: formData, 
            success: (data) ->
             task_list_empty()
             task_list_generator()
)