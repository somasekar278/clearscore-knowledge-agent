# 🚀 Deployment Guide - ClearScore Customer Service AI Agent

Complete step-by-step guide to deploy your ClearScore chatbot to Databricks Apps.

## Prerequisites Checklist

Before deploying, ensure you have:

- [ ] Databricks workspace access
- [ ] Your agent endpoint deployed and accessible (`mas-691e9159-endpoint`)
- [ ] `CAN_QUERY` permission on the serving endpoint
- [ ] Databricks personal access token (PAT)
- [ ] Databricks CLI installed (optional but recommended)

## Deployment Methods

### 🎯 Method 1: Databricks CLI (Recommended)

This is the fastest and most reliable method.

#### Step 1: Install Databricks CLI

```bash
# Using pip
pip install databricks-cli

# Or using conda
conda install -c conda-forge databricks-cli

# Verify installation
databricks --version
```

#### Step 2: Configure Authentication

```bash
databricks configure --token
```

When prompted, enter:
- **Databricks Host**: `https://e2-demo-field-eng.cloud.databricks.com`
- **Token**: Your personal access token (get from User Settings → Developer → Access Tokens)

#### Step 3: Navigate to App Directory

```bash
cd /Users/som.natarajan/fraud-case-management/clearscore-chatbot
```

#### Step 4: Create the App

```bash
databricks apps create clearscore-customer-service
```

#### Step 5: Deploy the App

```bash
databricks apps deploy clearscore-customer-service --source-code-path .
```

This will:
- ✅ Upload all files
- ✅ Install dependencies from `requirements.txt`
- ✅ Start the app
- ✅ Provide you with the app URL

#### Step 6: Access Your App

The CLI will output a URL like:
```
https://e2-demo-field-eng.cloud.databricks.com/apps/clearscore-customer-service
```

Open this URL in your browser!

#### Optional: Update the App

When you make changes:

```bash
databricks apps deploy clearscore-customer-service --source-code-path .
```

#### Optional: View Logs

```bash
databricks apps logs clearscore-customer-service
```

---

### 🖱️ Method 2: Databricks Workspace UI

Use this if you prefer a visual interface.

#### Step 1: Prepare Files

1. Navigate to `/Users/som.natarajan/fraud-case-management/clearscore-chatbot`
2. Ensure all files are present:
   - `app.py`
   - `ClearScoreChatbot.py`
   - `model_serving_utils.py`
   - `requirements.txt`
   - `app.yaml`

#### Step 2: Access Databricks Apps

1. Open your Databricks workspace: `https://e2-demo-field-eng.cloud.databricks.com`
2. Click on **Apps** in the left sidebar
3. Click **Create App**

#### Step 3: Configure the App

1. **App Name**: `clearscore-customer-service`
2. **Source Code**: Choose "Upload Files"
3. **Upload** all files from the `clearscore-chatbot` directory
4. **Configuration**: The system will read from `app.yaml`

#### Step 4: Review Configuration

Verify in `app.yaml`:

```yaml
command: ["python", "app.py"]

env:
  - name: "SERVING_ENDPOINT"
    value: "mas-691e9159-endpoint"
```

#### Step 5: Deploy

1. Click **Deploy**
2. Wait for deployment to complete (usually 2-5 minutes)
3. Status will change to "Running"

#### Step 6: Access Your App

Click on the app URL provided in the UI.

---

### 🐳 Method 3: Local Testing Before Deployment

Test locally before deploying to ensure everything works.

#### Step 1: Set Up Local Environment

```bash
cd /Users/som.natarajan/fraud-case-management/clearscore-chatbot

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: Configure Environment Variables

```bash
# Set your endpoint
export SERVING_ENDPOINT=mas-691e9159-endpoint

# Set Databricks credentials for local testing
export DATABRICKS_HOST=https://e2-demo-field-eng.cloud.databricks.com
export DATABRICKS_TOKEN=your_databricks_token_here
```

#### Step 3: Run Locally

```bash
python app.py
```

#### Step 4: Test in Browser

Open http://localhost:8000 and test:
- ✅ Chat interface loads
- ✅ Suggested questions work
- ✅ Agent responds to queries
- ✅ Clear chat works

#### Step 5: Deploy to Production

Once satisfied, use Method 1 or 2 above to deploy to Databricks Apps.

---

## Configuring Serving Endpoint Permissions

If you get permission errors, ensure you have access:

### Option 1: Request Permission from Admin

Ask your Databricks admin to grant you `CAN_QUERY` permission on `mas-691e9159-endpoint`.

### Option 2: Use Resource Binding (Recommended)

Update `app.yaml` to use resource binding:

```yaml
command: ["python", "app.py"]

env:
  - name: "SERVING_ENDPOINT"
    valueFrom: "serving-endpoint"

resources:
  serving-endpoints:
    - name: serving-endpoint
      endpoint: mas-691e9159-endpoint
      permission: CAN_QUERY
```

This automatically manages permissions when the app is deployed.

---

## Post-Deployment Tasks

### 1. Test the Deployment

Test common scenarios:
- [ ] Ask about credit scores
- [ ] Try suggested questions
- [ ] Test with long conversations
- [ ] Clear chat history
- [ ] Test error handling (ask something off-topic)

### 2. Share with Team

Share the app URL with your team:
```
https://e2-demo-field-eng.cloud.databricks.com/apps/clearscore-customer-service
```

### 3. Set Up Monitoring

Monitor your app's health:

```bash
# View logs
databricks apps logs clearscore-customer-service --tail

# Check status
databricks apps get clearscore-customer-service
```

### 4. Configure Access Control

In Databricks workspace:
1. Go to **Apps** → Your app
2. Click **Permissions**
3. Add users or groups who should have access

### 5. Document the URL

Add to your internal documentation:
- App URL
- Purpose: ClearScore customer service chatbot
- Contact: Your team
- Endpoint: `mas-691e9159-endpoint`

---

## Troubleshooting Deployment Issues

### Issue: "Could not find endpoint"

**Cause**: Endpoint name is incorrect or you don't have permission.

**Solution**:
1. Verify endpoint name in Databricks workspace under **Serving**
2. Ensure endpoint is in "Ready" state
3. Check you have `CAN_QUERY` permission

### Issue: "ModuleNotFoundError"

**Cause**: Missing dependencies in `requirements.txt`.

**Solution**:
1. Check `requirements.txt` has all required packages
2. Redeploy the app
3. Check logs: `databricks apps logs clearscore-customer-service`

### Issue: "App fails to start"

**Cause**: Python syntax error or configuration issue.

**Solution**:
1. Test locally first (see Method 3)
2. Check logs for error messages
3. Verify `app.yaml` format is correct

### Issue: "Slow response times"

**Cause**: Endpoint provisioning or cold start.

**Solutions**:
- Enable endpoint auto-scaling
- Use a larger model serving instance type
- Implement response caching

### Issue: "Permission denied"

**Cause**: Missing permissions on the serving endpoint.

**Solution**:
1. Use resource binding in `app.yaml` (see above)
2. Or request `CAN_QUERY` permission from admin

---

## Updating Your Deployed App

When you make changes to the code:

### Quick Update

```bash
databricks apps deploy clearscore-customer-service --source-code-path .
```

### Zero-Downtime Update

1. Create a new version:
   ```bash
   databricks apps create clearscore-customer-service-v2
   databricks apps deploy clearscore-customer-service-v2 --source-code-path .
   ```

2. Test the new version

3. Switch traffic:
   - Update your documentation to point to v2
   - Deprecate v1 after confirming v2 works

---

## Production Best Practices

### 1. Use Secrets for Sensitive Data

Don't hardcode tokens. Use Databricks Secrets:

```yaml
env:
  - name: "DATABRICKS_TOKEN"
    valueFrom:
      secretKeyRef:
        scope: customer-service
        key: agent-token
```

Create the secret:
```bash
databricks secrets create-scope customer-service
databricks secrets put-secret customer-service agent-token
```

### 2. Enable Logging

Add structured logging in your code:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"User query: {user_message}")
logger.info(f"Agent response time: {response_time}ms")
```

### 3. Set Resource Limits

In `app.yaml`:

```yaml
resources:
  cpu: "2"
  memory: "4Gi"
```

### 4. Enable Auto-Scaling

Configure your serving endpoint for auto-scaling to handle traffic spikes.

### 5. Implement Rate Limiting

Add rate limiting to prevent abuse:

```python
from functools import wraps
import time

def rate_limit(max_calls=10, time_window=60):
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls
            calls[:] = [c for c in calls if c > now - time_window]
            
            if len(calls) >= max_calls:
                return {"error": "Rate limit exceeded"}
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### 6. Monitor Costs

Track your serving endpoint costs:
1. Go to **Serving** in Databricks
2. View usage metrics
3. Optimize model size and instance type if needed

---

## Next Steps

After successful deployment:

1. ✅ **Customize branding**: Update colors in `ClearScoreChatbot.py`
2. ✅ **Add more prompts**: Expand suggested questions
3. ✅ **Integrate AI functions**: Add `ai_summarize()`, `ai_classify()` features
4. ✅ **Add analytics**: Track usage and popular questions
5. ✅ **Enable feedback**: Add thumbs up/down for responses
6. ✅ **Multi-language**: Add language detection and translation

---

## Support and Resources

- **Databricks Docs**: https://docs.databricks.com/en/dev-tools/databricks-apps/
- **Agent Framework**: https://docs.databricks.com/en/generative-ai/agent-framework/
- **Dash Docs**: https://dash.plotly.com/
- **Your Team**: Contact your Databricks admin for workspace-specific help

---

**🎉 Congratulations on deploying your ClearScore Customer Service AI Agent!**

For questions or issues, refer to the troubleshooting section or contact your Databricks account team.

