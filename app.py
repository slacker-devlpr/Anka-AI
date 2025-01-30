import dash
from dash import html

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server  # Required for Render

# Define the layout
app.layout = html.Div([
    html.H1("Hello, Render!"),
    html.P("This is a test Dash app deployed on Render."),
])

# Run the app (only for local testing)
if __name__ == "__main__":
    app.run_server(debug=True)
