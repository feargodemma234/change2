import re

ALLOWED_PROOF_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "pdf",
}

MAX_PROOF_BYTES = 10 * 1024 * 1024


def clean_text(value, max_length=500):
    if value is None:
        return ""

    value = str(value).strip()

    value = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", value)

    return value[:max_length]


def valid_email(email):
    email = str(email).strip().lower()

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return bool(re.match(pattern, email))


def validate_proof(uploaded_file):
    if uploaded_file is None:
        return False, "Please upload your payment proof."

    filename = str(uploaded_file.name).lower()

    if "." not in filename:
        return False, "The uploaded file must have an extension."

    extension = filename.rsplit(".", 1)[1]

    if extension not in ALLOWED_PROOF_EXTENSIONS:
        return False, "Only JPG, JPEG, PNG or PDF files are allowed."

    if uploaded_file.size > MAX_PROOF_BYTES:
        return False, "The payment proof must be 10 MB or smaller."

    return True, "Payment proof accepted."


def validate_phone(phone):
    phone = str(phone).strip()

    if not phone:
        return True

    digits = re.sub(r"\D", "", phone)

    if len(digits) < 7 or len(digits) > 15:
        return False

    return True


def validate_required(value, field_name):
    if not str(value).strip():
        return False, f"{field_name} is required."

    return True, ""