#!/bin/bash
# Deploy TapFlow to cloud services

set -e

echo "Deploying TapFlow..."

# Check for required environment variables
if [ -z "$RENDER_DEPLOY_HOOK_URL" ]; then
    echo "Warning: RENDER_DEPLOY_HOOK_URL not set, skipping API deployment"
else
    echo "Triggering API deployment to Render..."
    curl -X POST "$RENDER_DEPLOY_HOOK_URL"
fi

echo ""
echo "Deployment triggered!"
echo "Check the respective dashboards for deployment status:"
echo "  - Render: https://dashboard.render.com"
echo "  - Vercel: https://vercel.com/dashboard"
