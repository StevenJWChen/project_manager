#!/bin/bash

echo "🤖 AUTO-COMMIT: Project Manager"
echo "================================"
echo ""

# Check if there are any changes
if git diff --quiet && git diff --staged --quiet; then
    echo "📝 No changes to commit"
    exit 0
fi

# Show what will be committed
echo "📋 Changes to commit:"
echo ""
git status --porcelain
echo ""

# Add all changes
echo "➕ Adding all changes..."
git add .

# Get current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Create automatic commit message
COMMIT_MSG="Auto-commit: Updates on $TIMESTAMP

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Commit changes
echo "💾 Committing changes..."
git commit -m "$COMMIT_MSG"

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 Pushing to GitHub..."
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ SUCCESS! Changes pushed to GitHub"
        echo "🌐 View at: https://github.com/StevenJWChen/project_manager"
    else
        echo ""
        echo "❌ Push failed"
    fi
else
    echo ""
    echo "❌ Commit failed"
fi