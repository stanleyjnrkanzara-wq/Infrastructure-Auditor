import boto3
import json
import os
from datetime import datetime, timedelta

# Initialize AWS clients
ec2_client = boto3.client('ec2', region_name='us-east-1')
cloudwatch_client = boto3.client('cloudwatch', region_name='us-east-1')
sns_client = boto3.client('sns', region_name='us-east-1')
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    """
    Main Lambda handler: Collect infrastructure data and send to Claude for analysis
    """
    
    try:
        print("🔍 Starting infrastructure audit...")
        
        # Step 1: Collect EC2 and Cost Data
        print("📊 Collecting EC2 data...")
        ec2_data = collect_ec2_data()
        print(f"   Found {len(ec2_data)} running instances")
        
        # Step 2: Collect Security Data
        print("🔒 Collecting security group data...")
        security_data = collect_security_data()
        print(f"   Found {len(security_data)} security issues")
        
        # Step 3: Prepare prompt for Claude
        print("📝 Preparing audit prompt...")
        audit_prompt = prepare_audit_prompt(ec2_data, security_data)
        
        # Step 4: Call Claude via Bedrock
        print("🤖 Calling Claude for analysis...")
        analysis = call_bedrock_claude(audit_prompt)
        
        # Step 5: Send report to SNS (email/Slack)
        print("📧 Sending report via SNS...")
        send_report(analysis, ec2_data, security_data)
        
        print("✅ Audit complete!")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Audit complete and report sent!',
                'instances_scanned': len(ec2_data),
                'security_issues': len(security_data)
            })
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        send_error_notification(str(e))
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }


def collect_ec2_data():
    """
    Collect all running EC2 instances and their CPU utilization
    """
    instances = []
    
    try:
        # Get all running instances
        response = ec2_client.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                launch_time = instance['LaunchTime']
                
                # Get CPU utilization from CloudWatch (last 7 days)
                cpu_metrics = get_cpu_utilization(instance_id)
                
                # Estimate monthly cost (simplified)
                hourly_cost = estimate_hourly_cost(instance_type)
                monthly_cost = hourly_cost * 24 * 30
                
                instances.append({
                    'instance_id': instance_id,
                    'type': instance_type,
                    'launch_time': str(launch_time),
                    'cpu_utilization_7day_avg': cpu_metrics,
                    'estimated_monthly_cost': round(monthly_cost, 2),
                    'tags': instance.get('Tags', [])
                })
        
        print(f"   EC2 Data Collection: Found {len(instances)} instances")
        
    except Exception as e:
        print(f"Error collecting EC2 data: {str(e)}")
    
    return instances


def get_cpu_utilization(instance_id):
    """
    Get average CPU utilization for the last 7 days
    """
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=7)
        
        response = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,  # 1 hour
            Statistics=['Average']
        )
        
        if response['Datapoints']:
            avg_cpu = sum([dp['Average'] for dp in response['Datapoints']]) / len(response['Datapoints'])
            return round(avg_cpu, 2)
        return 0.0
        
    except Exception as e:
        print(f"Error getting CPU metrics for {instance_id}: {str(e)}")
        return 0.0


def estimate_hourly_cost(instance_type):
    """
    Rough estimate of hourly cost by instance type (US-East-1 on-demand)
    This is simplified - real pricing varies by AZ and purchase option
    """
    pricing = {
        't3.micro': 0.0104,
        't3.small': 0.0208,
        't3.medium': 0.0416,
        't3.large': 0.0832,
        't3.xlarge': 0.1664,
        't3.2xlarge': 0.3328,
        'm5.large': 0.096,
        'm5.xlarge': 0.192,
        'm5.2xlarge': 0.384,
        't2.micro': 0.0116,
        't2.small': 0.0232,
        't2.medium': 0.0464,
    }
    return pricing.get(instance_type, 0.05)  # Default estimate if type not found


def collect_security_data():
    """
    Collect all security groups and identify overly permissive rules
    """
    security_issues = []
    
    try:
        response = ec2_client.describe_security_groups()
        
        for sg in response['SecurityGroups']:
            sg_id = sg['GroupId']
            sg_name = sg['GroupName']
            vpc_id = sg.get('VpcId', 'default')
            
            # Check inbound rules
            for rule in sg.get('IpPermissions', []):
                # Check for open-to-world rules (0.0.0.0/0)
                for ip_range in rule.get('IpRanges', []):
                    if ip_range.get('CidrIp') == '0.0.0.0/0':
                        from_port = rule.get('FromPort', -1)
                        to_port = rule.get('ToPort', -1)
                        protocol = rule.get('IpProtocol', 'unknown')
                        
                        # Determine severity
                        critical_ports = [22, 3389, 1433, 3306, 5432, 5984, 6379, 9200, 9300, 27017, 27018, 27019, 27020, 50070]
                        if from_port in critical_ports or (from_port <= critical_ports[0] <= to_port if from_port != -1 and to_port != -1 else False):
                            severity = 'CRITICAL'
                        elif from_port in [80, 443]:
                            severity = 'LOW'  # Web traffic open is usually OK
                        else:
                            severity = 'MEDIUM'
                        
                        port_range = f"{from_port}-{to_port}" if from_port != to_port else str(from_port)
                        if from_port == -1:
                            port_range = "All"
                        
                        security_issues.append({
                            'sg_id': sg_id,
                            'sg_name': sg_name,
                            'vpc_id': vpc_id,
                            'issue_type': 'Open to Internet (0.0.0.0/0)',
                            'protocol': protocol,
                            'port_range': port_range,
                            'cidr': ip_range.get('CidrIp'),
                            'severity': severity
                        })
        
        print(f"   Security Data Collection: Found {len(security_issues)} issues")
        
    except Exception as e:
        print(f"Error collecting security data: {str(e)}")
    
    return security_issues


def prepare_audit_prompt(ec2_data, security_data):
    """
    Create a structured prompt for Claude to analyze
    """
    
    ec2_summary = ""
    if ec2_data:
        ec2_summary = "### EC2 INSTANCES & COSTS:\n\n"
        for inst in ec2_data:
            ec2_summary += f"Instance: {inst['instance_id']}\n"
            ec2_summary += f"  Type: {inst['type']}\n"
            ec2_summary += f"  CPU Usage (7-day avg): {inst['cpu_utilization_7day_avg']}%\n"
            ec2_summary += f"  Estimated Monthly Cost: ${inst['estimated_monthly_cost']}\n"
            ec2_summary += f"  Running Since: {inst['launch_time']}\n\n"
    else:
        ec2_summary = "### EC2 INSTANCES:\nNo running instances found.\n"
    
    security_summary = ""
    if security_data:
        security_summary = "### SECURITY ISSUES DETECTED:\n\n"
        for issue in security_data:
            security_summary += f"Security Group: {issue['sg_id']} ({issue['sg_name']})\n"
            security_summary += f"  Severity: {issue['severity']}\n"
            security_summary += f"  Protocol: {issue['protocol']}\n"
            security_summary += f"  Port(s): {issue['port_range']}\n"
            security_summary += f"  Open to: {issue['cidr']}\n"
            security_summary += f"  Issue: {issue['issue_type']}\n\n"
    else:
        security_summary = "### SECURITY ISSUES:\nNo overly permissive security groups detected (good job!).\n"
    
    prompt = f"""You are a Senior Cloud Infrastructure Auditor. Analyze the following AWS infrastructure audit data and provide professional, actionable recommendations.

{ec2_summary}

{security_summary}

## YOUR ANALYSIS TASK:

1. **Cost Optimization**: Identify instances with low CPU utilization (< 5%) and recommend downsizing. Calculate potential savings.

2. **Security Risks**: For any findings, assess the actual business impact and recommend immediate remediation.

3. **Executive Summary**: Provide a brief, high-impact summary suitable for a CTO or engineering leader.

4. **Action Items**: List specific, implementable recommendations with priority levels (CRITICAL, HIGH, MEDIUM, LOW).

Format your response as a professional audit report with clear sections. Be concise but thorough. Use metrics and specific numbers where possible.

Example format:
---
⚠️  INFRASTRUCTURE AUDIT REPORT - {datetime.now().strftime('%Y-%m-%d')}

📊 COST OPTIMIZATION FINDINGS:
[Your findings here]

🔒 SECURITY FINDINGS:
[Your findings here]

✅ RECOMMENDATIONS:
[Your recommendations here]

💰 POTENTIAL MONTHLY SAVINGS:
$[Amount]
---

Now generate the report based on the data above."""

    return prompt


def call_bedrock_claude(prompt):
    """
    Call Claude 3 Haiku via Amazon Bedrock
    """
    try:
        # Using Claude 3 Haiku (most cost-effective for this use case)
        model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        
        message = bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-06-01",
                "max_tokens": 1024,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )
        
        # Parse response
        response_body = json.loads(message['body'].read())
        
        # Extract text from response
        if 'content' in response_body and len(response_body['content']) > 0:
            analysis = response_body['content'][0]['text']
        else:
            analysis = "Error: No response from Claude"
        
        return analysis
        
    except Exception as e:
        print(f"Error calling Bedrock: {str(e)}")
        return f"Error analyzing infrastructure: {str(e)}"


def send_report(analysis, ec2_data, security_data):
    """
    Send the analysis via SNS (Email)
    """
    try:
        # Get SNS topic ARN from environment variable
        topic_arn = os.environ.get('SNS_TOPIC_ARN')
        
        if not topic_arn:
            print("Error: SNS_TOPIC_ARN environment variable not set")
            return
        
        message_body = f"""
═════════════════════════════════════════════════════════════
    DAILY INFRASTRUCTURE AUDIT REPORT
═════════════════════════════════════════════════════════════

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

Instances Scanned: {len(ec2_data)}
Security Issues Found: {len(security_data)}

─────────────────────────────────────────────────────────────

{analysis}

─────────────────────────────────────────────────────────────

This report was automatically generated by the 
AI Infrastructure Auditor running on AWS Lambda.

Next audit scheduled for: Tomorrow at 8:00 AM UTC
═════════════════════════════════════════════════════════════
"""
        
        sns_client.publish(
            TopicArn=topic_arn,
            Subject='[AWS AUDIT] Daily Infrastructure Report - ' + datetime.now().strftime('%Y-%m-%d'),
            Message=message_body
        )
        
        print("✅ Report sent successfully via SNS")
        
    except Exception as e:
        print(f"Error sending report: {str(e)}")


def send_error_notification(error_msg):
    """
    Send error notification if audit fails
    """
    try:
        topic_arn = os.environ.get('SNS_TOPIC_ARN')
        
        if not topic_arn:
            print("Error: SNS_TOPIC_ARN environment variable not set")
            return
        
        sns_client.publish(
            TopicArn=topic_arn,
            Subject='[AWS AUDIT ERROR] Infrastructure Audit Failed - ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            Message=f"""
Infrastructure audit encountered an error:

{error_msg}

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

Please check the Lambda logs for more details.
"""
        )
    except Exception as e:
        print(f"Could not send error notification: {str(e)}")