# GitHub Actions Workflows

This directory contains GitHub Actions workflows that automate testing, building, and deployment for the backend_ii_project.

## Available Workflows

### CI (Continuous Integration)

**File:** [ci.yml](./workflows/ci.yml)

This workflow runs tests and linting on the codebase to ensure quality.

**Triggers:**
- Push to `main` or `dev` branches
- Pull requests to `main` or `dev` branches

**Jobs:**
- `test`: Runs pytest with a PostgreSQL service container
- `lint`: Runs flake8, black, and isort for code quality checks

### Docker Build

**File:** [docker-build.yml](./workflows/docker-build.yml)

This workflow builds and pushes Docker images to GitHub Container Registry.

**Triggers:**
- Push to `main` or `dev` branches
- Push of version tags (e.g., `v1.0.0`)
- Pull requests to `main` or `dev` branches

**Jobs:**
- `build`: Builds and optionally pushes the Docker image

### Deploy

**File:** [deploy.yml](./workflows/deploy.yml)

This workflow handles deployment to servers via SSH.

**Triggers:**
- GitHub Release creation
- Manual trigger (workflow_dispatch) with environment selection

**Jobs:**
- `deploy`: Deploys the application to the server via SSH

## Required Secrets

For these workflows to function properly, you need to set up the following secrets in your GitHub repository:

### For Docker Build:
- No additional secrets required (uses `GITHUB_TOKEN` automatically)

### For Deployment:
- `SSH_PRIVATE_KEY`: SSH private key for connecting to the deployment server
- `SERVER_HOST`: Hostname or IP address of the deployment server
- `SERVER_USER`: Username for SSH connection
- `DEPLOY_PATH`: Path to the application directory on the server
- `SLACK_WEBHOOK` (optional): Webhook URL for Slack notifications

## Customizing Workflows

To customize these workflows:

1. Edit the corresponding YAML file in the `.github/workflows/` directory
2. Commit and push your changes
3. The updated workflow will be used for all future runs

## Manually Running Workflows

1. Go to the Actions tab in your GitHub repository
2. Select the workflow you want to run
3. Click "Run workflow"
4. Select the branch and provide any required inputs
5. Click "Run workflow" to start the execution

## Viewing Workflow Results

Visit the Actions tab in your GitHub repository to see the status and logs of workflow runs.