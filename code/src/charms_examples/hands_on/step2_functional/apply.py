from __future__ import annotations

from error_types import *
from step2_functional.action_types import PasswordActions
from type_defs import *

from result import *


def apply_handler(
    actions: PasswordActions, outcome: PasswordOutcome
) -> Result[ApplyError, None]: ...
