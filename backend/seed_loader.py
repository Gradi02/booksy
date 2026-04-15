import json
from datetime import date
from pathlib import Path

from sqlalchemy.orm import Session

import models
from auth import get_password_hash


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _parse_status(value: str | None) -> models.DeviceStatus:
    """Parse status string to DeviceStatus enum."""
    if not value:
        return models.DeviceStatus.AVAILABLE
    try:
        return models.DeviceStatus(value)
    except ValueError:
        return models.DeviceStatus.AVAILABLE


def ensure_default_admin(db: Session) -> None:
    existing = db.query(models.User).filter(models.User.username == "admin").first()
    if existing:
        return
    admin = models.User(
        username="admin",
        hashed_password=get_password_hash("admin123"),
        is_admin=True,
    )
    db.add(admin)
    db.commit()


def seed_devices(db: Session, seed_path: Path) -> None:
    if db.query(models.Device).first():
        return

    with seed_path.open("r", encoding="utf-8") as file:
        raw_items = json.load(file)

    seen_ids: set[int] = set()
    for item in raw_items:
        item_id = item.get("id")
        if not isinstance(item_id, int) or item_id in seen_ids:
            continue
        seen_ids.add(item_id)
        device = models.Device(
            id=item_id,
            name=item.get("name") or "Unnamed Device",
            brand=item.get("brand") or None,
            purchase_date=_parse_date(item.get("purchaseDate")),
            status=_parse_status(item.get("status")),
            notes=item.get("notes"),
            assigned_to=item.get("assignedTo"),
            history=item.get("history"),
        )
        db.add(device)
    db.commit()


def initialize_data(db: Session) -> None:
    ensure_default_admin(db)
    seed_path = Path(__file__).resolve().parent / "seed.json"
    if seed_path.exists():
        seed_devices(db, seed_path)
