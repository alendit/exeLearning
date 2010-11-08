function rpcCall(name, params, callback){
    // Send an event to python code to be handled by handle + name function
    // Eventnames are capitalized
    var data = {};
    data["name"] = name;
    data["params"] = params;
    $.ajax({url: '/main/handleAjax',
            dataType: 'json',
            data: data,
            success: callback});
}


function test(data){
    alert("Done!\n" + data.result);
}

$(document).ready(function() {
        $("#createNew").click(function() {
            title = prompt("Enter new title");
            rpcCall('CreateNew', {'title' : title}, function(data) {
                $('<p />').
                html($("<a />").
                attr("href", "/package/index/" + data.newId).
                text(title + " - " + data.newId)).
                appendTo($("#packages"));
                }); });
        });
