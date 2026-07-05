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


infrastructure-auditor/
├── manual-setup/              # Step-by-step AWS Console setup guide
│   ├── SETUP_GUIDE.md        # Detailed manual setup instructions
│   └── screenshots/          # Screenshots from manual setup (22+ images)
│
├── terraform/                # Infrastructure-as-Code deployment
│   ├── main.tf              # AWS resource definitions
│   ├── variables.tf         # Input variables
│   ├── outputs.tf           # Output values
│   ├── terraform.tfvars     # Example variable values
│   └── README.md            # Terraform deployment guide
│
├── .github/
│   └── workflows/           # GitHub Actions CI/CD
│       └── deploy.yml       # Automated test & deploy pipeline
│
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md      # System design & architecture overview
│   ├── CI_CD.md            # GitHub Actions pipeline documentation
│   └── INTERVIEW_GUIDE.md  # Talking points for recruiters
│
├── lambda-code/             # Python Lambda function
│   └── lambda_function.py  # Main audit script
│
├── tests/                   # Unit tests
│   └── test_lambda_function.py
│
├── README.md               # This file
└── .gitignore             # Git ignore file

##  Tech Stack

- **Cloud Platform**: AWS
- **Compute**: Lambda (Serverless)
- **AI**: Amazon Bedrock (Claude 3 Haiku)
- **Scheduling**: EventBridge
- **Notifications**: SNS
- **Infrastructure as Code**: Terraform
- **CI/CD**: GitHub Actions
- **Language**: Python 3.11

##  Full Documentation

- [Architecture Overview](./docs/ARCHITECTURE.md)
- [Manual Setup Guide](./manual-setup/SETUP_GUIDE.md)
- [Terraform Deployment](./terraform/README.md)
- [CI/CD Pipeline](./docs/CI_CD.md)
- [Interview Talking Points](./docs/INTERVIEW_GUIDE.md)

##  Cost Breakdown

| Service | Monthly | Notes |
|---------|---------|-------|
| Lambda | $0.00 | Covered by free tier |
| EventBridge | $0.00 | Free tier |
| SNS | $0.00 | Free tier |
| Bedrock (Haiku) | $0.01-0.02 | Minimal tokens |
| **Total** | **~$0.02** | Covered by credits |

##  Screenshots & Proof

All deployment screenshots available in `manual-setup/screenshots/`

##  Learning Outcomes

- AWS Lambda and serverless architecture
- Infrastructure-as-Code with Terraform
- Python with Boto3
- API integration (Bedrock)
- CI/CD pipelines with GitHub Actions
- Cloud security best practices
- Cost optimization strategies

##  How to Use This Repository

1. **Clone**: `git clone https://github.com/YOUR-USERNAME/infrastructure-auditor.git`
2. **Choose deployment method** (Manual, Terraform, or CI/CD automated)
3. **Follow the guide** for your chosen method
4. **Deploy** and verify with test audit
5. **Monitor** in AWS Console
6. **Share** on LinkedIn with this repo link

##  Security Notes

- Never commit AWS credentials to this repo
- Use IAM roles for Lambda (not access keys)
- Security groups created should be restrictive by default
- Review Bedrock model pricing before production use

##  Contributing

This is a learning project. Feel free to:
- Create issues for bugs
- Suggest improvements
- Fork and modify for your use case

##  Interview Talking Points

See [docs/INTERVIEW_GUIDE.md](./docs/INTERVIEW_GUIDE.md) for how to present this to recruiters.

## 📄 License

MIT License - Feel free to use and modify

---

**Built to solve real cloud problems.** 