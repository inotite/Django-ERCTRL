    var phUsername;
    var phIpAddress;
    var testing = false;
    var $syncForm = $('.phue-connection-form');
        availableGroups = '#id-available-groups option:selected',
        availableScenes = '#id-available-scenes option:selected',
        $addScene = $('#id_addScene'),
        $saveBridgeData = $('#id_save_scene_and_group'),
        room_id = $saveBridgeData.attr('data-room-id');
        var csrftoken = getCookie('csrftoken');

    $(".connection_msg").hide();
    $syncForm.on('submit', function () {

        if (testing) {
            bypassTesting();
        } else {
            var ip = $('#id_ipAddress').val();
            if (ip) {
                $.ajax({
                    method: "POST",
                    url: "http://" + ip + "/api",
                    dataType: 'json',
                    data: JSON.stringify({"devicetype": "escap#newdeveloper"})
                }).done(function (msg) {
                    $(".connection_msg").show();
                    if (msg[0].error) {
                        populateGroupsAndScenes();
                        $(".connection_msg").removeClass("alert-success");
                        $(".connection_msg").addClass("alert-danger");
                        $("#id_connection_msg").text('ERROR! - ' + msg[0].error.description);
                        // alert('ERROR! - ' + msg[0].error.description);
                    }
                    if (msg[0].success) {
                        $(".connection_msg").removeClass("alert-danger");
                        $(".connection_msg").addClass("alert-success");
                        $("#id_connection_msg").text('Successfully synced with bridge.');
                        phIpAddress = ip;
                        phUsername = msg[0].success.username;
                        saveBridgeData();
                        populateGroupsAndScenes();
                    }
                }).fail(function () {
                    $(".connection_msg").show();
                    $(".connection_msg").removeClass("alert-success");
                    $(".connection_msg").addClass("alert-danger");
                    $("#id_connection_msg").text('ERROR! - Check IP of your bridge and try one more time.');
                    // alert('ERROR! - Check IP of your bridge and try one more time.');
                });
            }
        }
        return false;
    });

    $addScene.on('click', function() {
        $('#orderedSceneContainer').append(
            "<div class='scene list-group-item' data-group='" + $(availableGroups).val() +
            "' data-scene='" + $(availableScenes).val() + "'><span>" + $(availableGroups).text() + " - " +
            $(availableScenes).text() + "</span><button class='btn btn-danger deleteBtn'>Delete</button></div>");
    });

    $('body').on('click', '.deleteBtn', deleteMe);

    $saveBridgeData.on('click', saveBridgeData);

    function loadPage(newPage) {
        // Take all of the form and page params, shove it into query parms, and reload
        room_id = $('#id-room-list').val();
        $saveBridgeData.attr("data-room-id", room_id);
    }

    // Change room event
    $("#id-room-list").change(function (event) {
        event.preventDefault();
        loadPage();
    });
    loadPage();

    function populateGroupsAndScenes(callback) {
        $.when(
            getGroups(),
            getScenes()
        ).then( function() {
            $('.ph-groups-content').show();
            callback ? callback() : null;
        });
    }

    function getScenes() {
        return $.ajax({
            method: "GET",
            url: "http://" + phIpAddress + "/api/" + phUsername + "/scenes",
            data: {}
        }).done(function (msg) {
            $.each(msg, function (index, value) {
                $('#id-available-scenes').append($('<option/>', {
                    value: index,
                    text: value.name
                }));
            });
        });
    }

    function getGroups() {
        return $.ajax({
            method: "GET",
            url: "http://" + phIpAddress + "/api/" + phUsername + "/groups",
            data: {}
        }).done(function (msg) {
            $('#id-available-groups').empty(); //clear list
            $.each(msg, function (index, value) {
                $('#id-available-groups').append($('<option/>', {
                    value: index,
                    text: value.name
                }));
            });
        });
    }

    function recallScene(group, scen) {
        $.ajax({
            method: "PUT",
            url: "http://" + phIpAddress + "/api/" + phUsername + "/groups/" + group + "/action",
            dataType: 'json',
            data: JSON.stringify({"scene": scen})
        }).done(function (msg) {
            $(".connection_msg").show();
            $(".connection_msg").removeClass("alert-danger");
            $(".connection_msg").addClass("alert-success");
            $("#id_connection_msg").text('Checked Lighting Scene on Group successfully');
        });
    }

    function serializeSceneList() {
        var builder = [];
        $.each($('div.scene'), function (index, value) {
            builder[index] = {
                "order": index,
                "groupId": value.attributes["data-group"].value,
                "sceneId": value.attributes["data-scene"].value
            }
        });
        return builder;
    }

    $('#testConfig').on('click', function(e) {
        // e.stopPropagation();
        // alert("child");
        recallScene($(availableGroups).val(), $(availableScenes).val());
    });


    function bypassTesting() {
        // phIpAddress = "192.168.1.106";
        phIpAddress = "127.0.0.1:8081";
        phUsername = "TMUwQoaKk8w2yOGpQB7J-eH43Te1lfSjc2-bMWvr";
        $addScene.prop('disabled', false);
        populateGroupsAndScenes();
    }

    function triggerPhilipsHue(event) {
        recallScene($(event).parent()[0].attributes["data-group"].value, $(event).parent()[0].attributes["data-scene"].value);
    }

    function deleteMe() {
        $(this).parents('.scene').remove();
    }

    function getBridgeData() {

        var callback = function (rtnData) {
            return function() {
                $.each(rtnData.settings_data, function (index, value) {
                    $('#orderedSceneContainer').append(
                        "<div class='scene list-group-item' data-group='" +
                        value.groupId + "' data-scene='" + value.sceneId + "'><span>" +
                        $('#id-available-groups option[value="' + value.groupId + '"]').text() + " - " +
                        $('#id-available-scenes option[value="' + value.sceneId + '"]').text() +
                        "</span><button class='btn btn-danger deleteBtn'>Delete</button></div>");
                });
                $addScene.prop('disabled', false);
            }
        };

        $.ajax({
            method: "GET",
            url: "/dashboard/rooms/"+room_id+"/ph-settings/",
            data: {}
        }).done(function (rtnData) {
            if (rtnData.username != "" && rtnData.username != null && rtnData.username != undefined && rtnData.is_connected > 0) {
                phUsername = rtnData.username;
                phIpAddress = rtnData.bridge_url;
                $('#id_ipAddress').val(phIpAddress);
                populateGroupsAndScenes(callback(rtnData));
            }
        });
    }

    getBridgeData();

    function saveBridgeData() {
        $.ajax({
            method: "POST",
            url: "/dashboard/rooms/"+room_id+"/ph-settings/",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            dataType: 'json',
            data: JSON.stringify({"bridge_url": phIpAddress, "username": phUsername, "settings_data": serializeSceneList()})
        }).done(function (msg) {
            //enable add scene button
            $(".connection_msg").show();
            $(".connection_msg").removeClass("alert-danger");
            $(".connection_msg").addClass("alert-success");
            $("#id_connection_msg").text('Changes was successfully saved');
            $addScene.prop('disabled', false);
        });
    }