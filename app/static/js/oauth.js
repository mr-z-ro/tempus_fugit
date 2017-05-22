<!-- hide script from old browsers
        function user_bookings(pid, tid){
            console.log("User Booking Clicked!");
            $.ajax({url: "/user_bookings",

                    context: document.body,
                    success: function(data){
                        data = JSON.parse(data);
//                        document.cookie = "spreadsheet_id=" + data['spreadsheet_id'];

                        setCookie("spreadsheet_id", data['spreadsheet_id'], 1);
                        setCookie("project_id", pid + "|" + tid, 1);

                        window.location.replace(data['oauth_url']);
                    }});
        };

        function create_spreadsheet(oauth_key){
            console.log("Creating Spreadsheet");

            $.ajax({url: "/create_spreadsheet?oauth_key=" + oauth_key,
                context: document.body,
                success: function(data){
                    console.log(data);
                    data = JSON.parse(data);

                    if(data['oauth_url'] != null){
                        window.location.replace(data['oauth_url'], '_blank');
                        return;
                    }

                    window.open(data['spreadsheet_url'], '_blank');
                    window.focus();
                    var project_id = getCookie('project_id');
                    if(project_id == null){
                        url = '/index.html';
                    } else {
                        url = '/projects/' + project_id;
                    }
                    window.location.replace(url);
            }});
        };

        function setCookie(cname, cvalue, exdays) {
            var d = new Date();
            d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
            var expires = "expires="+d.toUTCString();
            document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
        }


        function getCookie(cname) {
            var name = cname + "=";
            var decodedCookie = decodeURIComponent(document.cookie);
            var ca = decodedCookie.split(';');
            for(var i = 0; i <ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0) == ' ') {
                    c = c.substring(1);
                }
                if (c.indexOf(name) == 0) {
                    return c.substring(name.length, c.length);
                }
            }
            return "";
        }

// end hiding script form old browsers -->