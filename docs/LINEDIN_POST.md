# LinkedIn Post Template

## Version 1: Technical Deep Dive

---

🚀 **I Just Built an AI-Powered Cloud Auditor That Saves Money & Catches Security Risks**

Here's what bothers me: engineering teams waste thousands on oversized EC2 instances, and security groups accidentally left open to the entire internet (0.0.0.0/0). Junior engineers find these manually. Senior engineers automate detection.

**So I built the infrastructure audit system I'd want at any company I work for.**

## What It Does

Every morning at 8 AM, my system:
1. ✅ Scans all EC2 instances and pulls 7-day CPU utilization data
2. 🔒 Analyzes security groups for overly permissive rules
3. 🤖 Sends findings to Claude 3 Haiku (via Amazon Bedrock)
4. 📊 Generates an executive-ready report with specific recommendations
5. 📧 Emails the team

Instead of raw data, the report says:
> "Instance i-09f1234 has averaged 1.2% CPU. Downsize from t3.medium to t3.micro. Save $300/year."

## The Tech Stack

**AWS**: Lambda, EventBridge, CloudWatch, EC2, Bedrock, SNS
**IaC**: Terraform (fully reproducible)
**CI/CD**: GitHub Actions (auto-deploy on push)
**Language**: Python 3.11 + Boto3

## Why This Stands Out

✅ **Solves a Real Business Problem**: Lost AWS spend costs companies millions. This catches it automatically.

✅ **Practical AI**: Not building another chatbot. Using Claude to analyze structured infrastructure data and generate actionable intelligence.

✅ **Production-Ready**:
   - Error handling & logging
   - Automated scheduling
   - Infrastructure-as-Code
   - CI/CD pipeline
   - Monitoring & alerts

✅ **Fully Serverless**: ~$2/month to run. Scales automatically.

## The Numbers

| Metric | Value |
|--------|-------|
| Deployment Time | 30 minutes (Terraform) |
| Monthly Cost | ~$2 (covered by free tier) |
| Code Lines | 300 (Lambda) + 250 (Terraform) |
| Potential Savings | $300-1,000/month per company |

## What This Taught Me

**Cloud Governance**: Cost optimization + security compliance aren't bolt-ons. They're core engineering challenges.

**Generative AI**: Claude works best with context. Raw data = generic advice. Structured data + context = specific, actionable insights.

**Serverless Architecture**: This system runs 365 days/year with zero operational overhead.

## Next Steps

I'm exploring:
- Real-time Slack alerts instead of daily emails
- Automated remediation (downsize instances automatically)
- Cost forecasting + anomaly detection
- Multi-account AWS scanning

**GitHub Repo**: [infrastructure-auditor](https://github.com/stanleyjnrkanzara-wq/infrastructure-auditor)

---

**If you're hiring engineers who think about infrastructure beyond "it works," let's talk.** 

#AWS #CloudEngineering #Terraform #Bedrock #ServerlessArchitecture #Infrastructure #DevOps #Python

---

## Version 2: Storytelling Angle

---

💭 **I spent an hour manually reviewing CloudWatch dashboards. Then I built a system that does it in 30 seconds.**

The scene: Sprint planning, and someone mentions AWS costs are higher than expected. Nobody knows why. Everyone assumes it's normal.

Here's what's actually happening:
- ❌ Dev server running t3.medium with 2% CPU usage = $25/month waste
- ❌ Production security group accidentally exposed to 0.0.0.0/0 = security incident waiting to happen
- ❌ RDS instance over-provisioned = $500+/month we don't need

Most teams catch these issues in spreadsheet reviews (annual). By then, they've wasted thousands.

## The Solution I Built

An **AI-powered auditor** that runs daily, analyzes your cloud infrastructure, and emails the team actionable findings in minutes.

**Architecture**:
- Lambda function (triggered daily via EventBridge)
- Collects EC2 + CloudWatch + Security Group data
- Sends to Claude 3 Haiku for analysis
- Delivers report via SNS

**Sample output**: 
> "🚨 SECURITY RISK: Security group sg-9234 allows TCP 22 from 0.0.0.0/0. Recommendation: Restrict to corporate VPN. Status: CRITICAL."

> "💰 COST OPPORTUNITY: Instance i-0f1234 averages 1.8% CPU. Downsize t3.medium → t3.micro. Save $300/year."

## Why This Matters

✅ **It pays for itself in days** (one avoided security issue or caught waste)

✅ **It's production-grade**:
   - Terraform IaC (reproducible)
   - GitHub Actions CI/CD (automated testing & deployment)
   - Comprehensive error handling & logging
   - CloudWatch monitoring & alarms

✅ **Shows how senior engineers think**: Automate toil, solve problems at scale, build systems not scripts.

## The Outcome

- Deployment time: 30 minutes (Terraform)
- Monthly cost: ~$2
- Team benefit: Hours saved, security risks prevented, costs optimized

This is what **true cloud engineering** looks like.

---

**Repo**: [infrastructure-auditor](https://github.com/stanleynrkanzara-wq/infrastructure-auditor)

#AWS #CloudEngineering #Terraform #AI #Python #DevOps

---

## Version 3: Short & Punchy

---

🏗️ I built an AI auditor that scans your AWS infrastructure daily, finds cost waste + security gaps, and emails the team recommendations.

**Tech**: AWS Lambda + Bedrock + Terraform
**Cost**: $2/month
**Potential Savings**: $300-1,000/month per company

Fully serverless. Fully automated. Fully production-grade.

Now hiring? Let's talk.

[GitHub](https://github.com/stanleyjnrkanzara-wq/infrastructure-auditor)

#AWS #CloudEngineering #Terraform

---