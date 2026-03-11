from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, assert_never, cast, cast


# ---------------------------------------------------------------------------
# BAD: one record for all states
# ---------------------------------------------------------------------------

@dataclass
class UserRecord:
    session_id: str
    # if email is set, the user has registered; name must also be present
    email: Optional[str] = None
    name: Optional[str] = None
    # if user_id is set, the account is verified; email and name must be present
    user_id: Optional[str] = None
    # only meaningful for PendingVerification; must be present if email is set
    verification_token: Optional[str] = None
    # only meaningful for Active users; must be present if user_id is set
    loyalty_points: Optional[int] = None
    shipping_address: Optional[str] = None


def process_user_record_cast(user: UserRecord):
    if user.user_id:
        print(f"Welcome back, {cast(str, user.name).upper()}")
        send_receipt(cast(str, user.email))
        give_discount(user.user_id, cast(int, user.loyalty_points))
        ship_to(cast(str, user.shipping_address))
    elif user.email:
        send_verification_email(user.email, cast(str, user.verification_token))
    else:
        show_guest_banner()


def process_user_record_asserted(user: UserRecord):
    if user.user_id:
        assert user.name is not None
        assert user.email is not None
        assert user.loyalty_points is not None
        assert user.shipping_address is not None
        print(f"Welcome back, {user.name.upper()}")
        send_receipt(user.email)
        give_discount(user.user_id, user.loyalty_points)
        ship_to(user.shipping_address)
    elif user.email:
        assert user.verification_token is not None
        send_verification_email(user.email, user.verification_token)
    else:
        show_guest_banner()


# ---------------------------------------------------------------------------
# GOOD: three distinct states
# ---------------------------------------------------------------------------

@dataclass
class Guest:
    session_id: str


@dataclass
class PendingVerification:
    session_id: str
    email: str
    name: str
    verification_token: str


@dataclass
class Active:
    session_id: str
    user_id: str
    email: str
    name: str
    loyalty_points: int
    shipping_address: str


type User = Guest | PendingVerification | Active


def process_user(user: User):
    match user:
        case Guest():
            show_guest_banner()
        case PendingVerification(email=email, verification_token=token):
            send_verification_email(email, token)
        case Active(name=name, email=email, user_id=uid, loyalty_points=pts, shipping_address=addr):
            print(f"Welcome back, {name.upper()}")
            send_receipt(email)
            give_discount(uid, pts)
            ship_to(addr)
        case _ as unreachable:
            assert_never(unreachable)


# ---------------------------------------------------------------------------
# stubs
# ---------------------------------------------------------------------------

def show_guest_banner(): ...
def send_verification_email(email: str, token: str): ...
def send_receipt(email: str): ...
def give_discount(user_id: str, loyalty_points: int): ...
def ship_to(address: str): ...
