
from urllib.parse import urlparse

SENSITIVE_WORDS = [
    "login", "verify", "update", "password",
    "secure", "account", "banking", "confirm",
    "signin", "wallet", "payment"
]


def extract_features(url):
    url = url.strip()
    lower_url = url.lower()

    if not url.startswith(("http://", "https://")):
        parsed_url = "http://" + url
    else:
        parsed_url = url

    parsed = urlparse(parsed_url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""

    valid_url = int(
        parsed.scheme in ("http", "https")
        and bool(hostname)
        and "." in hostname
        and " " not in url
    )

    features = [
        len(url),
        valid_url,
        int("@" in url),
        sum(word in lower_url for word in SENSITIVE_WORDS),
        len(path),
        int(parsed.scheme == "https"),
        url.count("."),
        url.count("-"),
        lower_url.count("and"),
        lower_url.count("or"),
        lower_url.count("www"),
        lower_url.count("com"),
        url.count("_")
    ]

    return features
