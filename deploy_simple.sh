#!/bin/bash

# ClearScore Chatbot - Simple Deployment Script
# This uses the Databricks Asset Bundles approach

set -e

echo "🚀 ClearScore Customer Service Chatbot - Simple Deployment"
echo "============================================================"
echo ""

APP_NAME="clearscore-customer-service"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check Databricks CLI
if ! command -v databricks &> /dev/null; then
    print_error "Databricks CLI not found"
    echo "Install with: pip install databricks-cli"
    exit 1
fi

print_success "Databricks CLI found"

echo ""
echo "📦 Creating app bundle..."

# Create a zip file with all source code
BUNDLE_NAME="clearscore-app-bundle.zip"
zip -r $BUNDLE_NAME app.py ClearScoreChatbot.py model_serving_utils.py app.yml requirements.txt

print_success "Bundle created: $BUNDLE_NAME"

echo ""
echo "🔍 Checking if app exists..."

if databricks apps get $APP_NAME &> /dev/null; then
    print_warning "App '$APP_NAME' already exists"
    echo ""
    echo "To update the app, use the Databricks UI:"
    echo "1. Go to your Databricks workspace"
    echo "2. Navigate to Apps"
    echo "3. Find '$APP_NAME'"
    echo "4. Click 'Update' and upload the bundle: $BUNDLE_NAME"
    echo ""
else
    echo ""
    echo "📦 Creating new app..."
    databricks apps create $APP_NAME
    print_success "App created!"
    echo ""
    echo "To complete deployment:"
    echo "1. Go to your Databricks workspace"
    echo "2. Navigate to Apps"
    echo "3. Find '$APP_NAME'"
    echo "4. Upload the source bundle: $BUNDLE_NAME"
fi

echo ""
echo "============================================================"
echo "Bundle ready: $BUNDLE_NAME"
echo ""
echo "Next steps:"
echo "1. Go to: https://e2-demo-field-eng.cloud.databricks.com"
echo "2. Click on 'Apps' in the left sidebar"
echo "3. Find '$APP_NAME'"
echo "4. Upload or drag-and-drop: $BUNDLE_NAME"
echo "============================================================"
echo ""

print_success "Done! 🎉"

