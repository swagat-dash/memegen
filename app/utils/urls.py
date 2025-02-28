from furl import furl

from .. import settings


def schema(value) -> bool:
    return value and "://" in value


def arg(request, default, *names):
    for name in names:
        value = request.args.get(name)
        if value is not None:
            return value
    return default


def normalize(url: str) -> str:
    original = furl(url)
    normalized = furl(f"{settings.BASE_URL}{original.path}")

    if "background" in original.args:
        normalized.args["background"] = original.args["background"]

    return clean(str(normalized))


def params(**kwargs) -> dict:
    return {k: v for k, v in kwargs.items() if v}


def clean(url: str) -> str:
    # Unquote slashes
    url = url.replace("%3A%2F%2F", "://").replace("%2F", "/")

    # Drop trailing spaces
    while "/_." in url:
        url = url.replace("/_.", ".")

    return url
