import os
import dash
import dash_bootstrap_components as dbc
from dash import html
from ClearScoreChatbot import ClearScoreChatbot
from model_serving_utils import is_endpoint_supported

# Get serving endpoint from environment
# For local development, set: export SERVING_ENDPOINT=mas-691e9159-endpoint
# For Databricks Apps deployment, this is set in app.yaml
serving_endpoint = os.getenv('SERVING_ENDPOINT')

if not serving_endpoint:
    # Default to the ClearScore customer service agent endpoint if not specified
    serving_endpoint = 'ka-6859840b-endpoint'
    print(f"No SERVING_ENDPOINT set, defaulting to: {serving_endpoint}")

# Skip endpoint validation - let the chatbot try to connect
# The endpoint will fail gracefully with a helpful error message if it doesn't work
print(f"🔧 Endpoint configured: {serving_endpoint}")
print(f"   Skipping strict validation - will attempt connection when first message is sent")
endpoint_supported = True  # Always allow the chatbot to load

# Initialize the Dash app with a modern theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "ClearScore Customer Service AI Agent"

# Define the app layout based on endpoint support
if not endpoint_supported:
    app.layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2('💬 ClearScore Customer Service AI Agent', className='mb-3'),
                dbc.Alert([
                    html.H5("Endpoint Type Not Supported", className="alert-heading mb-3"),
                    html.P(f"The endpoint '{serving_endpoint}' is not compatible with this chatbot template.", 
                           className="mb-2"),
                    html.P("This template supports chat completions-compatible endpoints and Databricks agents.", 
                           className="mb-3"),
                    html.Div([
                        html.P([
                            "For more information, visit the ",
                            html.A("Databricks Agent Framework documentation", 
                                   href="https://docs.databricks.com/en/generative-ai/agent-framework/chat-app",
                                   target="_blank",
                                   className="alert-link"),
                            "."
                        ], className="mb-0")
                    ])
                ], color="warning", className="mt-4")
            ], width={'size': 10, 'offset': 1})
        ])
    ], fluid=True)
else:
    # Create the ClearScore customer service chatbot component
    chatbot = ClearScoreChatbot(
        app=app, 
        endpoint_name=serving_endpoint, 
        height='700px'
    )
    
    app.layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1('💬 ClearScore Customer Service AI Agent', className='text-center mb-2'),
                    html.P([
                        'Powered by Databricks AI • Get instant answers to ClearScore customer queries'
                    ], className='text-center text-muted mb-4'),
                ]),
                chatbot.layout
            ], width={'size': 10, 'offset': 1})
        ], className='mt-4')
    ], fluid=True, className='py-4')

if __name__ == '__main__':
    # For local development
    app.run(host='0.0.0.0', port=8000, debug=True)

