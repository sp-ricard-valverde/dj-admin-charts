from django import forms

from .fields import ColorField, FormField
from .widgets import ColorWidget
from ..models import ChartModel

POSITION = (('top', 'Top'),
            ('left', 'Left'),
            ('right', 'Right'),
            ('bottom', 'Bottom'))

INTERACTION = (('point', 'Point'),
               ('nearest', 'Nearest'),
               ('index', 'Index'),
               ('dataset', 'Dataset'),
               ('x', 'X'),
               ('y', 'Y'))

TOOLTIP_POSITION = (('average', 'Average'),
                    ('nearest', 'Nearest'))

EASING = (('linear', 'Linear'),
          ('easeInQuad', 'EaseInQuad'), ('easeOutQuad',
                                         'EaseOutQuad'), ('easeInOutQuad', 'EaseInOutQuad'),
          ('easeInCubic', 'EaseInCubic'), ('easeOutCubic',
                                           'EaseOutCubic'), ('easeInOutCubic', 'EaseInOutCubic'),
          ('easeInQuart', 'EaseInQuart'), ('easeOutQuart',
                                           'EaseOutQuart'), ('easeInOutQuart', 'EaseInOutQuart'),
          ('easeInQuint', 'EaseInQuint'), ('easeOutQuint',
                                           'EaseOutQuint'), ('easeInOutQuint', 'EaseInOutQuint'),
          ('easeInSine', 'EaseInSine'), ('easeOutSine',
                                         'EaseOutSine'), ('easeInOutSine', 'EaseInOutSine'),
          ('easeInExpo', 'EaseInExpo'), ('easeOutExpo',
                                         'EaseOutExpo'), ('easeInOutExpo', 'EaseInOutExpo'),
          ('easeInCirc', 'EaseInCirc'), ('easeOutCirc',
                                         'EaseOutCirc'), ('easeInOutCirc', 'EaseInOutCirc'),
          ('easeInElastic', 'EaseInElastic'), ('easeOutElastic', 'EaseOutElastic'),
          ('easeInOutElastic', 'EaseInOutElastic'),
          ('easeInBack', 'EaseInBack'), ('easeOutBack',
                                         'EaseOutBack'), ('easeInOutBack', 'EaseInOutBack'),
          ('easeInBounce', 'EaseInBounce'), ('easeOutBounce', 'EaseOutBounce'), ('easeInOutBounce', 'EaseInOutBounce'))

registered_dataset_classes = []


def register_dataset(cls):
    global registered_dataset_classes
    registered_dataset_classes.append(cls)


class BaseDatasetForm(forms.Form):

    class Media:
        js = ('js/AdminChart.js',)
        css = {
            'all': ('css/AdminChart.css',)
        }


class ActionDurationDatasetForm(BaseDatasetForm):
    action_duration_dataset_limit = forms.IntegerField(
        min_value=1, max_value=10, initial=10, label="Limit")


class MutableDatasetForm(forms.Form):
    """
    To be used with a formset structure
    """

    def __init__(self, *args, **kwargs):
        super(MutableDatasetForm, self).__init__(*args, **kwargs)

        available_classes = tuple([(str(cls), str(cls))
                                   for cls in registered_dataset_classes])

        initial = None if not available_classes else available_classes[0]

        self.fields['dataset_class'] = forms.ChoiceField(
            choices=available_classes, initial=initial, label="Class")

        for cls in registered_dataset_classes:
            form = cls.form()
            for name in form.fields:
                self.fields[name] = form[name].field


class ChartModelForm(forms.ModelForm):
    # Common Chart Configuration
    config_responsive = forms.BooleanField(initial=True, widget=forms.CheckboxInput(
        attrs={'onchange': 'OnResponsiveChanged(this.checked)'}), label="Responsive")
    config_responsiveAnimationDuration = forms.IntegerField(initial=0,
                                                            min_value=0, max_value=9999,
                                                            label="Responsive animation duration")
    config_maintainAspectRatio = forms.BooleanField(
        initial=True, label="Mantain aspect ratio")

    # Title Configuration
    title_display = forms.BooleanField(initial=True, widget=forms.CheckboxInput(
        attrs={'onchange': 'OnDisplayTitleChanged(this.checked)'}), label="Display")
    title_position = forms.ChoiceField(
        choices=POSITION, initial='top', label="Position")
    title_text = forms.CharField(max_length=128, label="Text")

    # Legend Configuration
    legend_display = forms.BooleanField(initial=True, widget=forms.CheckboxInput(
        attrs={'onchange': 'OnDisplayLegendChanged(this.checked)'}), label="Display")
    legend_position = forms.ChoiceField(
        choices=POSITION, initial='top', label="Position")

    # Tooltip Configuration
    tooltip_enabled = forms.BooleanField(initial=True, widget=forms.CheckboxInput(
        attrs={'onchange': 'OnEnableTooltipChanged(this.checked)'}), label="Enabled")
    tooltip_mode = forms.ChoiceField(
        choices=INTERACTION, initial='nearest', label="Mode")
    tooltip_intersect = forms.BooleanField(initial=True, label="Intersect")
    tooltip_position = forms.ChoiceField(
        choices=TOOLTIP_POSITION, initial='average', label="Position")
    tooltip_backgroundColor = ColorField(
        widget=ColorWidget(attrs={'options': {
            'showAlpha': True, 'showInput': True, 'preferredFormat': 'rgb'}}),
        label="Background Color")

    # Hover Configuration
    hover_mode = forms.ChoiceField(
        choices=INTERACTION, initial='nearest', label="Mode")
    hover_intersect = forms.BooleanField(initial=True, label="Intersect")
    hover_animationDuration = forms.IntegerField(initial=400,
                                                 min_value=0, max_value=9999,
                                                 label="Animation duration")

    # Animation Configuration
    animation_duration = forms.IntegerField(initial=1000,
                                            min_value=0, max_value=9999,
                                            label="Duration")
    animation_easing = forms.ChoiceField(
        choices=EASING, initial='easeOutQuart', label="Easing")

    class Meta:
        model = ChartModel
        fields = []

    class Media:
        js = ('js/AdminChart.js',)
        css = {
            'all': ('css/AdminChart.css',)
        }
