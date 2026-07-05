# Infrastructure-Auditor
AI-Powered Cloud Infrastructure Security and Cost Auditor Using AWS Lambda, Bedrock and Terraform with GitHub Actions CI/CD

# 🏗️ AI-Powered Cloud Infrastructure Auditor

A serverless AWS solution that automatically audits cloud infrastructure for security vulnerabilities and cost inefficiencies, powered by Claude 3 Haiku via Amazon Bedrock.

## 🎯 What This Does

- **Cost Optimization**: Identifies underutilized EC2 instances and recommends downsizing
- **Security Scanning**: Detects overly permissive security groups (open to 0.0.0.0/0)
- **AI Analysis**: Uses Claude 3 Haiku to generate actionable, executive-ready reports
- **Automated Delivery**: Reports sent daily via Email/Slack
- **Fully Serverless**: Runs on AWS Lambda with EventBridge scheduling

## 📊 Quick Stats

- **Monthly Cost**: ~$1-2 (covered by free tier/credits)
- **Deployment Time**: 2-3 hours (manual) or 30 minutes (Terraform)
- **Languages**: Python, Terraform, YAML
- **AWS Services**: Lambda, Bedrock, EventBridge, SNS, CloudWatch, EC2

## 🚀 Quick Start

### Option 1: Manual Setup
See [manual-setup/SETUP_GUIDE.md](./manual-setup/SETUP_GUIDE.md)

### Option 2: Terraform (Production)
See [terraform/README.md](./terraform/README.md)

### Option 3: Automated with GitHub Actions
Push to `main` branch - CI/CD pipeline handles everything

## 📁 Project Structure
