import dash
from dash import html, Input, Output, State, dcc
import dash_bootstrap_components as dbc
from model_serving_utils import query_endpoint

class ClearScoreChatbot:
    """ClearScore Customer Service AI Agent Chatbot Component"""
    
    def __init__(self, app, endpoint_name, height='700px'):
        self.app = app
        self.endpoint_name = endpoint_name
        self.height = height
        self.layout = self._create_layout()
        self._create_callbacks()
        self._add_custom_css()

    def _create_layout(self):
        """Create the chatbot UI layout"""
        return html.Div([
            # Suggested prompts section
            html.Div([
                html.H6('💡 Common Customer Questions:', className='mb-2'),
                html.Div([
                    dbc.Button('How do I check my credit score?', 
                              id='prompt-1', size='sm', color='light', className='me-2 mb-2'),
                    dbc.Button('How can I improve my credit score?', 
                              id='prompt-2', size='sm', color='light', className='me-2 mb-2'),
                    dbc.Button('Why has my score changed?', 
                              id='prompt-3', size='sm', color='light', className='me-2 mb-2'),
                    dbc.Button('How do I update my personal details?', 
                              id='prompt-4', size='sm', color='light', className='me-2 mb-2'),
                    dbc.Button('What credit products are available?', 
                              id='prompt-5', size='sm', color='light', className='me-2 mb-2'),
                    dbc.Button('How do I close my account?', 
                              id='prompt-6', size='sm', color='light', className='mb-2'),
                ], className='d-flex flex-wrap')
            ], className='mb-3', id='suggested-prompts'),
            
            # Chat card
            dbc.Card([
                dbc.CardBody([
                    html.Div([], id='chat-history', className='chat-history', style={'height': self.height}),
                ], className='chat-body p-0')
            ], className='chat-card mb-3'),
            
            # Input section
            dbc.InputGroup([
                dbc.Input(
                    id='user-input', 
                    placeholder='Ask a question about ClearScore services...', 
                    type='text',
                    className='user-input'
                ),
                dbc.Button('Send', id='send-button', color='success', n_clicks=0),
                dbc.Button('Clear Chat', id='clear-button', color='danger', n_clicks=0, outline=True),
            ], className='mb-2'),
            
            # Info text
            html.Div([
                html.Small([
                    '🔒 Secure • Powered by Databricks AI • ',
                    html.Span(f'Endpoint: {self.endpoint_name}', className='text-muted')
                ], className='text-muted')
            ], className='text-center'),
            
            # Hidden stores for state management
            dcc.Store(id='assistant-trigger', data=None),
            dcc.Store(id='chat-history-store', data=[]),
            html.Div(id='dummy-output', style={'display': 'none'}),
        ], className='chat-container')

    def _create_callbacks(self):
        """Create Dash callbacks for interactivity"""
        
        # Handle suggested prompt clicks
        @self.app.callback(
            Output('user-input', 'value', allow_duplicate=True),
            [
                Input('prompt-1', 'n_clicks'),
                Input('prompt-2', 'n_clicks'),
                Input('prompt-3', 'n_clicks'),
                Input('prompt-4', 'n_clicks'),
                Input('prompt-5', 'n_clicks'),
                Input('prompt-6', 'n_clicks'),
            ],
            prevent_initial_call=True
        )
        def set_prompt(p1, p2, p3, p4, p5, p6):
            ctx = dash.callback_context
            if not ctx.triggered:
                return dash.no_update
            
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            prompts = {
                'prompt-1': 'How do I check my credit score?',
                'prompt-2': 'How can I improve my credit score?',
                'prompt-3': 'Why has my score changed?',
                'prompt-4': 'How do I update my personal details?',
                'prompt-5': 'What credit products are available?',
                'prompt-6': 'How do I close my account?',
            }
            return prompts.get(button_id, '')
        
        # Handle user message submission
        @self.app.callback(
            Output('chat-history-store', 'data', allow_duplicate=True),
            Output('chat-history', 'children', allow_duplicate=True),
            Output('user-input', 'value', allow_duplicate=True),
            Output('assistant-trigger', 'data'),
            [
                Input('send-button', 'n_clicks'),
                Input('user-input', 'n_submit'),
            ],
            [
                State('user-input', 'value'),
                State('chat-history-store', 'data'),
            ],
            prevent_initial_call=True
        )
        def update_chat(send_clicks, user_submit, user_input, chat_history):
            if not user_input or not user_input.strip():
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update

            # Initialize chat_history as empty list if None
            if chat_history is None:
                chat_history = []
            
            chat_history.append({'role': 'user', 'content': user_input.strip()})
            
            # Display messages including typing indicator
            chat_display = self._format_chat_display(chat_history)
            chat_display.append(self._create_typing_indicator())

            return chat_history, chat_display, '', {'trigger': True}

        # Process assistant response
        @self.app.callback(
            Output('chat-history-store', 'data', allow_duplicate=True),
            Output('chat-history', 'children', allow_duplicate=True),
            Input('assistant-trigger', 'data'),
            State('chat-history-store', 'data'),
            prevent_initial_call=True
        )
        def process_assistant_response(trigger, chat_history):
            if not trigger or not trigger.get('trigger'):
                return dash.no_update, dash.no_update

            # Initialize chat_history as empty list if None
            if chat_history is None:
                chat_history = []
                
            if (not chat_history or not isinstance(chat_history[-1], dict)
                    or 'role' not in chat_history[-1]
                    or chat_history[-1]['role'] != 'user'):
                return dash.no_update, dash.no_update

            try:
                print(f"🤖 Calling ClearScore customer service agent: {self.endpoint_name}")
                assistant_response = self._call_model_endpoint(chat_history)
                
                # Ensure we got a valid response
                if not assistant_response:
                    assistant_response = "I apologize, but I received an empty response. Please try again."
                    
                chat_history.append({
                    'role': 'assistant',
                    'content': str(assistant_response)
                })
                print(f"✅ Agent response received")
            except Exception as e:
                error_message = f'⚠️ Error: Unable to get response from agent. {str(e)}'
                print(f"❌ Error: {error_message}")
                chat_history.append({
                    'role': 'assistant',
                    'content': error_message
                })

            chat_display = self._format_chat_display(chat_history)
            return chat_history, chat_display

        # Clear chat history
        @self.app.callback(
            Output('chat-history-store', 'data', allow_duplicate=True),
            Output('chat-history', 'children', allow_duplicate=True),
            Input('clear-button', 'n_clicks'),
            prevent_initial_call=True
        )
        def clear_chat(n_clicks):
            if n_clicks and n_clicks > 0:
                print('🗑️ Clearing chat history')
                return [], []
            return dash.no_update, dash.no_update

    def _call_model_endpoint(self, messages, max_tokens=2048):
        """Call the Databricks model serving endpoint"""
        try:
            response = query_endpoint(self.endpoint_name, messages, max_tokens)
            return response["content"]
        except Exception as e:
            print(f'Error calling model endpoint: {str(e)}')
            raise

    def _format_chat_display(self, chat_history):
        """Format chat messages for display"""
        formatted_messages = []
        for msg in chat_history:
            if isinstance(msg, dict) and 'role' in msg:
                # Split content by line breaks and create separate paragraphs
                content = msg['content']
                # Split by double newlines (our chunk separator)
                paragraphs = content.split('\n\n')
                
                # Create paragraph elements
                content_elements = []
                for para in paragraphs:
                    if para.strip():  # Only add non-empty paragraphs
                        # Further split by single newlines for line breaks within paragraphs
                        lines = para.split('\n')
                        para_content = []
                        for i, line in enumerate(lines):
                            if line.strip():
                                para_content.append(line)
                                if i < len(lines) - 1:  # Add br between lines
                                    para_content.append(html.Br())
                        
                        content_elements.append(
                            html.P(para_content, style={'margin-bottom': '10px'})
                        )
                
                formatted_messages.append(
                    html.Div([
                        html.Div([
                            html.Div('👤' if msg['role'] == 'user' else '🤖', 
                                    className='message-icon'),
                            html.Div(content_elements, className='message-text')
                        ], className=f"chat-message {msg['role']}-message")
                    ], className=f"message-container {msg['role']}-container")
                )
        
        return formatted_messages

    def _create_typing_indicator(self):
        """Create animated typing indicator"""
        return html.Div([
            html.Div([
                html.Div('🤖', className='message-icon'),
                html.Div([
                    html.Div(className='typing-dot'),
                    html.Div(className='typing-dot'),
                    html.Div(className='typing-dot')
                ], className='typing-indicator')
            ], className='chat-message assistant-message typing-message')
        ], className='message-container assistant-container')

    def _add_custom_css(self):
        """Add custom CSS styling with ClearScore branding"""
        custom_css = '''
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #EC4899 100%);
            min-height: 100vh;
        }
        
        .chat-container {
            background-color: #FFFFFF;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 24px;
        }
        
        .chat-card {
            border: 2px solid #e5e7eb;
            background-color: #f9fafb;
            border-radius: 12px;
            overflow: hidden;
        }
        
        .chat-body {
            background-color: #ffffff;
        }
        
        .chat-history {
            overflow-y: auto;
            padding: 20px;
            background: linear-gradient(to bottom, #ffffff 0%, #f9fafb 100%);
        }
        
        .message-container {
            display: flex;
            margin-bottom: 16px;
            animation: fadeIn 0.3s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user-container {
            justify-content: flex-end;
        }
        
        .chat-message {
            max-width: 75%;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 15px;
            line-height: 1.5;
            display: flex;
            gap: 10px;
            align-items: flex-start;
        }
        
        .message-icon {
            font-size: 20px;
            flex-shrink: 0;
        }
        
        .message-text {
            flex: 1;
            word-wrap: break-word;
        }
        
        .user-message {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
        }
        
        .assistant-message {
            background-color: #f3f4f6;
            color: #1f2937;
            border: 1px solid #e5e7eb;
        }
        
        .typing-message {
            background-color: #f3f4f6;
            border: 1px solid #e5e7eb;
        }
        
        .typing-indicator {
            display: flex;
            gap: 4px;
            padding: 8px 0;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            background-color: #9ca3af;
            border-radius: 50%;
            animation: typing-animation 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) { animation-delay: 0s; }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing-animation {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-8px); }
        }
        
        .user-input {
            border-radius: 24px;
            border: 2px solid #e5e7eb;
            padding: 12px 20px;
            font-size: 15px;
        }
        
        .user-input:focus {
            border-color: #4F46E5;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }
        
        #send-button {
            border-radius: 24px;
            padding: 12px 28px;
            font-weight: 600;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            border: none;
        }
        
        #send-button:hover {
            background: linear-gradient(135deg, #059669 0%, #047857 100%);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
        }
        
        #clear-button {
            border-radius: 24px;
            padding: 12px 24px;
            font-weight: 600;
            border: 2px solid #ef4444;
            color: #ef4444;
        }
        
        #clear-button:hover {
            background-color: #ef4444;
            color: white;
        }
        
        .btn-light {
            background-color: #f3f4f6;
            border: 1px solid #d1d5db;
            color: #4b5563;
            border-radius: 20px;
            padding: 6px 14px;
            font-size: 13px;
            transition: all 0.2s;
        }
        
        .btn-light:hover {
            background-color: #4F46E5;
            color: white;
            border-color: #4F46E5;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(79, 70, 229, 0.3);
        }
        
        .input-group {
            gap: 8px;
        }
        
        /* Scrollbar styling */
        .chat-history::-webkit-scrollbar {
            width: 8px;
        }
        
        .chat-history::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        .chat-history::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        
        .chat-history::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        '''
        
        self.app.index_string = self.app.index_string.replace(
            '</head>',
            f'<style>{custom_css}</style></head>'
        )

        # Auto-scroll chat to bottom
        self.app.clientside_callback(
            """
            function(children) {
                var chatHistory = document.getElementById('chat-history');
                if(chatHistory) {
                    chatHistory.scrollTop = chatHistory.scrollHeight;
                }
                return '';
            }
            """,
            Output('dummy-output', 'children'),
            Input('chat-history', 'children'),
            prevent_initial_call=True
        )

