from utils import ui, chart


ui.st_header()

# Overall Scores
chart.add_overall_statistics()
# KPI Cards
chart.add_kpi_cards()
# Overtime Score
chart.add_overtime_score()

# Fancy stuff
ui.felicitation()
