$(document).ready(function() {
    
    var active = 'use-login';

    var checkRadioButtons = function() {
           $("input[name='input-type']").each(
                function (index,radio) {
                    if (radio.checked) {
                        $("#"+radio.value).show("fast");
                        active = radio.value;
                    } else {
                        $("#"+radio.value).hide("fast");
                        $("#"+radio.value+" .error").hide();
                    }
                }
            )
        };

    checkRadioButtons();
    $("input[name='input-type']").change(checkRadioButtons);

    $('#source-help').click(
        function() {
            $('#source-help-text').slideToggle();
        }
    );

    $('#import-button').click(
        function() {
            var good = true;
            if (! $('#guser').val() || ! $('#gpass').val()) {
                $('#gerror').slideDown();
                good = false;
            }
            if (active == 'use-login') {
                if (! $('#zUser').val() || ! $('#zUser').val()) {
                    good = false;
                    $("#"+active+' .error').slideDown();
                }
            } else {
                if (! $('#source').val()) {
                    good = false;
                    $("#"+active+' .error').slideDown();
                } 
            }
            if (good) {
                if (active == 'use-source') {
                     $('#use-login :input').each(function(i,e) { e.value="" });
                }
                $('#import-timetable').submit();
            }
        }
    );
});
