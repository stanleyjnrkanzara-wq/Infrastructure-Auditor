#Architecture Overview

##System Diagram


![alt text](<WhatsApp Image 2026-07-07 at 22.26.26.jpeg>)

## Security Considerations

### IAM Permissions (Least Privilege)
- Lambda role only has READ permissions on EC2 and CloudWatch
- Lambda can WRITE to SNS and INVOKE Bedrock
- No admin or delete permissions

### Data Handling
- Metric data is ephemeral (not stored)
- Prompt is not logged
- Report is only sent to authorized SNS subscribers

### Bedrock
- Uses Haiku model (cost-effective)
- No fine-tuning or model training
- Default region: us-east-1

## Costs

### Monthly Breakdown
| Component | Invocations | Unit Cost | Total |
|-----------|-------------|-----------|-------|
| Lambda | 30 | ~$0.0000002 per second | $0.30 |
| CloudWatch | 30 queries | ~$0.01 per 1M | $0.00 |
| Bedrock | 30 × 1,500 tokens | $0.25/$1.25 per 1M | $0.01 |
| SNS | 30 emails | $0 (free tier) | $0.00 |
| EventBridge | 1 rule | $0 (free tier) | $0.00 |
| **Total** | | | **~$0.31** |

**Note**: Covered by free tier and AWS credits

## Scaling Considerations

### Horizontal Scaling
- Lambda automatically scales (concurrent executions)
- No database connections to manage
- SNS can handle high email volumes

### Vertical Scaling
- Increase Lambda memory if processing large numbers of instances (>100)
- Increase timeout if using larger models (currently Haiku = fast)

### Cost at Scale
- 100 instances, 10x daily audits = $3-5/month
- 1,000 instances, 100x daily audits = $30-50/month
- Always within free tier + minimal paid costs

## Monitoring & Observability

### CloudWatch Logs
- All Lambda execution logs captured
- Filter by timestamp, error level, execution ID

### CloudWatch Metrics
- Invocation count
- Duration
- Errors
- Concurrent executions

### Manual Testing
- Use Lambda Test button in console
- View real-time logs
- Verify email delivery

## Next Steps

1. **Terraform IaC**: Replicate in code for reproducibility
2. **GitHub Actions CI/CD**: Automated deployments
3. **Slack Integration**: Real-time alerts instead of emails
4. **Cost Anomaly Detection**: Alert on unusual AWS costs
5. **Historical Reporting**: Store reports in S3 for trend analysis