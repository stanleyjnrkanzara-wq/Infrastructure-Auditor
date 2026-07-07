# Manual AWS Setup Guide

This guide walks you through setting up the infrastructure audit system using the AWS Console.

## Prerequisites

- AWS Account with free tier eligibility
- AWS CLI installed and configured
- An email address for notifications

## Timeline

Estimated time: 2-3 hours

## Phases

### Phase 1: Pre-Flight Check (20 minutes)
- [✓] AWS Account verified
- [✓] AWS CLI configured
- [✓] Free tier status checked
- [✓] AWS Credits verified

### Phase 2: Create IAM Role (20 minutes)
- [✓] Lambda execution role created
- [✓] 4 policies attached (EC2, CloudWatch, Bedrock, SNS)

### Phase 3: Create Lambda Function (30 minutes)
- [✓] Function created with Python 3.11
- [✓] Execution role assigned
- [✓] Code deployed

### Phase 4: Create SNS Topic (20 minutes)
- [✓] Topic created
- [✓] Email subscription added and confirmed
- [✓] Topic ARN noted

### Phase 5: Link Lambda to SNS (10 minutes)
- [✓] Environment variable added
- [✓] SNS_TOPIC_ARN configured

### Phase 6: Test Lambda (10 minutes)
- [✓] Manual test executed
- [✓] Email received

### Phase 7: EventBridge Scheduling (15 minutes)
- [✓] Daily schedule created
- [✓] Lambda connected as target

### Phase 8: Verify Logs (10 minutes)
- [✓] CloudWatch logs checked
- [✓] Successful execution verified

## Screenshots Captured

All screenshots should be saved in `/manual-setup/screenshots/`

| Phase | Screenshot # | Description |
|-------|-------------|-------------|
| 1 | 1.0.1 - 1.0.11 | Pre-flight verification |
| 2 | 2.1.1 - 2.7.2 | IAM role creation |
| 3 | 3.1.1 - 3.3.2 | Lambda function creation |
| 4 | 4.1.1 - 4.4.3 | Lambda code deployment |
| 5 | 5.1.1 - 5.7.2 | SNS topic and email setup |
| 6 | 6.1.1 - 6.4.2 | Lambda environment variables |
| 7 | 7.1.1 - 7.4.1 | Manual test and email |
| 8 | 8.1.1 - 8.4.2 | EventBridge schedule creation |
| 9 | 9.1.1 - 9.3.1 | CloudWatch logs verification |

## Cost Summary

| Service | Cost | Notes |
|---------|------|-------|
| Lambda | $0.00 | Free tier: 1M requests/month |
| EventBridge | $0.00 | Free tier: 14 rules |
| SNS | $0.00 | Free tier: 1,000 emails |
| Bedrock (Haiku) | ~$0.02 | 30 invocations × 1,500 tokens = 45k tokens/month |
| **Total** | **$0.02** | Covered by AWS credits |

## Next Steps

1. Monitor CloudWatch logs daily for first week
2. Review email reports for accuracy
3. Proceed to Terraform setup for production deployment
4. Set up GitHub Actions for CI/CD

## Troubleshooting

### Lambda function doesn't execute
- Check CloudWatch logs for errors
- Verify IAM role has correct permissions
- Check environment variable SNS_TOPIC_ARN is set

### No email received
- Check spam folder
- Verify SNS subscription is "Confirmed" status
- Check CloudWatch logs for send errors

### EventBridge not triggering
- Verify schedule is "Enabled"
- Check that Lambda function is specified correctly
- Wait for next scheduled time

## Questions?

Refer to the [Architecture Documentation](../docs/ARCHITECTURE.md)