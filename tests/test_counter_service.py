"""Tests for counter service logic."""

import pytest
from datetime import datetime

from app.counter_service import (
    get_or_create_counter,
    get_counter_value,
    increment_counter,
    decrement_counter,
    reset_counter,
)
from app.database import reset_db


@pytest.fixture()
def new_db():
    """Fresh database for each test."""
    reset_db()
    yield
    reset_db()


def test_get_or_create_counter_creates_new(new_db):
    """Test that get_or_create_counter creates a new counter when it doesn't exist."""
    counter = get_or_create_counter("test_counter")

    assert counter is not None
    assert counter.name == "test_counter"
    assert counter.value == 0
    assert isinstance(counter.created_at, datetime)
    assert isinstance(counter.updated_at, datetime)


def test_get_or_create_counter_gets_existing(new_db):
    """Test that get_or_create_counter returns existing counter."""
    # Create first counter
    counter1 = get_or_create_counter("test_counter")
    original_id = counter1.id

    # Get the same counter again
    counter2 = get_or_create_counter("test_counter")

    assert counter2.id == original_id
    assert counter2.name == "test_counter"
    assert counter2.value == 0


def test_get_counter_value_default(new_db):
    """Test getting counter value with default name."""
    value = get_counter_value()
    assert value == 0


def test_get_counter_value_custom_name(new_db):
    """Test getting counter value with custom name."""
    value = get_counter_value("custom")
    assert value == 0


def test_increment_counter_from_zero(new_db):
    """Test incrementing counter from initial value of 0."""
    new_value = increment_counter()
    assert new_value == 1

    # Verify persistence
    stored_value = get_counter_value()
    assert stored_value == 1


def test_increment_counter_multiple_times(new_db):
    """Test incrementing counter multiple times."""
    # Increment 5 times
    for expected in range(1, 6):
        new_value = increment_counter()
        assert new_value == expected

    # Verify final value
    final_value = get_counter_value()
    assert final_value == 5


def test_increment_counter_custom_name(new_db):
    """Test incrementing counter with custom name."""
    new_value = increment_counter("custom_counter")
    assert new_value == 1

    # Verify the default counter is still 0
    default_value = get_counter_value()
    assert default_value == 0


def test_decrement_counter_from_zero(new_db):
    """Test decrementing counter from initial value of 0."""
    new_value = decrement_counter()
    assert new_value == -1

    # Verify persistence
    stored_value = get_counter_value()
    assert stored_value == -1


def test_decrement_counter_from_positive(new_db):
    """Test decrementing counter from positive value."""
    # First increment to 3
    increment_counter()
    increment_counter()
    increment_counter()

    # Then decrement
    new_value = decrement_counter()
    assert new_value == 2

    # Verify persistence
    stored_value = get_counter_value()
    assert stored_value == 2


def test_decrement_counter_multiple_times(new_db):
    """Test decrementing counter multiple times."""
    # Start with positive value
    increment_counter()
    increment_counter()  # Counter = 2

    # Decrement multiple times
    assert decrement_counter() == 1
    assert decrement_counter() == 0
    assert decrement_counter() == -1
    assert decrement_counter() == -2


def test_decrement_counter_custom_name(new_db):
    """Test decrementing counter with custom name."""
    new_value = decrement_counter("custom_counter")
    assert new_value == -1

    # Verify the default counter is still 0
    default_value = get_counter_value()
    assert default_value == 0


def test_reset_counter_from_positive(new_db):
    """Test resetting counter from positive value."""
    # First increment to 5
    for _ in range(5):
        increment_counter()

    # Reset to 0
    new_value = reset_counter()
    assert new_value == 0

    # Verify persistence
    stored_value = get_counter_value()
    assert stored_value == 0


def test_reset_counter_from_negative(new_db):
    """Test resetting counter from negative value."""
    # First decrement to -3
    for _ in range(3):
        decrement_counter()

    # Reset to 0
    new_value = reset_counter()
    assert new_value == 0

    # Verify persistence
    stored_value = get_counter_value()
    assert stored_value == 0


def test_reset_counter_already_zero(new_db):
    """Test resetting counter that is already 0."""
    new_value = reset_counter()
    assert new_value == 0


def test_reset_counter_custom_name(new_db):
    """Test resetting counter with custom name."""
    # Increment custom counter
    increment_counter("custom_counter")
    increment_counter("custom_counter")

    # Reset custom counter
    new_value = reset_counter("custom_counter")
    assert new_value == 0

    # Verify custom counter is reset but default is still 0
    assert get_counter_value("custom_counter") == 0
    assert get_counter_value() == 0


def test_multiple_counters_independent(new_db):
    """Test that multiple counters operate independently."""
    # Modify different counters
    increment_counter("counter1")
    increment_counter("counter1")
    increment_counter("counter1")  # counter1 = 3

    decrement_counter("counter2")
    decrement_counter("counter2")  # counter2 = -2

    increment_counter()  # default = 1

    # Verify independence
    assert get_counter_value("counter1") == 3
    assert get_counter_value("counter2") == -2
    assert get_counter_value() == 1


def test_counter_updates_timestamp(new_db):
    """Test that counter operations update the timestamp."""
    counter1 = get_or_create_counter("test")
    original_time = counter1.updated_at

    # Small delay to ensure timestamp difference
    import time

    time.sleep(0.01)

    # Increment and check timestamp updated
    increment_counter("test")
    counter2 = get_or_create_counter("test")

    assert counter2.updated_at > original_time


def test_edge_cases_large_numbers(new_db):
    """Test counter with large positive and negative numbers."""
    # Test large increments
    for _ in range(1000):
        increment_counter("large_test")

    assert get_counter_value("large_test") == 1000

    # Test large decrements
    for _ in range(1500):
        decrement_counter("large_test")

    assert get_counter_value("large_test") == -500
