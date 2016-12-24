url = "/login"
$("#login").click ->
    
    formData = {}
    if !/@/.test($('#username').val())
        alert("Enter a Valid Email Address")
    else
        formData["user_name"] = $('#username').val().replace(' ', '').toLowerCase().split('@')[0]
        formData["user_password"] = $('#userpassword').val()
        formData["submitType"] = "login"

        console.log(formData)

        $.ajax url,
            type: 'POST'
            data: formData
            success: (data) ->
                next_url = "http://localhost:8080/user/"
                next_url = next_url.concat(formData["user_name"])
                console.log(next_url)
                window.location.replace(next_url)
            error: (data) ->
                alert(data.responseText)

$("#register").click ->
    
    formData = {}
    if !/@/.test($('#username').val())
        alert("Enter a Valid Email Address")
    else
        formData["user_name"] = $('#username').val().replace(' ', '').toLowerCase().split('@')[0]
        formData["user_password"] = $('#userpassword').val()
        formData["submitType"] = "register"

        console.log(formData)

        $.ajax url,
            type: 'POST'
            data: formData
            success: (data) ->
                next_url = "http://localhost:8080/user/"
                next_url = next_url.concat(formData["user_name"])
                window.location.replace(next_url)
            error: (data) ->
                alert(data.responseText)