# Infrastructure-Auditor
AI-Powered Cloud Infrastructure Security and Cost Auditor Using AWS Lambda, Bedrock and Terraform with GitHub Actions CI/CD

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0:FF9900,100:232F3E&height=120&section=header&text=%20AI-Powered%20Cloud%20Infrastructure%20Auditor&fontSize=32&fontColor=ffffff&fontAlignY=55" alt="header"/>
</p>

<p align="center"><i>A serverless AWS solution that automatically audits cloud infrastructure for security vulnerabilities and cost inefficiencies, powered by Claude 3 Haiku via Amazon Bedrock.</i></p>

<p align="center">
  <img src="https://img.shields.io/badge/AWS-Lambda-FF9900?logo=amazon-aws&logoColor=white&style=flat"/>
  <img src="https://img.shields.io/badge/AI-Bedrock-CC0000?logo=anthropic&logoColor=white&style=flat"/>
  <img src="https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform&logoColor=white&style=flat"/>
  <img src="https://img.shields.io/badge/Code-Python-3776AB?logo=python&logoColor=white&style=flat"/>
</p>

---

##  What This Does

> **Cost Optimization** — Identifies underutilized EC2 instances and recommends downsizing

> **Security Scanning** — Detects overly permissive security groups (open to 0.0.0.0/0)

> **AI Analysis** — Uses Claude 3 Haiku to generate actionable, executive-ready reports

> **Automated Delivery** — Reports sent daily via Email/Slack

> **Fully Serverless** — Runs on AWS Lambda with EventBridge scheduling

---

## 📊 Quick Stats

<p align="center">

|  Monthly Cost |  Deployment Time |  Languages |  AWS Services |
|:---:|:---:|:---:|:---:|
| ~$1-2 | 2-3 hrs / 30 min | Python, Terraform, YAML | Lambda, Bedrock, EventBridge, SNS, CloudWatch, EC2 |
| *(covered by free tier/credits)* | *(manual / Terraform)* | | |

</p>

---

##  Quick Start

<p align="center">

| |  Manual Setup |  Terraform (Production) |  GitHub Actions |
|:---|:---|:---|:---|
| **Time** | 2-3 hours | 30 minutes | Zero config |
| **Guide** | [SETUP_GUIDE.md](./manual-setup/SETUP_GUIDE.md) | [README.md](./terraform/README.md) | Push to `main` branch — CI/CD pipeline handles everything |

</p>

---

## 📁 Project Structure
