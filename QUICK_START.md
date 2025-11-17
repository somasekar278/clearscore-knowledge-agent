# 🚀 ClearScore Chatbot - Quick Start Guide

## What You Have

A complete, production-ready **ClearScore Customer Service AI Agent** chatbot that:
- ✅ Connects to your Databricks agent endpoint (`mas-691e9159-endpoint`)
- ✅ Provides a beautiful chat interface
- ✅ Includes 6 pre-configured customer service questions
- ✅ Ready to deploy to Databricks Apps

---

## 📦 Files Overview

| File | Purpose |
|------|---------|
| `app.py` | Main application |
| `ClearScoreChatbot.py` | Chat UI component |
| `model_serving_utils.py` | Endpoint connection utilities |
| `app.yaml` | Databricks Apps configuration |
| `requirements.txt` | Python dependencies |
| `deploy.sh` | **One-click deployment script** ⭐ |
| `README.md` | Complete documentation |
| `DEPLOYMENT_GUIDE.md` | Detailed deployment steps |
| `ai_functions_example.py` | Advanced AI features (optional) |

---

## 🎯 Deploy in 3 Steps

### Step 1: Install Databricks CLI
```bash
pip install databricks-cli
```

### Step 2: Configure Authentication
```bash
databricks configure --token
```
Enter your workspace URL and token when prompted.

### Step 3: Deploy! 🚀
```bash
cd /Users/som.natarajan/fraud-case-management/clearscore-chatbot
./deploy.sh
```

That's it! The script will:
- ✅ Create the app
- ✅ Deploy all files
- ✅ Give you the app URL

---

## 🖥️ Local Testing (Optional)

Want to test locally first?

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SERVING_ENDPOINT=mas-691e9159-endpoint
export DATABRICKS_HOST=https://e2-demo-field-eng.cloud.databricks.com
export DATABRICKS_TOKEN=your_token_here

# Run locally
python app.py

# Open http://localhost:8000
```

---

## 🎨 What It Looks Like

```
┌─────────────────────────────────────────────────┐
│  💬 ClearScore Customer Service AI Agent        │
│  Powered by Databricks AI                       │
├─────────────────────────────────────────────────┤
│  💡 Common Customer Questions:                  │
│  [How do I check my score?] [Improve score]    │
│  [Why score changed?] [Update details]         │
├─────────────────────────────────────────────────┤
│  Chat History:                                  │
│                                                 │
│  👤 User: How do I check my credit score?      │
│                                                 │
│  🤖 Agent: You can check your credit score...  │
│                                                 │
├─────────────────────────────────────────────────┤
│  [Type your message here...] [Send] [Clear]    │
└─────────────────────────────────────────────────┘
```

---

## 💡 Suggested Questions Include:

1. "How do I check my credit score?"
2. "How can I improve my credit score?"
3. "Why has my score changed?"
4. "How do I update my personal details?"
5. "What credit products are available?"
6. "How do I close my account?"

---

## 🔧 Quick Customization

### Change Suggested Questions
Edit `ClearScoreChatbot.py` around line 23-31

### Change Colors
Edit `ClearScoreChatbot.py` in the `_add_custom_css()` method

### Change Endpoint
Edit `app.yaml` line 7

---

## 📚 Need More Help?

- **Quick Reference**: This file
- **Complete Docs**: `README.md`
- **Step-by-Step**: `DEPLOYMENT_GUIDE.md`
- **Project Overview**: `PROJECT_SUMMARY.md`
- **Advanced Features**: `ai_functions_example.py`

---

## 🎉 Ready to Deploy?

Run this single command:

```bash
./deploy.sh
```

The script will guide you through everything!

---

## 🆘 Troubleshooting

### "Databricks CLI not found"
```bash
pip install databricks-cli
```

### "Permission denied on deploy.sh"
```bash
chmod +x deploy.sh
```

### "Endpoint not found"
Verify your endpoint name in Databricks workspace under **Serving**

### "Can't connect to endpoint"
Ensure you have `CAN_QUERY` permission on the endpoint

---

## ✨ What's Next?

After deployment:

1. ✅ **Test it**: Try all suggested questions
2. 🎨 **Customize it**: Adjust colors and questions
3. 📊 **Monitor it**: Check logs with `databricks apps logs`
4. 🚀 **Enhance it**: Add AI functions from examples
5. 🔗 **Share it**: Give the URL to your team

---

**🚀 Let's deploy your ClearScore chatbot!**

```bash
./deploy.sh
```

---

*Questions? Check README.md or DEPLOYMENT_GUIDE.md*
