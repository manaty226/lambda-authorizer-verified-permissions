variable "policy_id" {
  type = string  
}

data "aws_caller_identity" "me" {}

data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "../lambda/authorizer"
  output_path = "./modules/lambda/authorizer.zip"
}

data "archive_file" "layer_zip" {
  type        = "zip"
  source_dir  = "../lambda/boto3_layer"
  output_path = "./modules/lambda/layer.zip"
}

resource "aws_lambda_layer_version" "boto3" {
  filename   = "${data.archive_file.layer_zip.output_path}"
  layer_name = "boto3"
  source_code_hash = "${data.archive_file.layer_zip.output_base64sha256}"
  compatible_runtimes = ["python3.9"]
}

resource "aws_lambda_function" "authorizer" {
  filename      = "${data.archive_file.function_zip.output_path}"
  function_name = "api_gateway_authorizer"
  role          = aws_iam_role.lambda.arn
  handler       = "src.index.lambda_handler"
  runtime       = "python3.9"
  timeout       = 20
  source_code_hash = "${data.archive_file.function_zip.output_base64sha256}"

  environment {
    variables = {
      POLICY_ID = var.policy_id
    }
  }
  
  layers = [aws_lambda_layer_version.boto3.arn]
  
}

resource "aws_iam_role" "lambda" {
  name = "lambda-authorizer-role"
  
  managed_policy_arns = ["arn:aws:iam::aws:policy/AWSLambdaExecute"]

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

resource "aws_iam_role_policy" "verified_permissions_policy" {
  name = "access_verified_permissions"
  role = aws_iam_role.lambda.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
		{
			"Effect": "Allow",
			"Action": "verifiedpermissions:IsAuthorizedWithToken",
			"Resource": "arn:aws:verifiedpermissions::${data.aws_caller_identity.me.account_id}:policy-store/*"
		}
  ]
}
EOF
}

output "authorizer_invoke_arn" { value = aws_lambda_function.authorizer.invoke_arn }