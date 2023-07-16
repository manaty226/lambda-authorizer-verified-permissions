variable "policy_id" {
  type = string  
}

data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "../lambda/authorizer"
  output_path = "./modules/lambda/authorizer.zip"
}

resource "aws_lambda_function" "authorizer" {
  filename      = "${data.archive_file.function_zip.output_path}"
  function_name = "api_gateway_authorizer"
  role          = aws_iam_role.lambda.arn
  handler       = "src.index.lambda_handler"
  runtime       = "python3.7"
  timeout       = 20
  source_code_hash = "${data.archive_file.function_zip.output_base64sha256}"

  environment {
    variables = {
      POLICY_ID = var.policy_id
    }
  }

  layers = ["${aws_lambda_layer_version.authzed.arn}"]

  
  vpc_config {
    subnet_ids = [var.subnet_id]
    security_group_ids = [var.security_group_id]
  }
}

resource "aws_iam_role" "lambda" {
  name = "demo-lambda"
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"]
  
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action":
        "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "acm_policy" {
  name = "default"
  role = aws_iam_role.lambda.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "acm:GetCertificate",
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

output "authorizer_invoke_arn" { value = aws_lambda_function.authorizer.invoke_arn }