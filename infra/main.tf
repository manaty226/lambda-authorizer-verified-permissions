provider "aws" {
  region = "ap-northeast-1"
}

variable "policy_id" {
  type = string
}

module "lambda" {
  source = "./modules/lambda"
  policy_id = var.policy_id
}

module "api" {
  source = "./modules/api"
  authorizer_invoke_arn = module.lambda.authorizer_invoke_arn
}

module "cognito" {
  source = "./modules/cognito"
}