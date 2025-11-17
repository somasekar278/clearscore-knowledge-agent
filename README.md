# 💬 ClearScore Customer Service AI Agent

A beautiful, production-ready chatbot interface for ClearScore customer service, powered by Databricks AI and built with Dash. Designed to be deployed as a Databricks App.

## 🎯 Features

- ✨ **Modern UI**: Beautiful gradient design with smooth animations
- 🤖 **Databricks AI Integration**: Connects to your ClearScore customer service agent endpoint
- 💬 **Chat Interface**: Full conversation history with user and assistant messages
- 🎨 **Suggested Questions**: Quick-start prompts for common customer queries
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile
- 🔒 **Secure**: Integrates with Databricks authentication and permissions
- 🚀 **Production Ready**: Designed for Databricks Apps deployment

## 🏗️ Architecture

This app is based on the [Databricks dash-chatbot-app template](https://github.com/databricks/app-templates/tree/main/dash-chatbot-app) and customized for ClearScore customer service.

**Key Components:**
- `app.py` - Main application entry point
- `ClearScoreChatbot.py` - Chatbot UI component with customer service features
- `model_serving_utils.py` - Utilities for calling Databricks serving endpoints
- `app.yaml` - Databricks Apps deployment configuration

## 📋 Prerequisites

- Databricks workspace with access to Model Serving
- A deployed customer service agent endpoint (e.g., `mas-691e9159-endpoint`)
- Python 3.9 or higher
- Databricks CLI (for deployment)

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your endpoint:**
   ```bash
   export SERVING_ENDPOINT=mas-691e9159-endpoint
   ```

3. **Configure Databricks authentication:**
   ```bash
   export DATABRICKS_HOST=https://e2-demo-field-eng.cloud.databricks.com
   export DATABRICKS_TOKEN=your_token_here
   ```

4. **Run the app:**
   ```bash
   python app.py
   ```

5. **Open in browser:**
   Navigate to http://localhost:8000

### Databricks Apps Deployment

#### Option 1: Using Databricks CLI (Recommended)

1. **Install Databricks CLI:**
   ```bash
   pip install databricks-cli
   ```

2. **Configure authentication:**
   ```bash
   databricks configure --token
   ```
   Enter your workspace URL and personal access token.

3. **Deploy the app:**
   ```bash
   databricks apps create clearscore-chatbot
   databricks apps deploy clearscore-chatbot --source-code-path .
   ```

4. **Access your app:**
   The CLI will output the URL where your app is running.

#### Option 2: Using Databricks Workspace UI

1. Navigate to **Apps** in your Databricks workspace
2. Click **Create App**
3. Choose **Upload Files** and upload all files from this directory
4. Configure the app using the settings in `app.yaml`
5. Click **Deploy**

## ⚙️ Configuration

### Endpoint Configuration

Update `app.yaml` to point to your customer service agent endpoint:

```yaml
env:
  - name: "SERVING_ENDPOINT"
    value: "mas-691e9159-endpoint"
```

### Using Resource Binding (Recommended for Production)

For better security and automatic permission management:

```yaml
env:
  - name: "SERVING_ENDPOINT"
    valueFrom: "serving-endpoint"

resources:
  serving-endpoints:
    - name: serving-endpoint
      endpoint: mas-691e9159-endpoint
      permission: CAN_QUERY
```

## 🎨 Customization

### Modify Suggested Questions

Edit the prompts in `ClearScoreChatbot.py`:

```python
prompts = {
    'prompt-1': 'How do I check my credit score?',
    'prompt-2': 'How can I improve my credit score?',
    'prompt-3': 'Why has my score changed?',
    'prompt-4': 'How do I update my personal details?',
    'prompt-5': 'What credit products are available?',
    'prompt-6': 'How do I close my account?',
}
```

Add more prompts by:
1. Adding a new button in `_create_layout()`:
   ```python
   dbc.Button('Your question here', 
              id='prompt-7', size='sm', color='light', className='me-2 mb-2'),
   ```
2. Adding the Input in the callback
3. Adding the question to the prompts dictionary

### Adjust Styling

The chatbot uses custom CSS defined in `ClearScoreChatbot._add_custom_css()`. Modify colors, fonts, and layout to match your brand:

```python
# Change gradient colors
background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);

# Change user message bubble colors
.user-message {
    background: linear-gradient(135deg, #YOUR_BRAND_COLOR 0%, #YOUR_BRAND_COLOR_2 100%);
}
```

### Change Max Tokens

In `ClearScoreChatbot._call_model_endpoint()`:

```python
def _call_model_endpoint(self, messages, max_tokens=512):  # Adjust this value
```

Higher values allow longer responses but take more time.

## 🔧 Troubleshooting

### Error: "SERVING_ENDPOINT not configured"

**Solution:** Set the environment variable:
```bash
export SERVING_ENDPOINT=mas-691e9159-endpoint
```

### Error: "Unable to determine serving endpoint"

**Solution:** Ensure your `app.yaml` has the correct endpoint name and that you have `CAN_QUERY` permissions on the endpoint.

### Error: "Endpoint Type Not Supported"

**Solution:** This app supports:
- Databricks agent endpoints (v1/v2)
- Foundation model endpoints with chat task type
- External model endpoints with chat completion support

Verify your endpoint type in the Databricks workspace under **Serving**.

### Connection Issues

1. Check that the endpoint is in the "Ready" state in Databricks
2. Verify you have network access to the workspace
3. Ensure your authentication token is valid and not expired
4. Check that you have `CAN_QUERY` permission on the serving endpoint

### Local Development Authentication Issues

Make sure you have:
```bash
export DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
export DATABRICKS_TOKEN=dapi...your-token
```

## 💡 Common Use Cases

### Customer Service Inquiries
- Credit score questions
- Account management
- Product recommendations
- Troubleshooting issues
- Policy clarifications

### Example Questions
- "How do I check my credit score?"
- "Why did my credit score go down?"
- "How can I dispute an error on my credit report?"
- "What factors affect my credit score?"
- "How do I update my email address?"
- "What credit cards am I eligible for?"

## 🔗 Integration Options

### 1. Standalone Deployment (Current Setup)
Deploy as a separate Databricks App accessible via its own URL.

### 2. Iframe Embedding
Embed the chatbot in your existing web application:

```html
<iframe
  src="https://your-databricks-app-url.com"
  width="100%"
  height="800px"
  style="border: none; border-radius: 8px;"
  title="ClearScore Customer Service"
></iframe>
```

### 3. API Integration
Expose the agent as a REST API and integrate programmatically:

```python
import requests

response = requests.post(
    f"{endpoint_url}/invocations",
    headers={"Authorization": f"Bearer {token}"},
    json={"messages": [{"role": "user", "content": "How do I check my score?"}]}
)
```

## 🚀 Advanced Features You Can Add

### 1. Databricks AI Functions Integration

Use SQL Execution API to add AI functions like `ai_summarize()`, `ai_classify()`:

```python
from databricks import sql

def summarize_conversation(chat_history):
    connection = sql.connect(...)
    cursor = connection.cursor()
    
    full_text = " ".join([msg['content'] for msg in chat_history])
    
    cursor.execute(f"""
        SELECT ai_summarize('{full_text}', 'max_length' => 100)
    """)
    
    return cursor.fetchone()[0]
```

### 2. Multi-Language Support

Add language detection and translation:

```python
cursor.execute(f"""
    SELECT ai_translate('{user_message}', 'target_language' => 'en')
""")
```

### 3. Sentiment Analysis

Track customer satisfaction:

```python
cursor.execute(f"""
    SELECT ai_classify('{user_message}', ARRAY('positive', 'neutral', 'negative'))
""")
```

### 4. Conversation History

Store conversations in a Delta table:

```python
cursor.execute("""
    INSERT INTO customer_conversations 
    VALUES (?, ?, ?, ?)
""", (session_id, timestamp, user_message, agent_response))
```

### 5. Analytics Dashboard

Create a dashboard showing:
- Most common questions
- Average response time
- Customer satisfaction trends
- Topic distribution

## 📚 Additional Resources

- [Databricks Agent Framework Documentation](https://docs.databricks.com/en/generative-ai/agent-framework/index.html)
- [Databricks Apps Documentation](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html)
- [Model Serving Documentation](https://docs.databricks.com/en/machine-learning/model-serving/index.html)
- [Databricks AI Functions](https://docs.databricks.com/en/sql/language-manual/sql-ref-functions-builtin-ai.html)
- [Dash Framework Documentation](https://dash.plotly.com/)

## 🔐 Security Considerations

- ✅ Uses Databricks authentication and authorization
- ✅ Token management handled by Databricks Apps
- ✅ No credentials stored in code
- ✅ Secure communication with serving endpoints
- ✅ Support for resource binding (recommended for production)
- ⚠️ For production, use Databricks Secrets for sensitive configuration

### Using Databricks Secrets

```yaml
env:
  - name: "DATABRICKS_TOKEN"
    valueFrom:
      secretKeyRef:
        scope: customer-service
        key: agent-token
```

## 📊 Monitoring and Observability

Monitor your chatbot's performance:

1. **Endpoint Metrics**: View in Databricks Serving UI
   - Request count
   - Latency
   - Error rate

2. **Application Logs**: Check Databricks Apps logs
   ```bash
   databricks apps logs clearscore-chatbot
   ```

3. **Custom Metrics**: Add logging in your code
   ```python
   print(f"🤖 Query received: {user_message}")
   print(f"⏱️ Response time: {response_time}ms")
   ```

## 🆘 Support

For issues related to:
- **Databricks Apps**: Contact your Databricks account team or check [Databricks docs](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html)
- **Agent Endpoints**: See [Agent Framework docs](https://docs.databricks.com/en/generative-ai/agent-framework/index.html)
- **ClearScore Integration**: Contact your ClearScore technical team

## 📝 License

This project is based on the Databricks app templates and follows the same license terms.

---

**Built with ❤️ using Databricks Agent Framework and Dash**

*Empowering ClearScore customer service teams with AI-powered support*
