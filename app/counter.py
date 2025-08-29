"""Counter application UI module."""

from nicegui import ui

from app.counter_service import get_counter_value, increment_counter, decrement_counter, reset_counter


def create():
    """Create the counter application routes and UI."""

    @ui.page("/counter")
    def counter_page():
        """Counter application page with increment, decrement, and display."""

        # Apply modern theme colors
        ui.colors(
            primary="#2563eb",
            secondary="#64748b",
            accent="#10b981",
            positive="#10b981",
            negative="#ef4444",
            warning="#f59e0b",
        )

        # Page header
        ui.label("Counter Application").classes("text-3xl font-bold text-gray-800 mb-8 text-center w-full")

        # Initialize counter value
        current_value = get_counter_value()

        # Create counter display and buttons within a centered card
        with ui.card().classes("w-96 mx-auto p-8 shadow-xl rounded-xl bg-white"):
            # Counter display
            counter_display = (
                ui.label(str(current_value))
                .classes("text-6xl font-bold text-center w-full mb-8 text-gray-800")
                .mark("counter-display")
            )

            # Button container
            with ui.row().classes("gap-4 justify-center w-full mb-6"):
                # Decrement button
                ui.button("−", on_click=lambda: handle_decrement()).classes(
                    "bg-negative text-white text-2xl font-bold w-16 h-16 rounded-full shadow-lg hover:shadow-xl transition-shadow"
                ).mark("decrement-button")

                # Increment button
                ui.button("+", on_click=lambda: handle_increment()).classes(
                    "bg-positive text-white text-2xl font-bold w-16 h-16 rounded-full shadow-lg hover:shadow-xl transition-shadow"
                ).mark("increment-button")

            # Reset button
            ui.button("Reset", on_click=lambda: handle_reset()).classes(
                "bg-secondary text-white px-6 py-2 rounded-lg w-full shadow-md hover:shadow-lg transition-shadow"
            ).mark("reset-button")

        def handle_increment():
            """Handle increment button click."""
            new_value = increment_counter()
            counter_display.set_text(str(new_value))
            ui.notify(f"Counter incremented to {new_value}", type="positive")

        def handle_decrement():
            """Handle decrement button click."""
            new_value = decrement_counter()
            counter_display.set_text(str(new_value))
            ui.notify(f"Counter decremented to {new_value}", type="info")

        def handle_reset():
            """Handle reset button click."""
            new_value = reset_counter()
            counter_display.set_text(str(new_value))
            ui.notify("Counter reset to 0", type="warning")

    @ui.page("/")
    def index():
        """Redirect root to counter page."""
        ui.navigate.to("/counter")
