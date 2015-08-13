define([
    'underscore'
], function(_) {
    var utils = {
        /**
         * Convert number of seconds to an H:M:S string.
         *
         * http://stackoverflow.com/a/5539081/173630
         */
        secondsToHms: function(d) {
            d = Number(d);

            var h = Math.floor(d / 3600);
            var m = Math.floor(d % 3600 / 60);
            var s = Math.floor(d % 3600 % 60);

            return (
                (h > 0 ? h + ':' + (m < 10 ? '0' : '') : '') +
                    m + ':' + (s < 10 ? '0' : '') + s
            );
        },

        /**
         * Given an array like this:
         *
         *     ['a', 'b', 'c']
         *
         * This function yields:
         *
         *    '<div>a</div><div>b</div><div>c</div>'
         */
        _formatArrayToDivs: function(arr) {
            return _.reduce(
                arr,
                function(memo, str) {
                    return memo + '<div>' + str + '</div>';
                },
                '');
        },

        /**
         * Format a django-rest-framework JSON error to HTML.
         *
         * @return string - A string of HTML.
         */
        formatDrfJsonErrorsToHtml: function(json) {
            var msg = '';

            for (var key in json) {
                if (_.isArray(json[key])) {
                    msg += this._formatArrayToDivs(json[key]);
                }
            }

            return msg;
        }
    };

    return utils;
});
