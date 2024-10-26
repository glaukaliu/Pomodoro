
# Pomodoro Timer

A simple and customizable Pomodoro Timer application built with Python and Tkinter. This application helps you manage your work and break intervals using the Pomodoro Technique.

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/pomodoro-timer.git
   cd pomodoro-timer
   ```

2. **Create a virtual environment (recommended):**

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Upgrade pip (optional but recommended):**

   ```sh
   pip install --upgrade pip
   ```

4. **Install the required packages:**

   ```sh
   pip install pygame
   ```

5. **Place the sound files in the project directory:**

   Ensure you have `click.mp3` and `finish.mp3` in the same directory as the Python scripts.

## Usage

When you run the application, you will see the main window with the following options:

1. **Start/Stop Timer**:
   - Click the Start button to begin the timer.
   - Click the Stop button to pause the timer.
   - A click sound will play when you press the Start/Stop button.

2. **Mode Selection**:
   - You can switch between Pomodoro, Short Break, and Long Break modes.
   - The timer will reset to the selected mode's duration.

3. **Settings**:
   - Adjust the durations for Pomodoro, Short Break, and Long Break.
   - Changes will apply immediately if the mode is active.

4. **Timer Completion**:
   - When the timer reaches zero, a finish sound will play.
   - The timer will reset to the initial duration of the current mode.

## License

[MIT](https://choosealicense.com/licenses/mit/)

### Documentation

#### Project Structure

- **main.py**: The entry point of the application. It initializes the `PomodoroTimer` class.
- **pomodoro_timer.py**: Contains the `PomodoroTimer` class, which handles the UI and timer logic.
- **sound_manager.py**: Contains the `SoundManager` class, which handles playing sounds using `pygame`.

#### Key Classes and Methods

- **PomodoroTimer (pomodoro_timer.py)**
   - `__init__()`: Initializes the application window and variables.
   - `create_widgets()`: Sets up the UI components.
   - `start_stop_timer()`: Starts or stops the timer.
   - `run_timer()`: Manages the countdown logic.
   - `countdown()`: Updates the timer each second.
   - `update_time_display()`: Refreshes the displayed time.
   - `activate_pomodoro()`, `activate_short_break()`, `activate_long_break()`: Switches between modes.
   - `open_settings()`: Opens the settings window.
   - `set_pomodoro_time()`, `set_short_break_time()`, `set_long_break_time()`: Updates mode durations.

- **SoundManager (sound_manager.py)**
   - `__init__()`: Initializes the pygame mixer and sound file paths.
   - `play_sound(sound_name)`: Plays the specified sound in a separate thread.
   - `_play_sound_pygame(sound_file)`: Handles the actual playback of the sound file.

#### Data Handling

No complex data handling required. The application simply plays sound files and manages the timer using in-memory variables.
