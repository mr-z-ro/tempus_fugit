<!-- hide script from old browsers
        function user_bookings(){
            console.log("User Booking Clicked!");
            $.ajax({url: "/user_bookings",

                    context: document.body,
                    success: function(data){
                        data = JSON.parse(data);
                        document.cookie = "spreadsheet_id=" + data['spreadsheet_id'];

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

//                    if('oauth_key' in data){
//                        url = data['oauth_key'];
//                        window.location(url);
//                        return;
//                    }

                    window.open(data['spreadsheet_url'], '_blank');
                    window.focus();
            }});
        };


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