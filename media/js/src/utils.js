define([], function() {
    var utils = {
        /**
         * Convert number of seconds to a an H:M:S string.
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
        }
    };

    return utils;
});
