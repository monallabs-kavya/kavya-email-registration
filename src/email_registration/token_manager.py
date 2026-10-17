import logging
from datetime import (datetime,
                      timedelta)


from binascii import Error as BASE64ERROR
from base64 import urlsafe_b64encode, urlsafe_b64decode
import string
import hmac
import hashlib

logger = logging.getLogger(__name__)
from .errors import (SignatureExpired,
                     BadSignature, 
                     MaxRetriesExceeded, 
                     UserAlreadyActive,
                     InvalidToken
                     )
PASSWORD_RESET_TIMEOUT = 259200
SECRET= "my secret key"
KEY_SALT = b"email-verification-salt"
ALGORITHM ="sha256"
def int_to_base36(n):
    """Convert an integer to a base36 string."""
    if n == 0:
        return '0'
    chars = string.digits + string.ascii_lowercase
    result = []
    while n > 0:
        n, remainder = divmod(n, 36)
        result.append(chars[remainder])
    return ''.join(reversed(result))



def base36_to_int(s):
    """Convert a base36 string back to an integer."""
    return int(s, 36)


def _num_seconds(dt):
    return int((dt - datetime(2001, 1, 1)).total_seconds())

def _now():
    # Used for mocking in tests
    return datetime.now()


def perform_encoding(plain_entity):
    return urlsafe_b64encode(str(plain_entity).encode('UTF-8')).decode('UTF-8')

def perform_decoding(encoded_entity):
    try:
        return urlsafe_b64decode(encoded_entity).decode('UTF-8')
    except BASE64ERROR:
        return False

def _make_hash_value(user_email, timestamp):
    """
    Creates a unique hash value using only the email and timestamp.
    You can optionally mix in a static salt or secret-dependent value if needed.
    """
    # Clean up and normalize the email to ensure consistency
    normalized_email = str(user_email).strip().lower()
    return f"{normalized_email}{timestamp}"


def salted_hmac(key_salt, value, secret, algorithm="sha256"):
    """

    """
    if isinstance(secret, str):
        secret = secret.encode('utf-8')
    if isinstance(key_salt, str):
        key_salt = key_salt.encode('utf-8')
    if isinstance(value, str):
        value = value.encode('utf-8')

    # Derive a key using the salt and secret (similar to Django's approach)
    hasher = getattr(hashlib, algorithm)
    key = hasher(key_salt + secret).digest()
    return hmac.new(key, value, hasher)


def _make_token_with_timestamp(user_email, timestamp, secret):
    ts_b36 = int_to_base36(timestamp)
    
    # Generate HMAC hexdigest and shorten it (taking every 2nd character)
    h = salted_hmac(KEY_SALT, _make_hash_value(user_email, timestamp), secret, ALGORITHM)
    hash_string = h.hexdigest()[::2]
    
    return f"{ts_b36}-{hash_string}"


def _make_token_with_timestamp(user_email, timestamp, secret):
    ts_b36 = int_to_base36(timestamp)
    
    # Generate HMAC hexdigest and shorten it (taking every 2nd character)
    h = salted_hmac(KEY_SALT, _make_hash_value(user_email, timestamp), secret, ALGORITHM)
    hash_string = h.hexdigest()[::2]
    
    return f"{ts_b36}-{hash_string}"

def make_token(user):
    """
    """
    return _make_token_with_timestamp(
        user,
        _num_seconds(_now()),
        SECRET,
    )


def generate_relative_link(user_email):
    """
    Generates link for the first time.
    """
    #token = __generate_token(inactive_user)
    token = make_token(user_email)
    encoded_email = urlsafe_b64encode(str(user_email).encode('utf-8')).decode('utf-8')

    link = f"/verification/user/verify-email/{encoded_email}/{token}/"
    #return encoded_email, token

    #absolute_link = request.build_absolute_uri(link)
    # need full/a link
    #absolute_link  = link
    #request.url.host
    #return absolute_link
    return link


def check_token(user_email, token):
    """
    Check that a verification token is correct and hasn't expired for a given email.
    """
    if not (user_email and token):
        return False
        
    # Parse the token
    try:
        ts_b36, _ = token.split("-")
        ts = base36_to_int(ts_b36)
    except (ValueError, TypeError):
        return False

    # Check that the token hasn't been tampered with (using timing-attack safe comparison)
    expected_token = _make_token_with_timestamp(user_email, ts, SECRET)
    if not hmac.compare_digest(expected_token, token):
        return False

    # Check if the timestamp is within the allowed timeout limit
    if (_num_seconds(_now()) - ts) > PASSWORD_RESET_TIMEOUT:
        return False

    return True


def decrypt_link(encoded_email, token):
    """
    Main verification and decryption happens here without Django dependencies.
    """
    try:
        decoded_email = perform_decoding(encoded_email)
        #decoded_token = perform_decoding(encoded_token)
    except Exception as e:
        raise InvalidToken("Malformed base64 encoding in link.") from e

    # 1. Verify token structure, signature, and expiration using our pure-Python check_token
    # Note: check_token internally validates the HMAC signature and the max_age/timeout limit.
    if not check_token(decoded_email, token):
        # To distinguish between expiration vs bad signature, we can do a quick check:
        try:
            ts_b36, _ = token.split("-")
            ts = base36_to_int(ts_b36)
            expected_token = _make_token_with_timestamp(decoded_email, ts, SECRET)
            
            # Check if signature matches but time has expired
            if hmac.compare_digest(expected_token, token):
                if (_num_seconds(_now()) - ts) > max_age:
                    logger.warning(f'\n{"~" * 40}\n[WARNING] : The link is Expired!\n{"~" * 40}\n')
                    # Optional: Handle retry count logic if user exists
                    # user = get_user_by_token(decoded_email, ...)
                    # if not __verify_attempts(user): raise MaxRetriesExceeded()
                    raise SignatureExpired("The verification link has expired.")
            else:
                logger.critical(f'\n{"~" * 40}\n[CRITICAL] : X_x --> CAUTION : LINK SIGNATURE ALTERED! <-- x_X\n{"~" * 40}\n')
                raise BadSignature("Token signature is invalid.")
        except (ValueError, TypeError) as exc:
            logger.critical(f'\n{"~" * 40}\n[CRITICAL] : X_x --> CAUTION : MALFORMED TOKEN! <-- x_X\n{"~" * 40}\n')
            raise InvalidToken("The token format is invalid.") from exc
            
        raise InvalidToken("Token verification failed.")

    print(f"SUCCESS: Email {decoded_email} successfully verified!")
    return decoded_email
