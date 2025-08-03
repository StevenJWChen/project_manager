#!/bin/bash

echo "🚀 Pushing Project Manager to GitHub"
echo "====================================="
echo ""
echo "Repository: https://github.com/StevenJWChen/project_manager"
echo ""
echo "⚠️  IMPORTANT: You need a GitHub Personal Access Token"
echo ""
echo "If you don't have one, create it now:"
echo "1. Go to: https://github.com/settings/tokens"
echo "2. Click 'Generate new token (classic)'"
echo "3. Give it a name like 'Project Manager Push'"
echo "4. Select 'repo' scope (full access to repositories)"
echo "5. Click 'Generate token'"
echo "6. COPY the token immediately (you won't see it again!)"
echo ""
echo "When prompted for credentials:"
echo "Username: StevenJWChen"
echo "Password: [Your Personal Access Token - NOT your GitHub password]"
echo ""
read -p "Press Enter when you have your Personal Access Token ready..."
echo ""
echo "Starting push..."
echo ""

# Make sure we're on the main branch
git branch -M main

# Check if repository exists on GitHub first
echo "📡 Checking if repository exists on GitHub..."
curl -s -o /dev/null -w "%{http_code}" https://github.com/StevenJWChen/project_manager > /tmp/repo_check.txt
HTTP_CODE=$(cat /tmp/repo_check.txt)

if [ "$HTTP_CODE" != "200" ]; then
    echo ""
    echo "⚠️  Repository might not exist on GitHub yet!"
    echo ""
    echo "Please create the repository first:"
    echo "1. Go to: https://github.com/new"
    echo "2. Repository name: project_manager"
    echo "3. Make it Public or Private (your choice)"
    echo "4. DO NOT initialize with README, .gitignore, or license"
    echo "5. Click 'Create repository'"
    echo ""
    read -p "Press Enter after creating the repository..."
fi

# Push to GitHub
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Your project has been pushed to GitHub"
    echo ""
    echo "🌐 View your repository at:"
    echo "   https://github.com/StevenJWChen/project_manager"
    echo ""
    echo "📋 What was uploaded:"
    echo "   • Complete project management system"
    echo "   • Batch operations functionality"
    echo "   • Real-time web interface"
    echo "   • Automation demos"
    echo "   • 51 files, 21,793 lines of code"
    echo ""
else
    echo ""
    echo "❌ Push failed. Please check your credentials and try again."
    echo ""
    echo "Troubleshooting:"
    echo "1. Make sure you created the repository on GitHub first"
    echo "2. Use your GitHub username: StevenJWChen"
    echo "3. Use a Personal Access Token as password (not your GitHub password)"
    echo "4. Create token at: https://github.com/settings/tokens"
    echo ""
fi