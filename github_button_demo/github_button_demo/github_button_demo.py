"""Welcome to Reflex! This file showcases the custom component in a basic app."""

import reflex as rx
from reflex_github_button import LiteralButtonType, github_button
from rxconfig import config

filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    """The app state."""

    pass


CODE_EXAMPLE = """
from reflex_github_button import github_button

github_button(
    button_type="star",
    owner="TimChild",
    repo="reflex-github-button",
    show_count=True,
)
"""

# LiteralButtonType = Literal[
#     "follow",
#     "sponsor",
#     "watch",
#     "star",
#     "fork",
#     "issue",
#     "discuss",
#     "download",
#     "install this package",
#     "use this template",
#     "use this github action",
# ]


def gh_button(
    button_type: LiteralButtonType,
    show_count: bool = False,
    repo: str | None = "reflex-github-button",
) -> rx.Component:
    return github_button(
        button_type=button_type,
        owner="TimChild",
        repo=repo,
        show_count=show_count,
        dynamic_color_mode=True,
    )


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.color_mode.button(),
            rx.text(
                "Add a GitHub button to your app",
                font_size="2em",
            ),
            rx.text(
                "See ",
                rx.link(
                    "https://buttons.github.io/", href="https://buttons.github.io/"
                ),
                " for full customization examples.",
            ),
            rx.code_block(CODE_EXAMPLE, language="python"),
            rx.hstack(
                gh_button("follow", repo=None, show_count=True),
                gh_button("sponsor", repo=None),
                gh_button("watch", show_count=True),
                gh_button("star", show_count=True),
            ),
            rx.hstack(
                gh_button("fork", show_count=True),
                gh_button("issue", show_count=True),
                gh_button("discuss"),
                gh_button("download"),
            ),
            rx.hstack(
                gh_button("install this package"),
                gh_button("use this template"),
                gh_button("use this github action"),
            ),
            rx.text(
                "You can also set the color scheme and choose between small and large."
            ),
            align="center",
            spacing="7",
        ),
        height="100vh",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
