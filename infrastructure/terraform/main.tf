provider "aws" {
  region = "us-east-1"
}

# ---------------------------------------------------------
# AWS Macie: Automated Sensitive Data Discovery
# ---------------------------------------------------------

resource "aws_macie2_account" "dlp_audit" {
  finding_publishing_frequency = "FIFTEEN_MINUTES"
  status                       = "ENABLED"
}

# Enable Macie to discover sensitive data in S3 buckets
resource "aws_macie2_classification_job" "daily_scan" {
  job_type = "SCHEDULED"
  name     = "Daily-PII-Sweep"
  
  s3_job_definition {
    bucket_definitions {
      account_id = "123456789012"
      buckets    = ["corp-finance-data", "corp-customer-logs"]
    }
  }

  schedule_frequency {
    daily_schedule = true
  }

  # Define what we are looking for (Custom Data Identifiers)
  custom_data_identifier_ids = [
    aws_macie2_custom_data_identifier.employee_id.id
  ]
  
  depends_on = [aws_macie2_account.dlp_audit]
}

# ---------------------------------------------------------
# Custom Regex Pattern for 'Employee ID'
# ---------------------------------------------------------

resource "aws_macie2_custom_data_identifier" "employee_id" {
  name                   = "Corp-Employee-ID"
  regex                  = "EMP-[0-9]{6}"
  description            = "Matches internal Employee IDs (EMP-123456)"
  maximum_match_distance = 50
  keywords               = ["EmployeeID", "WorkerID", "StaffNum"]
}

# ---------------------------------------------------------
# SNS Topic for Alerts (Integration with SOAR/SIEM)
# ---------------------------------------------------------

resource "aws_sns_topic" "dlp_alerts" {
  name = "dlp-critical-alerts"
}

resource "aws_sns_topic_policy" "default" {
  arn = aws_sns_topic.dlp_alerts.arn
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowMaciePublish"
        Effect = "Allow"
        Principal = { Service = "macie.amazonaws.com" }
        Action   = "sns:Publish"
        Resource = aws_sns_topic.dlp_alerts.arn
      }
    ]
  })
}
