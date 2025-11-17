#!/bin/bash
# Auto-deploy ClearScore Chatbot to Databricks Apps
# This script syncs code and automatically deploys the app
# Usage: ./deploy.sh

set -e  # Exit on error

# Configuration
APP_NAME="clearscore-customer-service"
WORKSPACE_PATH="/Workspace/clearscore-chatbot-app"

echo "🚀 Starting auto-deployment to Databricks Apps..."
echo "   📱 App Name: $APP_NAME"
echo "   📂 Workspace Path: $WORKSPACE_PATH"
echo ""

# Check if databricks CLI is installed
if ! command -v databricks &> /dev/null; then
    echo "❌ Error: Databricks CLI not found. Please install it first:"
    echo "   pip install databricks-cli"
    exit 1
fi

# Check if databricks CLI is configured
if ! databricks workspace list / &> /dev/null; then
    echo "❌ Error: Databricks CLI not configured. Please run:"
    echo "   databricks configure --token"
    exit 1
fi

# Step 1: Prepare deployment directory (exclude unnecessary files)
echo ""
echo "📦 Step 1/3: Preparing deployment package..."
DEPLOY_DIR=".deploy-tmp"
rm -rf "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR"

# Copy only the necessary files
cp app.py "$DEPLOY_DIR/"
cp ClearScoreChatbot.py "$DEPLOY_DIR/"
cp model_serving_utils.py "$DEPLOY_DIR/"
cp app.yml "$DEPLOY_DIR/"
cp requirements.txt "$DEPLOY_DIR/"

echo "✅ Deployment package prepared"

# Step 2: Sync code to workspace
echo ""
echo "📤 Step 2/3: Syncing code to Databricks workspace..."
databricks workspace mkdirs "$WORKSPACE_PATH" || true
databricks workspace import-dir "$DEPLOY_DIR" "$WORKSPACE_PATH" --overwrite

# Cleanup
rm -rf "$DEPLOY_DIR"
echo "✅ Code synced to workspace: $WORKSPACE_PATH"

# Step 3: Deploy the app
echo ""
echo "🚀 Step 3/3: Deploying app to Databricks Apps..."
databricks apps deploy "$APP_NAME" \
    --source-code-path "$WORKSPACE_PATH"

echo ""
echo "⏳ Waiting for deployment to complete..."
sleep 15

# Check deployment status
for i in {1..20}; do
    STATUS=$(databricks apps get "$APP_NAME" --output json 2>/dev/null | jq -r '.app_status.state' 2>/dev/null || echo "UNKNOWN")
    echo "   Status check $i/20: $STATUS"
    
    if [ "$STATUS" = "RUNNING" ]; then
        echo ""
        echo "✅ Deployment successful! App is running."
        
        # Get app URL
        APP_URL=$(databricks apps get "$APP_NAME" --output json 2>/dev/null | jq -r '.url' 2>/dev/null || echo "")
        if [ -n "$APP_URL" ]; then
            echo "🌐 App URL: $APP_URL"
        fi
        
        exit 0
    elif [ "$STATUS" = "FAILED" ] || [ "$STATUS" = "ERROR" ]; then
        echo ""
        echo "❌ Deployment failed! Checking logs..."
        databricks apps logs "$APP_NAME" --tail 50
        exit 1
    fi
    
    sleep 10
done

echo ""
echo "⚠️  Deployment is taking longer than expected. Check status with:"
echo "   databricks apps get $APP_NAME"
echo "   databricks apps logs $APP_NAME"
