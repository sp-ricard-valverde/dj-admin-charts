if (!$) {
    $ = django.jQuery;
}

function toggleChildrenState(el, checked) {
    var selection = el.find('.colorpicker');

    if (checked) {
        el.find('*').attr("disabled", false);
        el.find('label').removeClass('disabled');
        if (selection.length) {
            selection.spectrum('enable');
        }
    }
    else {
        el.find('*').attr("disabled", true);
        el.find('label').addClass('disabled');
        if (selection.length) {
            selection.spectrum('disable');
        }
    }
}

function OnToggleConfigGroup(checked, id) {
    $("#"+id+"_group").toggle();
}

function OnResponsiveChanged(checked) {
    toggleChildrenState($('.field-config_responsiveAnimationDuration'), checked);
}

function OnDisplayTitleChanged(checked) {
    toggleChildrenState($('#title_sub_group'), checked);
}

function OnDisplayLegendChanged(checked) {
    toggleChildrenState($('#legend_sub_group'), checked);
}

function OnEnableTooltipChanged(checked) {
    toggleChildrenState($('#tooltip_sub_group'), checked);
}

