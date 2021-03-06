// Generated by CoffeeScript 1.12.2
(function() {
  var formData, post_list_url, task_list, task_list_empty, task_list_generator, task_name, url, username;

  formData = {};

  url = "/login";

  task_list = $("#taskList");

  username = window.location.pathname.split("/user/")[1];

  post_list_url = "/user/" + username + "/posts";

  task_name = '';

  task_list_generator = function() {
    return $.get(post_list_url, function(data) {
      return $.each(JSON.parse(data), function(key, val) {
        if (val.task_status === "new") {
          return task_list.append('<div class="checkbox"><label><input type="checkbox" value="task-name" onclick="task_complete(event)" id="' + val.task_name + '"> ' + val.task_name + '</label></div>');
        } else {
          return task_list.append('<div class="checkbox"><label><input type="checkbox" value="task-name" checked=true onclick="task_complete(event)" id="' + val.task_name + '"> <mark>' + val.task_name + '</mark> </label></div>');
        }
      });
    });
  };

  task_list_empty = function() {
    return task_list.empty();
  };

  window.task_complete = function(event) {
    formData["task_title"] = event.target.id;
    formData["task_status"] = "completed";
    console.log(formData);
    return $.ajax(post_list_url, {
      type: "POST",
      data: formData,
      success: function(data) {
        task_list_empty();
        return task_list_generator();
      }
    });
  };

  window.onload = task_list_generator();

  $("#task").click(function() {
    formData["task_title"] = $('#newTask').val();
    formData["task_status"] = "new";
    console.log(formData);
    return $.ajax(post_list_url, {
      type: "POST",
      data: formData,
      success: function(data) {
        task_list_empty();
        return task_list_generator();
      }
    });
  });

}).call(this);
