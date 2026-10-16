import email_validator
from email_validator import EmailNotValidError


def test_validator(data):
  try:
    # Explicitly set check_deliverability=True
    result = email_validator.validate_email(
        data,
        check_deliverability=True,
        allow_smtputf8=True,
        allow_empty_local=False,
    )
    print(f"SUCCESS: Validated email -> {result.normalized}")
  except EmailNotValidError as e:
    print(f"CAUGHT ERROR: {type(e).__name__} -> {e}")


# Test with a fake/non-existent domain
test_validator("sndesdp@xkdd.com")
