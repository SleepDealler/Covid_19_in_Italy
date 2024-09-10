import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
template = pio.templates["seaborn"]  # Or your custom template
template.layout.font = go.layout.Font(
    family="Arial",  # Font family (e.g., "Arial", "Helvetica", "Times New Roman")
    size=16  # Font size (adjust as needed)
)
pio.templates.default = template
pio.kaleido.scope.default_height = 576
pio.kaleido.scope.default_width = 1040
pio.kaleido.scope.default_scale = 2

def color_palette():
    return 'Inferno_r'

def color_palette_plt():
    return 'inferno_r'

def animation_len():
    return 30

