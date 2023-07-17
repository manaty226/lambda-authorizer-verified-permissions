resource "aws_cognito_user_pool" "this" {
  name = "blog-app"
}

resource "aws_cognito_user_pool_client" "blog-app" {
  name = "app-client"

  user_pool_id = aws_cognito_user_pool.this.id
  explicit_auth_flows = ["ALLOW_USER_PASSWORD_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"]
}