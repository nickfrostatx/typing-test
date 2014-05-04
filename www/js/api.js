(function() {

    api.baseUrl = 'http://127.0.0.1:8080';

    // {"success": true}
    api.createUser = api.view('/users/', 'POST');

    // {"key": <string>}
    // {"error": 404, "msg": "Invalid email and/or password."}
    api.newSession = api.view('/sessions/', 'POST');
    
    // {"answer": <int>}
    api.getStory = api.view('/stories/', 'POST', true);


    function storeKeyCookie(key) {
        // Set expiration time to 30 days
        var expiration = new Date();
        expiration.setTime(expiration.getTime() + (30 * 24 * 60 * 60 * 1000));

        document.cookie = 'key=' + escape(key) + '; expires=' + expiration.toGMTString() + '; path=/';
    }

    function readKeyCookie() {
        // Loop through each cookie
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];

            // Strip preceding whitespace
            while (c.charAt(0) === ' ')
                c = c.substring(1, c.length);

            if (c.indexOf('key=') === 0)
                return unescape(c.substring(4, c.length));
        }

        return false;
    }

    api.authenticate = function(data, callback, error) {
        api.newSession(data, function(data) {
            api.key = data.key;
            api.authenticated = true;
            storeKeyCookie(data.key);
            callback();
        }, error);
    };

    // Autodetect key from cookies
    var key = readKeyCookie();
    if (key) {
        api.key = key;
        api.authenticated = true;
        storeKeyCookie(key);
    }

})();
