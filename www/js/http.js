(function() {
    function Api() {
        this.baseUrl = '';
        this.key = '';
        this.authenticated = false;
    }

    Api.prototype.call = function(url, method, data) {
        return $.ajax({
            url: this.baseUrl + url,
            method: method,
            data: data,
            dataType: 'JSON',
        });
    };

    Api.prototype.requestFailed = function(jqXHR, textStatus, errorThrown) {
        console.log('Error: ' + errorThrown);
    }

    Api.prototype.view = function(url, method, authed) {
        return function(data, success, error) {
            if (authed !== undefined)
                data.key = this.key;
            if (error === undefined)
                error = this.requestFailed;
            return this.call(url, method, data).done(success).fail(error);
        }
    };

    window.api = new Api();
})();
