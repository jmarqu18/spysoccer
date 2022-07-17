from django import forms

from .models import PerformanceReport


class PerformanceReportForm(forms.ModelForm):
    class Meta:
        model = PerformanceReport
        exclude = ["id", "scout", "player"]


class PerformanceReportPorteroForm(forms.ModelForm):
    class Meta:
        model = PerformanceReport
        fields = [
            "match_date",
            "notes",
            "height",
            "physical_power",
            "right_foot",
            "left_foot",
            "determined",
            "intelligence",
            "positioning",
            "gk_saves",
            "gk_footwork",
            "gk_aerial_game",
            "gk_penalty_saves",
            "gk_comunication",
            "gk_goal_kicks",
            "gk_one_to_one",
            "gk_box_domain",
            "gk_crosses",
            "gk_grip",
            "command_of_defence",
            "decision_making",
            "quick_short_distance",
            "traveling_ball",
            "off_the_ball_movements",
            "trickery",
            "dealing_with_offside",
            "work_rate",
        ]


class PerformanceReportCentralForm(forms.ModelForm):
    class Meta:
        model = PerformanceReport
        fields = [
            "match_date",
            "notes",
            "height",
            "physical_power",
            "right_foot",
            "left_foot",
            "determined",
            "intelligence",
            "positioning",
            "turns",
            "back_movement",
            "lateral_movement",
            "pace",
            "quick_short_distance",
            "covering_depth",
            "short_passing",
            "long_passing",
            "aerial_game",
            "tackling",
            "anticipating",
            "command_of_defence",
            "composture_on_the_ball",
        ]


class PerformanceReportLateralForm(forms.ModelForm):
    class Meta:
        model = PerformanceReport
        fields = [
            "match_date",
            "notes",
            "height",
            "right_foot",
            "left_foot",
            "determined",
            "pace",
            "quick_short_distance",
            "turns",
            "back_movement",
            "lateral_movement",
            "work_rate",
            "defensive_capacity",
            "lateral_crosses",
            "arrival_baseline",
            "coverings",
            "box_to_box_ability",
            "traveling_ball",
            "tackling",
            "anticipating",
            "dynamism",
            "decision_making",
        ]


class PerformanceReportMediocentroForm(forms.ModelForm):
    class Meta:
        model = PerformanceReport
        fields = [
            "match_date",
            "notes",
            "height",
            "physical_power",
            "right_foot",
            "left_foot",
            "determined",
            "turns",
            "back_movement",
            "lateral_movement",
            "pace",
            "covering_depth",
            "short_passing",
            "long_passing",
            "aerial_game",
            "tackling",
            "anticipating",
            "vision",
            "build_up_capacity",
            "defensive_capacity",
            "work_rate",
            "box_to_box_ability",
        ]


class PerformanceReportMedioOfensivoForm(forms.ModelForm):
    class Meta:
        model = PerformanceReport
        fields = [
            "match_date",
            "notes",
            "height",
            "right_foot",
            "left_foot",
            "determined",
            "pace",
            "quick_short_distance",
            "short_passing",
            "long_passing",
            "composture_on_the_ball",
            "technique",
            "striking_ability",
            "vision",
            "key_passing",
            "link_up_play",
            "dynamism",
            "decision_making",
            "shooting",
            "through_passing",
            "build_up_capacity",
            "trickery",
        ]


class PerformanceReportExtremoForm(forms.ModelForm):
    class Meta:
        model = PerformanceReport
        fields = [
            "match_date",
            "notes",
            "height",
            "right_foot",
            "left_foot",
            "determined",
            "pace",
            "quick_short_distance",
            "short_passing",
            "technique",
            "striking_ability",
            "vision",
            "key_passing",
            "link_up_play",
            "dynamism",
            "decision_making",
            "lateral_crosses",
            "arrival_baseline",
            "trickery",
            "traveling_ball",
            "off_the_ball_movements",
            "shooting",
        ]


class PerformanceReportDelanteroForm(forms.ModelForm):
    class Meta:
        model = PerformanceReport
        fields = [
            "match_date",
            "notes",
            "height",
            "physical_power",
            "right_foot",
            "left_foot",
            "determined",
            "intelligence",
            "positioning",
            "technique",
            "striking_ability",
            "dynamism",
            "decision_making",
            "off_the_ball_movements",
            "trickery",
            "dealing_with_offside",
            "work_rate",
            "shooting",
            "through_passing",
            "pace",
            "hold_up_play",
            "aerial_game",
        ]
