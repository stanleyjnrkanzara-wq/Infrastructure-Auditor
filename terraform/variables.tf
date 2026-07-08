variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "email_address" {
  description = "Email address for SNS notifications"
  type        = string
  sensitive   = true
}

variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 60
}

variable "lambda_memory" {
  description = "Lambda function memory in MB"
  type        = number
  default     = 256
}

variable "schedule_expression" {
  description = "EventBridge cron expression for daily audit"
  type        = string
  default     = "cron(0 8 * * ? *)"  # 8 AM UTC daily
}