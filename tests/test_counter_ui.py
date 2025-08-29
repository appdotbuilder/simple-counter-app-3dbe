"""Tests for counter UI interactions."""

import pytest
from nicegui.testing import User

from app.database import reset_db


@pytest.fixture()
def new_db():
    """Fresh database for each test."""
    reset_db()
    yield
    reset_db()


async def test_counter_page_loads(user: User, new_db) -> None:
    """Test that the counter page loads with initial state."""
    await user.open("/counter")

    # Check page title
    await user.should_see("Counter Application")

    # Check initial counter display shows 0
    await user.should_see(marker="counter-display")
    await user.should_see("0")

    # Check buttons are present
    await user.should_see(marker="increment-button")
    await user.should_see(marker="decrement-button")
    await user.should_see(marker="reset-button")


async def test_increment_button_functionality(user: User, new_db) -> None:
    """Test increment button increases counter value."""
    await user.open("/counter")

    # Click increment button
    user.find(marker="increment-button").click()

    # Wait for UI update and check counter display
    await user.should_see("Counter incremented to 1")
    await user.should_see("1")


async def test_decrement_button_functionality(user: User, new_db) -> None:
    """Test decrement button decreases counter value."""
    await user.open("/counter")

    # Click decrement button
    user.find(marker="decrement-button").click()

    # Wait for UI update and check counter display
    await user.should_see("Counter decremented to -1")
    await user.should_see("-1")


async def test_reset_button_functionality(user: User, new_db) -> None:
    """Test reset button sets counter back to 0."""
    await user.open("/counter")

    # First increment the counter
    user.find(marker="increment-button").click()
    await user.should_see("Counter incremented to 1")

    # Then reset it
    user.find(marker="reset-button").click()
    await user.should_see("Counter reset to 0")

    # Check counter display shows 0
    await user.should_see("0")


async def test_multiple_increments(user: User, new_db) -> None:
    """Test multiple increment operations."""
    await user.open("/counter")

    # Click increment 3 times
    for expected in range(1, 4):
        user.find(marker="increment-button").click()
        await user.should_see(f"Counter incremented to {expected}")

    # Final check
    await user.should_see("3")


async def test_multiple_decrements(user: User, new_db) -> None:
    """Test multiple decrement operations."""
    await user.open("/counter")

    # Click decrement 2 times
    user.find(marker="decrement-button").click()
    await user.should_see("Counter decremented to -1")

    user.find(marker="decrement-button").click()
    await user.should_see("Counter decremented to -2")

    # Final check
    await user.should_see("-2")


async def test_mixed_operations(user: User, new_db) -> None:
    """Test mixed increment and decrement operations."""
    await user.open("/counter")

    # Increment 3 times
    for i in range(3):
        user.find(marker="increment-button").click()
        await user.should_see(f"Counter incremented to {i + 1}")

    # Decrement 2 times
    user.find(marker="decrement-button").click()
    await user.should_see("Counter decremented to 2")

    user.find(marker="decrement-button").click()
    await user.should_see("Counter decremented to 1")

    # Final check
    await user.should_see("1")


async def test_reset_after_negative_value(user: User, new_db) -> None:
    """Test reset functionality after reaching negative values."""
    await user.open("/counter")

    # Decrement to negative
    user.find(marker="decrement-button").click()
    await user.should_see("Counter decremented to -1")

    user.find(marker="decrement-button").click()
    await user.should_see("Counter decremented to -2")

    # Reset
    user.find(marker="reset-button").click()
    await user.should_see("Counter reset to 0")

    # Check counter display shows 0
    await user.should_see("0")


async def test_index_redirects_to_counter(user: User, new_db) -> None:
    """Test that root path redirects to counter page."""
    await user.open("/")

    # Should be redirected to counter page
    await user.should_see("Counter Application")
    await user.should_see(marker="counter-display")
