"""Error types. Every one of these is meant to be printed to a human, not a stack trace."""


class KitError(Exception):
    """Base class for every error this tool raises on purpose."""


class ConfigError(KitError):
    """The YAML config could not be loaded or is structurally wrong."""


class MissingFieldError(KitError):
    """A template asked for a field the config does not contain.

    Carries the dotted path of the field and (once the renderer catches it) the
    template that wanted it, so the message can name both.
    """

    def __init__(self, path: str, template: str | None = None, hint: str | None = None):
        self.path = path
        self.template = template
        self.hint = hint
        super().__init__(str(self))

    def __str__(self) -> str:
        where = f" (needed by template '{self.template}')" if self.template else ""
        msg = f"Missing required field '{self.path}' in your config{where}."
        if self.hint:
            msg += f" {self.hint}"
        msg += " Run `client-onboard-kit init` to see a fully-populated example."
        return msg


class UnrenderedPlaceholderError(KitError):
    """Output still contained template syntax. This must never reach a client."""

    def __init__(self, template: str, snippets: list[str]):
        self.template = template
        self.snippets = snippets
        super().__init__(str(self))

    def __str__(self) -> str:
        found = "; ".join(self.snippets[:5])
        return (
            f"Refusing to write '{self.template}': the rendered output still contains "
            f"template syntax ({found}). This is a bug in the template — fix the "
            f"template rather than shipping a document with a raw placeholder in it."
        )


class TemplateNotFoundError(KitError):
    pass
