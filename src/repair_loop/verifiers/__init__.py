"""Remote verification implementations."""

from .base import Verifier
from .github_actions import GitHubActionsVerifier

__all__ = ["GitHubActionsVerifier", "Verifier"]
