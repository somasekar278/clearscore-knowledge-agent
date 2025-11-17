#!/bin/bash
# Quick sync script for ClearScore Chatbot
# Commits and pushes changes to GitHub

set -e

echo "🔄 Syncing ClearScore Chatbot to GitHub..."
echo ""

# Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo "📝 Uncommitted changes found. Creating commit..."
    
    # Stage all changes
    git add .
    
    # Get commit message from user or use default
    if [ -z "$1" ]; then
        COMMIT_MSG="Update: $(date '+%Y-%m-%d %H:%M:%S')"
    else
        COMMIT_MSG="$*"
    fi
    
    echo "   Commit message: $COMMIT_MSG"
    git commit -m "$COMMIT_MSG"
    echo "✅ Changes committed"
else
    echo "✅ No uncommitted changes"
fi

# Pull latest changes
echo ""
echo "⬇️  Pulling latest changes from GitHub..."
git pull origin main --rebase || true

# Push to GitHub
echo ""
echo "⬆️  Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Sync complete!"
echo "🌐 Repository: https://github.com/somasekar278/clearscore-knowledge-agent"

