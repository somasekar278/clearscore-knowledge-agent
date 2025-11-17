#!/bin/bash

# ClearScore Chatbot - Local Development Script
# This script runs the chatbot locally for testing

echo "🚀 Starting ClearScore Customer Service Chatbot (Local)"
echo "========================================================="
echo ""

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export SERVING_ENDPOINT=ka-6859840b-endpoint
export DATABRICKS_HOST=https://e2-demo-field-eng.cloud.databricks.com
export DATABRICKS_TOKEN=your_databricks_token_here  # Replace with your token

echo "✅ Environment configured"
echo "   Endpoint: $SERVING_ENDPOINT"
echo "   Host: $DATABRICKS_HOST"
echo ""
echo "📱 Starting app on http://localhost:8000"
echo "   Press Ctrl+C to stop"
echo ""

# Run the app
python app.py

