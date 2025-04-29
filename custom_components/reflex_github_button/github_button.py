"""Reflex custom component GithubButton."""

# For wrapping react guide, visit https://reflex.dev/docs/wrapping-react/overview/
from typing import Literal

import reflex as rx

# Some libraries you want to wrap may require dynamic imports.
# This is because they they may not be compatible with Server-Side Rendering (SSR).
# To handle this in Reflex, all you need to do is subclass `NoSSRComponent` instead.
# For example:
# from reflex.components.component import NoSSRComponent
# class GithubButton(NoSSRComponent):
#     pass


class GitHubButton(rx.Component):
    """A custom loading icon component."""

    # The React library to wrap.
    library = "react-github-btn"
    # The React component tag.
    tag = "GitHubButton"
    is_default = True

    # The props of the React component.
    # Note: when Reflex compiles the component to Javascript,
    # `snake_case` property names are automatically formatted as `camelCase`.
    # The prop names may be defined in `camelCase` as well.
    # some_prop: rx.Var[str] = "some default value"
    # some_other_prop: rx.Var[int] = 1
    href: str
    # data_color_scheme: str = "no-preference: dark; light: dark; dark: dark;"
    # data_icon: str = "octicon-star"
    # data_size: str = "large"
    # aria_label: str = "GitHub"

    # Event triggers declaration if any.
    # Below is equivalent to merging `{ "on_change": lambda e: [e] }`
    # onto the default event triggers of parent/base Component.
    # The function defined for the `on_change` trigger maps event for the javascript
    # trigger to what will be passed to the backend event handler function.
    # on_change: rx.EventHandler[lambda e: [e]]
    #
    # To add custom code to your component
    # def _get_custom_code(self) -> str:
    #     return "const customCode = 'customCode';"
    #
    # def get_event_triggers(self) -> dict:
    #     return {"on_change": lambda status: [status]}


LiteralSize = Literal["large", "small", "medium"]
LiteralButtonType = Literal[
    "follow",
    "sponsor",
    "watch",
    "star",
    "fork",
    "issue",
    "discuss",
    "download",
    "install this package",
    "use this template",
    "use this github action",
]
DarkOrLight = Literal["dark", "light"]

TYPE_ICON_MAP: dict[LiteralButtonType, str | None] = {
    "follow": None,
    "sponsor": "octicon-heart",
    "watch": "octicon-eye",
    "star": "octicon-star",
    "fork": "octicon-repo-forked",
    "issue": "octicon-issue-opened",
    "discuss": "octicon-comment-discussion",
    "download": "octicon-download",
    "install this package": "octicon-package",
    "use this template": "octicon-repo-template",
    "use this github action": "octicon-play",
}

EXTRA_PATH_MAP: dict[LiteralButtonType, str | None] = {
    "watch": "subscription",
    "fork": "fork",
    "issue": "issues",
    "discuss": "discussions",
    "download": "archive/HEAD.zip",
    "install this package": "packages",
    "use this template": "generate",
}


def github_button(
    button_type: LiteralButtonType,
    owner: str,
    repo: str | None = None,
    show_count: bool = False,
    large: bool = True,
    color_default: DarkOrLight = "light",
    color_light: DarkOrLight = "light",
    color_dark: DarkOrLight = "dark",
    dynamic_color_mode: bool = False,
    standard_icon: bool = False,
    **props,
) -> GitHubButton:
    """Create a GitHub button.

    See https://buttons.github.io/ for full customization examples.

    Args:
        button_type: The type of button to create.
        owner: The owner of the repository.
        repo: The name of the repository.
        show_count: Whether to show the count of stars/issues/etc..
        large: Whether to use a large button.
        color_default: The default color scheme. (user has no preference)
        color_light: The light color scheme. (user has light preference)
        color_dark: The dark color scheme. (user has dark preference)
        dynamic_color_mode: Set True to match the reflex color theme
            (uses reflex color mode instead of user preferences).
        standard_icon: Whether to use the standard GitHub icon instead.
    """
    if button_type not in ["follow", "sponsor"] and repo is None:
        raise ValueError(f"{button_type} button requires a repo name")
    if button_type in ["follow", "sponsor"] and repo is not None:
        raise ValueError(f"{button_type} button does not take a repo name")
    if show_count is True and button_type not in [
        "follow",
        "watch",
        "star",
        "fork",
        "issue",
    ]:
        raise ValueError(f"{button_type} button does not take a show_count")

    owner_repo = f"{owner}/{repo}" if repo else owner
    href = f"https://github.com/{owner_repo}"
    if extra_path := EXTRA_PATH_MAP.get(button_type):
        href += f"/{extra_path}"

    button_type_text = button_type.title()
    aria = f"{button_type_text} {owner_repo} on GitHub"

    if dynamic_color_mode:
        light_or_dark = rx.color_mode_cond(color_light, color_dark)
        color_scheme = f"no-preference: {light_or_dark}; light: {light_or_dark}; dark: {light_or_dark};"
    else:
        color_scheme = (
            f"no-preference: {color_default}; light: {color_light}; dark: {color_dark};"
        )

    return GitHubButton.create(
        button_type_text,
        href=href,
        data_color_scheme=color_scheme,
        data_icon=TYPE_ICON_MAP.get(button_type) if not standard_icon else None,
        data_size="large" if large else None,
        data_show_count=show_count if show_count else None,
        aria_label=aria,
        **props,
    )
