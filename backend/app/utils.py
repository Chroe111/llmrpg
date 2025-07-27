import textwrap


def clean(text: str, **kwargs: str) -> str:
    return textwrap.dedent(text.format(**kwargs)).strip()
