"""Counter service module for managing counter operations."""

from datetime import datetime

from sqlmodel import select

from app.database import get_session
from app.models import Counter, CounterCreate


def get_or_create_counter(name: str = "default") -> Counter:
    """Get existing counter by name or create a new one if it doesn't exist."""
    with get_session() as session:
        statement = select(Counter).where(Counter.name == name)
        counter = session.exec(statement).first()

        if counter is None:
            counter_data = CounterCreate(name=name, value=0)
            counter = Counter(
                name=counter_data.name,
                value=counter_data.value,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(counter)
            session.commit()
            session.refresh(counter)

        return counter


def get_counter_value(name: str = "default") -> int:
    """Get the current value of a counter."""
    counter = get_or_create_counter(name)
    return counter.value


def increment_counter(name: str = "default") -> int:
    """Increment counter by 1 and return the new value."""
    with get_session() as session:
        statement = select(Counter).where(Counter.name == name)
        counter = session.exec(statement).first()

        if counter is None:
            counter = get_or_create_counter(name)

        # Re-query to get the fresh instance in this session
        statement = select(Counter).where(Counter.name == name)
        counter = session.exec(statement).first()

        if counter is not None:
            counter.value += 1
            counter.updated_at = datetime.utcnow()
            session.add(counter)
            session.commit()
            session.refresh(counter)
            return counter.value

        return 0


def decrement_counter(name: str = "default") -> int:
    """Decrement counter by 1 and return the new value."""
    with get_session() as session:
        statement = select(Counter).where(Counter.name == name)
        counter = session.exec(statement).first()

        if counter is None:
            counter = get_or_create_counter(name)

        # Re-query to get the fresh instance in this session
        statement = select(Counter).where(Counter.name == name)
        counter = session.exec(statement).first()

        if counter is not None:
            counter.value -= 1
            counter.updated_at = datetime.utcnow()
            session.add(counter)
            session.commit()
            session.refresh(counter)
            return counter.value

        return 0


def reset_counter(name: str = "default") -> int:
    """Reset counter to 0 and return the new value."""
    with get_session() as session:
        statement = select(Counter).where(Counter.name == name)
        counter = session.exec(statement).first()

        if counter is None:
            counter = get_or_create_counter(name)
            return 0

        # Re-query to get the fresh instance in this session
        statement = select(Counter).where(Counter.name == name)
        counter = session.exec(statement).first()

        if counter is not None:
            counter.value = 0
            counter.updated_at = datetime.utcnow()
            session.add(counter)
            session.commit()
            session.refresh(counter)
            return counter.value

        return 0
