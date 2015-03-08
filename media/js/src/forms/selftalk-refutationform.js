(function() {
    /**
     * refreshInputDisplay looks at each form in the array '$forms' and
     * hides or shows the 'other' input if the appropriate dropdown
     * option is selected.
     *
     * Params:
     * $dropdowns - an array of <select> elements.
     */
    function refreshInputDisplay($dropdowns) {
        $dropdowns.each(function(k, v) {
            var $v = $(v);
            var val = $v.val();
            var selectedText = $.trim(
                $v.find('option[value=' + val + ']').text());

            var $otherInput = $v.closest('.form-group').next().find('input');
            if (selectedText.toLowerCase() === 'other') {
                $otherInput.show();
            } else {
                $otherInput.hide();
            }
        });
    }

    $(document).ready(function() {
        var $el = $('#selftalk-refutation-block');
        var $dropdowns = $el.find('.refutation-dropdown');

        $dropdowns.on('change', function() {
            refreshInputDisplay($dropdowns);
        });
        refreshInputDisplay($dropdowns);
    });
})();
