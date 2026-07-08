terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  # Optional: Use S3 backend for state management (production)
  # backend "s3" {
  #   bucket         = "your-terraform-state-bucket"
  #   key            = "infrastructure-auditor/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  # }
}

provider "aws" {
  region = var.aws_region
}

# ============================================================
# IAM ROLE FOR LAMBDA
# ============================================================

resource "aws_iam_role" "lambda_role" {
  name               = "lambda-infrastructure-auditor-role-${var.environment}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "lambda-infrastructure-auditor-role"
  }
}

# Attach managed policies
resource "aws_iam_role_policy_attachment" "lambda_ec2_read" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_cloudwatch_read" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_bedrock" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockFullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_sns" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSNSFullAccess"
}

# ============================================================
# LAMBDA FUNCTION
# ============================================================

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda-code/lambda_function.py"
  output_path = "${path.module}/lambda_function.zip"
}

resource "aws_lambda_function" "auditor" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "infrastructure-auditor-${var.environment}"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.11"
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.audit_reports.arn
      ENVIRONMENT   = var.environment
    }
  }

  tags = {
    Name = "infrastructure-auditor"
  }
}

# ============================================================
# SNS TOPIC FOR NOTIFICATIONS
# ============================================================

resource "aws_sns_topic" "audit_reports" {
  name              = "infrastructure-audit-reports-${var.environment}"
  display_name      = "Daily Infrastructure Audit Reports"
  kms_master_key_id = "alias/aws/sns"

  tags = {
    Name = "infrastructure-audit-reports"
  }
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.audit_reports.arn
  protocol  = "email"
  endpoint  = var.email_address
}

# ============================================================
# EVENTBRIDGE SCHEDULE
# ============================================================

resource "aws_cloudwatch_event_rule" "daily_audit" {
  name                = "daily-infrastructure-audit-${var.environment}"
  description         = "Trigger infrastructure audit daily at 8 AM UTC"
  schedule_expression = var.schedule_expression
  is_enabled          = true

  tags = {
    Name = "daily-infrastructure-audit"
  }
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.daily_audit.name
  target_id = "InfrastructureAuditorLambda"
  arn       = aws_lambda_function.auditor.arn

  # Optional: Add input transformation
  input_transformer {
    input_paths = {
      time = "$.time"
    }
    input_template = jsonencode({
      source      = "eventbridge"
      trigger_time = "<time>"
    })
  }
}

# Grant EventBridge permission to invoke Lambda
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.auditor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_audit.arn
}

# ============================================================
# CLOUDWATCH LOG GROUP FOR LAMBDA
# ============================================================

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/infrastructure-auditor-${var.environment}"
  retention_in_days = 7

  tags = {
    Name = "infrastructure-auditor-logs"
  }
}

# ============================================================
# CLOUDWATCH ALARMS
# ============================================================

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "infrastructure-auditor-errors-${var.environment}"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Alert when Lambda function has errors"
  alarm_actions       = [aws_sns_topic.audit_reports.arn]

  dimensions = {
    FunctionName = aws_lambda_function.auditor.function_name
  }
}

resource "aws_cloudwatch_metric_alarm" "lambda_duration" {
  alarm_name          = "infrastructure-auditor-duration-${var.environment}"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Average"
  threshold           = 30000  # 30 seconds
  alarm_description   = "Alert when Lambda execution duration is too high"
  alarm_actions       = [aws_sns_topic.audit_reports.arn]

  dimensions = {
    FunctionName = aws_lambda_function.auditor.function_name
  }
}