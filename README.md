# loginflask_api
Login Email and password validation using Flaskapi and Mysql Python project

HI,
Project Title: login page api Flask Framework and mysql with Python project
Main Purpose : If you enter the email and password in login form.
sometime error will be raised because the your not correct email like your missing '@' this symbol so dispay the error
example

import re
def validate_email(email):
# Regular expression pattern to match a valid email address
pattern = r'^[\w.-]+@[\w.-]+.\w+$'

if re.match(pattern, email):
    print("Valid email:", email)
else:
    print("Invalid email:", email)
Test cases
emails = [
"user@example.com",
"invalid-email",
"another.user@domain.co",
"no@tld.",
"name.lastname@subdomain.domain.com",
]

for email in emails:
validate_email(email)

def validate_password(password):
# Regular expression pattern to match a valid password
# This pattern requires at least 8 characters, including at least one uppercase letter, one lowercase letter, one digit, and one special character.
pattern = r'^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[@$!%?&])[A-Za-z\d@$!%?&]{8,}$'

if re.match(pattern, password):
    print("Valid password",password)
else:
    print("Invalid password",password)
Test cases
passwords = [
"Passw0rd$",
"simple",
"12345678",
"P@ssw0rd",
"Complex123$",
"Auto@1224"
]

for password in passwords:
validate_password(password)


