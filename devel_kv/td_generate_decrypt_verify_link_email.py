from email_registration.token_manager import (generate_relative_link,
                                              decrypt_link
                                              )

relative_verification_link = generate_relative_link("sandeep@dummy.com")
parts = relative_verification_link.split("/")
encoded_email = parts[4]
token = parts[5]

decrypt_link(encoded_email, token)

