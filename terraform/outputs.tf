output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.auditor.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.auditor.arn
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic for notifications"
  value       = aws_sns_topic.audit_reports.arn
}

output "sns_topic_name" {
  description = "Name of the SNS topic"
  value       = aws_sns_topic.audit_reports.name
}

output "eventbridge_rule_name" {
  description = "Name of the EventBridge rule"
  value       = aws_cloudwatch_event_rule.daily_audit.name
}

output "eventbridge_rule_arn" {
  description = "ARN of the EventBridge rule"
  value       = aws_cloudwatch_event_rule.daily_audit.arn
}

output "log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}

output "deployment_summary" {
  description = "Summary of deployed resources"
  value = {
    lambda_function    = aws_lambda_function.auditor.function_name
    sns_topic          = aws_sns_topic.audit_reports.name
    scheduler          = aws_cloudwatch_event_rule.daily_audit.name
    logs               = aws_cloudwatch_log_group.lambda_logs.name
    environment        = var.environment
    region             = var.aws_region
  }
}