"""
Comprehensive Stroop Test Application
=====================================

A professional PyQt5-based implementation of the Stroop effect psychological test.
This application provides an interactive GUI for administering various Stroop test
variants including classic, reverse, neutral, and emotional Stroop tests.

The Stroop effect demonstrates the interference in the reaction time of a task
when the name of a color (e.g., "blue", "green", or "red") is printed in a color
not denoted by the name (e.g., the word "red" printed in blue ink instead of red ink).

AUTHOR: [Your Name]
VERSION: 1.0.0
DATE: December 2025
LICENSE: MIT License

FEATURES:
    - Multiple test types (Classic, Reverse, Neutral, Emotional Stroop)
    - Four difficulty levels (Easy, Medium, Hard, Expert)
    - User profile management with persistent data storage
    - Comprehensive statistics and performance tracking
    - Professional GUI with modern styling
    - Configurable trial counts and time limits
    - Real-time response timing and accuracy measurement

USAGE:
    python stroop_test.py

SYSTEM REQUIREMENTS:
    - Python 3.7+
    - PyQt5
    - Windows/Linux/macOS

TECHNICAL NOTES:
    - Built with PyQt5 for cross-platform GUI
    - Uses QGraphicsDropShadowEffect for professional shadows
    - JSON-based user data persistence
    - Event-driven architecture for responsive UI
"""

import sys
import json
import random
import time
import os
from datetime import datetime

# PyQt5 imports for GUI components
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox,
    QLineEdit, QTextEdit, QProgressBar, QGroupBox,
    QMessageBox, QFrame, QSpacerItem, QSizePolicy,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush


class StroopTest(QMainWindow):
    """
    Main application window for the Stroop Test.

    This class implements the complete Stroop test application with:
    - User interface management
    - Test administration and timing
    - Data persistence
    - Statistics calculation and display
    - Professional styling with Qt-native effects

    Attributes:
        user_data (dict): Dictionary storing user profiles and statistics
        current_test (dict): Current test session data
        test_results (list): List of completed test results
        main_layout (QVBoxLayout): Main layout container
        Various UI elements stored as instance attributes
    """

    def __init__(self):
        """
        Initialize the Stroop Test application.

        Sets up the main window, loads user data, initializes UI components,
        and applies global styling.
        """
        super().__init__()

        # Initialize core data structures
        self.user_data = {}           # Stores user profiles and statistics
        self.current_test = None      # Current active test session
        self.test_results = []        # Completed test results

        # Load persistent user data
        self.load_user_data()

        # Initialize user interface
        self.init_ui()
        self.apply_global_styles()
    def __init__(self):
        super().__init__()
        self.user_data = {}
        self.current_test = None
        self.test_results = []
        self.load_user_data()
        
        self.init_ui()
        self.apply_global_styles()
        
    def init_ui(self):
        """
        Initialize the main user interface components.

        Sets up the main window properties, creates the central widget,
        establishes the main layout structure, and displays the initial
        welcome screen.
        """
        # Configure main window properties
        self.setWindowTitle("🧠 Comprehensive Stroop Test")
        self.setGeometry(100, 100, 900, 700)  # Position and size: x, y, width, height

        # Create central widget to hold all UI elements
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main vertical layout for the central widget
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setSpacing(15)                    # Space between elements
        self.main_layout.setContentsMargins(20, 20, 20, 20) # Margins around layout

        # Display the initial welcome screen
        self.show_welcome_screen()
        
    def apply_global_styles(self):
        """
        Apply global stylesheet for professional look using Qt-supported CSS only.

        This method defines the visual styling for all UI components using
        Qt's stylesheet system. Only CSS properties supported by Qt are used
        to avoid console warnings. Professional gradients, colors, and spacing
        are applied throughout the application.
        """
        self.setStyleSheet("""
            /* Main window background with gradient */
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border: 2px solid #4a5568;
                border-radius: 10px;
            }

            /* General label styling */
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }

            /* Title label styling */
            QLabel#title {
                color: #ffd700;
                font-weight: bold;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.1), stop:1 rgba(255,255,255,0.05));
                border-radius: 15px;
                padding: 10px;
                margin: 5px;
            }

            /* Group box containers */
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 10px;
                margin-top: 10px;
                background: rgba(255,255,255,0.1);
                padding: 10px;
            }

            /* Group box title styling */
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffd700;
                font-weight: bold;
            }

            /* Button styling with gradients */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4299e1, stop:1 #3182ce);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
                min-width: 120px;
            }

            /* Button hover effect */
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #63b3ed, stop:1 #4299e1);
            }

            /* Button pressed effect */
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3182ce, stop:1 #2c5282);
            }

            /* Start button special styling */
            QPushButton#start_btn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #48bb78, stop:1 #38a169);
                font-size: 16px;
                padding: 15px 30px;
            }

            /* Start button hover */
            QPushButton#start_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #68d391, stop:1 #48bb78);
            }

            /* Dropdown combobox styling */
            QComboBox {
                background: rgba(255,255,255,0.9);
                color: #2d3748;
                border: 2px solid #e2e8f0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                min-width: 150px;
            }

            /* Combobox hover effect */
            QComboBox:hover {
                border-color: #4299e1;
            }

            /* Combobox dropdown arrow styling */
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }

            /* Text input field styling */
            QLineEdit {
                background: rgba(255,255,255,0.9);
                color: #2d3748;
                border: 2px solid #e2e8f0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }

            /* Text input focus effect */
            QLineEdit:focus {
                border-color: #4299e1;
            }

            /* Progress bar styling */
            QProgressBar {
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 5px;
                text-align: center;
                background: rgba(255,255,255,0.1);
            }

            /* Progress bar fill styling */
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #48bb78, stop:1 #38a169);
                border-radius: 3px;
            }

            /* Stimulus display frame */
            QFrame#stimulus_frame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.95), stop:1 rgba(255,255,255,0.85));
                border: 3px solid #4299e1;
                border-radius: 15px;
            }

            /* Stimulus text label */
            QLabel#stimulus_label {
                color: #2d3748;
                font-weight: bold;
            }
        """)

    def add_shadow_effect(self, widget, blur_radius=10, offset_x=3, offset_y=3, color=QColor(0, 0, 0, 80)):
        """
        Add a professional drop shadow effect to a widget using Qt's native graphics effects.

        This method replaces unsupported CSS shadow properties with Qt's
        QGraphicsDropShadowEffect for clean, performant shadows that don't
        generate console warnings.

        Args:
            widget: The QWidget to apply shadow effect to
            blur_radius (int): Shadow blur radius in pixels (default: 10)
            offset_x (int): Horizontal shadow offset in pixels (default: 3)
            offset_y (int): Vertical shadow offset in pixels (default: 3)
            color (QColor): Shadow color with alpha transparency (default: semi-transparent black)
        """
        # Create Qt native drop shadow effect
        shadow = QGraphicsDropShadowEffect()

        # Configure shadow properties
        shadow.setBlurRadius(blur_radius)    # How blurred the shadow appears
        shadow.setOffset(offset_x, offset_y) # Shadow position relative to widget
        shadow.setColor(color)               # Shadow color and transparency

        # Apply the effect to the widget
        widget.setGraphicsEffect(shadow)
        
    def show_welcome_screen(self):
        """
        Display the main welcome screen with user selection and test configuration options.

        This method sets up the initial interface that users see when starting the application.
        It includes:
        - Application title with professional styling
        - User profile selection/management
        - Test type and difficulty configuration
        - Start button to begin testing
        """
        # Clear any existing UI elements from previous screens
        self.clear_layout()

        # Create and configure the main application title
        title = QLabel("🧠 Comprehensive Stroop Test")
        title.setObjectName("title")                           # For CSS styling
        title.setFont(QFont("Arial", 28, QFont.Bold))         # Large, bold font
        title.setAlignment(Qt.AlignCenter)                     # Center alignment
        title.setStyleSheet("""
            QLabel#title {
                color: #ffd700;                               /* Gold text color */
                font-weight: bold;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.15), stop:1 rgba(255,255,255,0.08));
                border: 2px solid rgba(255,215,0,0.3);       /* Subtle gold border */
                border-radius: 20px;                         /* Rounded corners */
                padding: 15px;                               /* Internal spacing */
                margin: 10px;                                /* External spacing */
            }
        """)

        # Apply professional drop shadow effect using Qt native methods
        self.add_shadow_effect(title, blur_radius=15, offset_x=0, offset_y=8,
                              color=QColor(0, 0, 0, 120))  # Semi-transparent black shadow
        self.main_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Test your cognitive processing speed and attention!")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #e2e8f0; margin-bottom: 20px;")
        self.main_layout.addWidget(subtitle)
        
        # User selection section with 3D effect
        user_group = QGroupBox("👤 User Profile")
        user_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                border: 3px solid rgba(255,255,255,0.4);
                border-radius: 12px;
                margin-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.15), stop:1 rgba(255,255,255,0.08));
                padding: 15px;
            }
        """)
        # Add native Qt shadow effect
        self.add_shadow_effect(user_group, blur_radius=10, offset_x=0, offset_y=6, color=QColor(0, 0, 0, 80))
        user_layout = QVBoxLayout()
        user_layout.setSpacing(10)
        
        # Existing user dropdown
        user_select_layout = QHBoxLayout()
        user_select_layout.addWidget(QLabel("Select User:"))
        self.user_combo = QComboBox()
        self.user_combo.addItem("🎯 New User")
        for user in self.user_data.keys():
            self.user_combo.addItem(f"👤 {user}")
        user_select_layout.addWidget(self.user_combo)
        user_layout.addLayout(user_select_layout)
        
        # New user input with enhanced styling
        new_user_layout = QHBoxLayout()
        new_user_layout.addWidget(QLabel("New User Name:"))
        self.new_user_input = QLineEdit()
        self.new_user_input.setPlaceholderText("Enter name for new user...")
        new_user_layout.addWidget(self.new_user_input)
        user_layout.addLayout(new_user_layout)
        
        user_group.setLayout(user_layout)
        self.main_layout.addWidget(user_group)
        
        # Test configuration section with 3D effect
        test_group = QGroupBox("⚙️ Test Configuration")
        test_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                border: 3px solid rgba(255,255,255,0.4);
                border-radius: 12px;
                margin-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.15), stop:1 rgba(255,255,255,0.08));
                padding: 15px;
            }
        """)
        # Add native Qt shadow effect
        self.add_shadow_effect(test_group, blur_radius=10, offset_x=0, offset_y=6, color=QColor(0, 0, 0, 80))
        test_layout = QGridLayout()
        test_layout.setSpacing(12)
        
        # Test type selection
        test_layout.addWidget(QLabel("🎮 Test Type:"), 0, 0)
        self.test_type_combo = QComboBox()
        self.test_type_combo.addItems([
            "🎨 Classic Stroop (Word vs Color)",
            "🔄 Reverse Stroop (Color vs Word)", 
            "🎯 Neutral (Color Only)",
            "💭 Emotional Stroop (Words with Emotional Content)"
        ])
        test_layout.addWidget(self.test_type_combo, 0, 1)
        
        # Difficulty level with color indicators
        test_layout.addWidget(QLabel("📊 Difficulty Level:"), 1, 0)
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["🟢 Easy", "🟡 Medium", "🟠 Hard", "🔴 Expert"])
        test_layout.addWidget(self.difficulty_combo, 1, 1)
        
        # Number of trials
        test_layout.addWidget(QLabel("🎲 Number of Trials:"), 2, 0)
        self.trials_combo = QComboBox()
        self.trials_combo.addItems(["10", "20", "30", "50"])
        test_layout.addWidget(self.trials_combo, 2, 1)
        
        test_group.setLayout(test_layout)
        self.main_layout.addWidget(test_group)
        
        # Enhanced start button
        start_button = QPushButton("🚀 Start Test")
        start_button.setObjectName("start_btn")
        start_button.clicked.connect(self.start_test)
        self.main_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        
        # Statistics button with icon
        stats_button = QPushButton("📈 View Statistics")
        stats_button.clicked.connect(self.show_statistics)
        self.main_layout.addWidget(stats_button, alignment=Qt.AlignCenter)
        
        # Add decorative spacer
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
    def start_test(self):
        """
        Initialize and start a new Stroop test session.

        This method orchestrates the test initialization process:
        1. Validates user selection
        2. Retrieves test configuration from UI controls
        3. Initializes test session data structure
        4. Generates randomized test trials
        5. Transitions to test interface

        The test session data structure tracks all aspects of the current test
        including timing, accuracy, and trial progression.
        """
        # Step 1: Validate user selection
        user_name = self.get_current_user()
        if not user_name:
            QMessageBox.warning(self, "Error", "Please select or create a user profile.")
            return

        # Step 2: Retrieve test configuration from UI controls
        # Remove emoji prefixes from combo box selections for clean data
        test_type = self.test_type_combo.currentText().replace('🎨 ', '').replace('🔄 ', '').replace('🎯 ', '').replace('💭 ', '')
        difficulty = self.difficulty_combo.currentText().replace('🟢 ', '').replace('🟡 ', '').replace('🟠 ', '').replace('🔴 ', '')
        num_trials = int(self.trials_combo.currentText())

        # Step 3: Re-seed random number generator for test variety
        # Ensures different trial sequences between test sessions
        random.seed()

        # Step 4: Initialize comprehensive test session data structure
        self.current_test = {
            'user': user_name,                           # User identifier
            'test_type': test_type,                      # Type of Stroop test
            'difficulty': difficulty,                    # Difficulty level
            'num_trials': num_trials,                    # Total number of trials
            'start_time': datetime.now().isoformat(),   # Test session start timestamp
            'trials': [],                               # List of individual trial data
            'current_trial': 0,                         # Current trial index (0-based)
            'correct_answers': 0,                       # Running count of correct responses
            'total_time': 0.0                           # Cumulative response time
        }

        # Step 5: Generate randomized test trials based on configuration
        self.generate_trials()

        # Step 6: Transition to test interface
        self.show_test_screen()
        
    def get_current_user(self):
        """
        Retrieve the currently selected or newly created user name.

        This method checks the user selection interface to determine which user
        is currently active. It handles two scenarios:
        1. Existing user selected from dropdown
        2. New user created via text input

        Returns:
            str or None: The user name if valid selection/input exists, None otherwise

        Note:
            User names are stored without emoji prefixes for clean data management
        """
        # Check if user selected "New User" option
        if self.user_combo.currentText() == "🎯 New User":
            # Get user input from text field and validate
            user_name = self.new_user_input.text().strip()
            if user_name:  # Ensure non-empty input
                return user_name
        else:
            # Extract user name from existing user selection (remove emoji prefix)
            return self.user_combo.currentText().replace('👤 ', '')

        # Return None if no valid user selection/input
        return None
        
    def generate_trials(self):
        """
        Generate randomized test trials based on selected test type and difficulty.

        This method creates the complete set of stimuli for the test session.
        Each trial contains the word to display, the color to display it in,
        timing constraints, and response tracking fields.

        The method adapts the trial generation based on:
        - Difficulty level (affects color set size and time limits)
        - Test type (affects word-color relationships)
        """
        test_type = self.current_test['test_type']
        difficulty = self.current_test['difficulty']

        # Step 1: Configure test parameters based on difficulty level
        if difficulty == "Easy":
            colors = ["RED", "BLUE", "GREEN", "YELLOW"]      # 4 colors
            time_limit = 3000  # 3 seconds per trial
        elif difficulty == "Medium":
            colors = ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "ORANGE"]  # 6 colors
            time_limit = 2500  # 2.5 seconds
        elif difficulty == "Hard":
            colors = ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "ORANGE", "PINK", "BROWN"]  # 8 colors
            time_limit = 2000  # 2 seconds
        else:  # Expert
            colors = ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "ORANGE", "PINK", "BROWN", "GRAY", "BLACK"]  # 10 colors
            time_limit = 1500  # 1.5 seconds

        # Step 2: Build word vocabulary based on test type
        words = colors.copy()  # Start with color words

        # Add emotional words for emotional Stroop variant
        if test_type == "Emotional Stroop (Words with Emotional Content)":
            emotional_words = ["LOVE", "HATE", "FEAR", "JOY", "SAD", "ANGRY", "CALM", "STRESS"]
            words.extend(emotional_words)

        # Step 3: Generate individual trials
        trials = []
        num_trials = self.current_test['num_trials']

        for i in range(num_trials):
            # Create word-color combinations based on test type
            if test_type == "Classic Stroop (Word vs Color)":
                # CLASSIC STROOP: Word and color are incongruent (different)
                # This creates the interference effect where word meaning conflicts with color perception
                word = random.choice(words)
                # Ensure color is different from word (if word is a color)
                color = random.choice([c for c in colors if c != word] if word in colors else colors)

            elif test_type == "Reverse Stroop (Color vs Word)":
                # REVERSE STROOP: Word matches color, but user reports the WORD instead of color
                # Tests attention to textual content over visual appearance
                color = random.choice(colors)
                word = color  # Word matches the color

            elif test_type == "Neutral (Color Only)":
                # NEUTRAL: Only color patches, no text
                # Baseline condition for measuring pure color recognition speed
                word = ""  # Empty word for color-only stimuli
                color = random.choice(colors)

            else:  # Emotional Stroop
                # EMOTIONAL STROOP: Words have emotional connotations
                # Measures interference from emotional processing
                word = random.choice(words)
                color = random.choice(colors)

            # Step 4: Create trial data structure
            trial = {
                'trial_num': i + 1,           # Trial sequence number (1-based)
                'word': word,                 # Text to display (empty for neutral)
                'color': color,               # Color to display text/stimulus in
                'time_limit': time_limit,     # Maximum response time in milliseconds
                'start_time': None,           # Timestamp when trial begins
                'response_time': None,        # User's response time in seconds
                'user_answer': None,          # User's selected response
                'correct': None              # Boolean: was answer correct?
            }
            trials.append(trial)

        # Step 5: Store generated trials in current test session
        self.current_test['trials'] = trials
        
    def show_test_screen(self):
        """Display the test interface"""
        self.clear_layout()
        
        # Progress bar with enhanced styling
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 3px solid rgba(255,255,255,0.4);
                border-radius: 8px;
                text-align: center;
                background: rgba(255,255,255,0.1);
                height: 25px;
                font-size: 12px;
                font-weight: bold;
                color: white;
            }

            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #48bb78, stop:0.5 #38a169, stop:1 #2f855a);
                border-radius: 5px;
            }
        """)
        self.progress_bar.setMaximum(self.current_test['num_trials'])
        self.progress_bar.setValue(0)
        self.main_layout.addWidget(self.progress_bar)
        
        # Trial counter with enhanced styling
        self.trial_label = QLabel(f"🎯 Trial 1 of {self.current_test['num_trials']}")
        self.trial_label.setAlignment(Qt.AlignCenter)
        self.trial_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.trial_label.setStyleSheet("""
            QLabel {
                color: #ffd700;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.15), stop:1 rgba(255,255,255,0.08));
                border: 2px solid rgba(255,215,0,0.3);
                border-radius: 10px;
                padding: 8px;
                margin: 5px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            }
        """)
        self.main_layout.addWidget(self.trial_label)
        
        # Stroop stimulus display with 3D effect
        self.stimulus_frame = QFrame()
        self.stimulus_frame.setObjectName("stimulus_frame")
        self.stimulus_frame.setStyleSheet("""
            QFrame#stimulus_frame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.98), stop:1 rgba(255,255,255,0.92));
                border: 4px solid qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4299e1, stop:1 #3182ce);
                border-radius: 20px;
                min-height: 150px;
            }
        """)
        # Add native Qt shadow effect
        self.add_shadow_effect(self.stimulus_frame, blur_radius=20, offset_x=0, offset_y=15, color=QColor(0, 0, 0, 100))
        
        stimulus_layout = QVBoxLayout(self.stimulus_frame)
        self.stimulus_label = QLabel()
        self.stimulus_label.setObjectName("stimulus_label")
        self.stimulus_label.setAlignment(Qt.AlignCenter)
        self.stimulus_label.setFont(QFont("Arial", 60, QFont.Bold))
        self.stimulus_label.setStyleSheet("""
            QLabel#stimulus_label {
                color: #2d3748;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                background: transparent;
            }
        """)
        stimulus_layout.addWidget(self.stimulus_label)
        
        self.main_layout.addWidget(self.stimulus_frame, alignment=Qt.AlignCenter)
        
        # Create response buttons
        self.create_response_buttons()
        
        # Timer display with enhanced styling
        self.timer_label = QLabel("⏱️ Time: 0.00s")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.timer_label.setStyleSheet("""
            QLabel {
                color: #ff6b6b;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.15), stop:1 rgba(255,255,255,0.08));
                border: 2px solid rgba(255,107,107,0.3);
                border-radius: 10px;
                padding: 8px;
                margin: 5px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
                font-weight: bold;
            }
        """)
        self.main_layout.addWidget(self.timer_label)
        
        # Start first trial
        self.show_next_trial()
        
    def create_response_buttons(self):
        """Create response buttons based on test type"""
        test_type = self.current_test['test_type']
        
        # Always reset the response layout to ensure clean recreation
        if hasattr(self, 'response_layout'):
            # Clear any existing buttons
            while self.response_layout.count():
                item = self.response_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            # Remove the layout from main layout if it exists
            if self.response_layout.parent():
                self.main_layout.removeItem(self.response_layout)
        
        # Create new layout
        self.response_layout = QHBoxLayout()
        self.response_layout.setSpacing(8)
        self.main_layout.addLayout(self.response_layout)
            
        colors = ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "ORANGE", "PINK", "BROWN", "GRAY", "BLACK"]
        
        if test_type == "Classic Stroop (Word vs Color)" or test_type == "Neutral (Color Only)":
            # Color response buttons with 3D effects
            for color in colors[:len(self.get_colors_for_difficulty())]:
                btn = QPushButton(color)
                color_hex = self.get_color_hex(color)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 {color_hex}, stop:1 {self.darken_color(color_hex)});
                        color: white;
                        border: 2px solid rgba(255,255,255,0.3);
                        border-radius: 10px;
                        padding: 12px 20px;
                        font-size: 14px;
                        font-weight: bold;
                        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
                        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                        min-width: 80px;
                        margin: 2px;
                    }}
                    
                    QPushButton:hover {{
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 {self.lighten_color(color_hex)}, stop:1 {color_hex});
                        transform: translateY(-3px);
                        box-shadow: 0 8px 16px rgba(0,0,0,0.4);
                    }}
                    
                    QPushButton:pressed {{
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 {self.darken_color(color_hex)}, stop:1 {self.darken_color(self.darken_color(color_hex))});
                        transform: translateY(0px);
                        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                    }}
                """)
                btn.clicked.connect(lambda checked, c=color: self.process_response(c))
                self.response_layout.addWidget(btn)
        elif test_type == "Reverse Stroop (Color vs Word)":
            # Word response buttons with 3D effects
            words = self.get_colors_for_difficulty()
            for word in words:
                btn = QPushButton(word)
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #667eea, stop:1 #5a67d8);
                        color: white;
                        border: 2px solid rgba(255,255,255,0.3);
                        border-radius: 10px;
                        padding: 12px 20px;
                        font-size: 14px;
                        font-weight: bold;
                        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
                        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                        min-width: 80px;
                        margin: 2px;
                    }
                    
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #7c8ce8, stop:1 #667eea);
                        transform: translateY(-3px);
                        box-shadow: 0 8px 16px rgba(0,0,0,0.4);
                    }
                    
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #5a67d8, stop:1 #4c51bf);
                        transform: translateY(0px);
                        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                    }
                """)
                btn.clicked.connect(lambda checked, w=word: self.process_response(w))
                self.response_layout.addWidget(btn)
        else:  # Emotional Stroop
            # Mixed responses with 3D effects
            responses = self.get_colors_for_difficulty() + ["LOVE", "HATE", "FEAR", "JOY"]
            for response in responses:
                btn = QPushButton(response)
                if response in colors:
                    color_hex = self.get_color_hex(response)
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {color_hex}, stop:1 {self.darken_color(color_hex)});
                            color: white;
                            border: 2px solid rgba(255,255,255,0.3);
                            border-radius: 10px;
                            padding: 12px 20px;
                            font-size: 14px;
                            font-weight: bold;
                            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
                            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                            min-width: 80px;
                            margin: 2px;
                        }}
                        
                        QPushButton:hover {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {self.lighten_color(color_hex)}, stop:1 {color_hex});
                            transform: translateY(-3px);
                            box-shadow: 0 8px 16px rgba(0,0,0,0.4);
                        }}
                        
                        QPushButton:pressed {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {self.darken_color(color_hex)}, stop:1 {self.darken_color(self.darken_color(color_hex))});
                            transform: translateY(0px);
                            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                        }}
                    """)
                else:
                    btn.setStyleSheet("""
                        QPushButton {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ed64a6, stop:1 #d53f8c);
                            color: white;
                            border: 2px solid rgba(255,255,255,0.3);
                            border-radius: 10px;
                            padding: 12px 20px;
                            font-size: 14px;
                            font-weight: bold;
                            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
                            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                            min-width: 80px;
                            margin: 2px;
                        }
                        
                        QPushButton:hover {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #fbb6ce, stop:1 #ed64a6);
                            transform: translateY(-3px);
                            box-shadow: 0 8px 16px rgba(0,0,0,0.4);
                        }
                        
                        QPushButton:pressed {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #d53f8c, stop:1 #b83280);
                            transform: translateY(0px);
                            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                        }
                    """)
                btn.clicked.connect(lambda checked, r=response: self.process_response(r))
                self.response_layout.addWidget(btn)
                
    def get_color_hex(self, color_name):
        """
        Convert color name to corresponding hex color code for UI styling.

        This utility method provides consistent color mapping for the Stroop test
        stimuli and UI elements. The colors are chosen to be clearly distinguishable
        and appropriate for psychological testing.

        Args:
            color_name (str): Color name (e.g., "RED", "BLUE")

        Returns:
            str: Hex color code (e.g., "#e53e3e" for red)

        Color Palette:
        - RED, BLUE, GREEN, YELLOW: Primary test colors
        - PURPLE, ORANGE, PINK, BROWN: Extended colors for higher difficulties
        - GRAY, BLACK: Expert level additions
        """
        color_map = {
            "RED": "#e53e3e",      # Bright red for good visibility
            "BLUE": "#3182ce",    # Professional blue
            "GREEN": "#38a169",   # Success green
            "YELLOW": "#d69e2e",  # Warm yellow
            "PURPLE": "#805ad5",  # Rich purple
            "ORANGE": "#dd6b20",  # Vibrant orange
            "PINK": "#d53f8c",    # Modern pink
            "BROWN": "#a0522d",   # Earthy brown
            "GRAY": "#718096",    # Neutral gray
            "BLACK": "#2d3748"    # Dark slate
        }
        return color_map.get(color_name, "#4299e1")  # Default fallback color
        
    def lighten_color(self, hex_color):
        """Lighten a hex color"""
        # Simple color lightening (in a real app you'd use a proper color library)
        return hex_color  # For simplicity, return same color
        
    def darken_color(self, hex_color):
        """Darken a hex color"""
        # Simple color darkening (in a real app you'd use a proper color library)
        return hex_color  # For simplicity, return same color
        
    def get_colors_for_difficulty(self):
        """Get color list based on difficulty"""
        difficulty = self.current_test['difficulty']
        if difficulty == "Easy":
            return ["RED", "BLUE", "GREEN", "YELLOW"]
        elif difficulty == "Medium":
            return ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "ORANGE"]
        elif difficulty == "Hard":
            return ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "ORANGE", "PINK", "BROWN"]
        else:  # Expert
            return ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "ORANGE", "PINK", "BROWN", "GRAY", "BLACK"]
            
    def show_next_trial(self):
        """Display the next trial stimulus"""
        if self.current_test['current_trial'] >= self.current_test['num_trials']:
            self.finish_test()
            return
            
        trial = self.current_test['trials'][self.current_test['current_trial']]
        
        # Update progress
        self.progress_bar.setValue(self.current_test['current_trial'] + 1)
        self.trial_label.setText(f"🎯 Trial {self.current_test['current_trial'] + 1} of {self.current_test['num_trials']}")
        
        # Set stimulus
        if trial['word']:
            self.stimulus_label.setText(trial['word'])
        else:
            self.stimulus_label.setText("■")  # Color square for neutral test
            
        # Set color
        color_name = trial['color']
        if color_name == "RED":
            color = QColor(Qt.red)
        elif color_name == "BLUE":
            color = QColor(Qt.blue)
        elif color_name == "GREEN":
            color = QColor(Qt.green)
        elif color_name == "YELLOW":
            color = QColor(Qt.yellow)
        elif color_name == "PURPLE":
            color = QColor(128, 0, 128)
        elif color_name == "ORANGE":
            color = QColor(255, 165, 0)
        elif color_name == "PINK":
            color = QColor(255, 192, 203)
        elif color_name == "BROWN":
            color = QColor(165, 42, 42)
        elif color_name == "GRAY":
            color = QColor(Qt.gray)
        elif color_name == "BLACK":
            color = QColor(Qt.black)
            
        palette = self.stimulus_label.palette()
        palette.setColor(QPalette.WindowText, color)
        self.stimulus_label.setPalette(palette)
        
        # Start timer
        trial['start_time'] = time.time()
        self.start_time = time.time()
        
        # Update timer display
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(50)  # Update every 50ms
        
        # Set timeout timer
        self.timeout_timer = QTimer()
        self.timeout_timer.setSingleShot(True)
        self.timeout_timer.timeout.connect(lambda: self.process_response(None))  # Timeout
        self.timeout_timer.start(trial['time_limit'])
        
    def update_timer(self):
        """Update the timer display"""
        elapsed = time.time() - self.start_time
        self.timer_label.setText(f"⏱️ Time: {elapsed:.2f}s")
        
    def process_response(self, response):
        """
        Process a user's response to the current trial and prepare for the next trial.

        This method handles the complete response processing pipeline:
        1. Stops timing mechanisms
        2. Calculates response time
        3. Evaluates answer correctness
        4. Updates test statistics
        5. Advances to next trial

        Args:
            response (str): User's selected answer (color name or word)
        """
        # Step 1: Stop all active timers to prevent further timing
        if hasattr(self, 'timer'):
            self.timer.stop()  # Stop the display timer
        if hasattr(self, 'timeout_timer'):
            self.timeout_timer.stop()  # Stop the timeout timer

        # Step 2: Get current trial data and capture end time
        trial = self.current_test['trials'][self.current_test['current_trial']]
        end_time = time.time()

        # Step 3: Calculate response time (time from stimulus onset to response)
        if trial['start_time']:
            response_time = end_time - trial['start_time']
        else:
            response_time = 0  # Fallback for timing errors

        # Step 4: Record response data in trial structure
        trial['response_time'] = response_time
        trial['user_answer'] = response

        # Step 5: Determine correct answer based on test type
        test_type = self.current_test['test_type']
        if test_type == "Classic Stroop (Word vs Color)" or test_type == "Neutral (Color Only)":
            # User should identify the DISPLAY color
            correct_answer = trial['color']
        elif test_type == "Reverse Stroop (Color vs Word)":
            # User should identify the WORD (which matches the color)
            correct_answer = trial['word']
        else:  # Emotional Stroop
            # User should identify the DISPLAY color (ignoring emotional word content)
            correct_answer = trial['color']

        # Step 6: Evaluate correctness and update statistics
        trial['correct'] = (response == correct_answer)

        if trial['correct']:
            self.current_test['correct_answers'] += 1
        self.current_test['total_time'] += response_time

        # Step 7: Advance to next trial
        self.current_test['current_trial'] += 1
        self.show_next_trial()
        
    def finish_test(self):
        """
        Complete the test session and transition to results display.

        This method finalizes the test session by:
        1. Recording completion timestamp
        2. Calculating final performance statistics
        3. Persisting results to user data file
        4. Displaying comprehensive results screen

        The method handles the transition from active testing to results review,
        ensuring all data is properly saved and statistics are calculated.
        """
        # Step 1: Record test completion timestamp
        self.current_test['end_time'] = datetime.now().isoformat()

        # Step 2: Calculate final performance metrics
        accuracy = (self.current_test['correct_answers'] / self.current_test['num_trials']) * 100
        avg_time = self.current_test['total_time'] / self.current_test['num_trials']

        # Step 3: Persist results to long-term storage
        self.save_test_results()

        # Step 4: Display comprehensive results screen
        self.show_results_screen(accuracy, avg_time)
        
    def show_results_screen(self, accuracy, avg_time):
        """Display test results"""
        self.clear_layout()
        
        # Results title with 3D effect using Qt shadows
        title = QLabel("🎉 Test Results")
        title.setObjectName("title")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel#title {
                color: #ffd700;
                font-weight: bold;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.15), stop:1 rgba(255,255,255,0.08));
                border: 2px solid rgba(255,215,0,0.3);
                border-radius: 20px;
                padding: 15px;
                margin: 10px;
            }
        """)
        # Add native Qt shadow effect
        self.add_shadow_effect(title, blur_radius=15, offset_x=0, offset_y=8, color=QColor(0, 0, 0, 120))
        self.main_layout.addWidget(title)
        
        # Results summary with enhanced styling
        results_group = QGroupBox("📊 Summary")
        results_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
                border: 3px solid rgba(255,255,255,0.4);
                border-radius: 15px;
                margin-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(72,187,120,0.2), stop:1 rgba(56,161,105,0.1));
                padding: 20px;
            }
        """)
        # Add native Qt shadow effect
        self.add_shadow_effect(results_group, blur_radius=12, offset_x=0, offset_y=8, color=QColor(0, 0, 0, 100))
        results_layout = QVBoxLayout()
        results_layout.setSpacing(12)
        
        # Enhanced result labels
        user_label = QLabel(f"👤 User: {self.current_test['user']}")
        user_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffd700;")
        results_layout.addWidget(user_label)
        
        test_label = QLabel(f"🎮 Test Type: {self.current_test['test_type']}")
        test_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        results_layout.addWidget(test_label)
        
        diff_label = QLabel(f"📊 Difficulty: {self.current_test['difficulty']}")
        diff_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        results_layout.addWidget(diff_label)
        
        trials_label = QLabel(f"🎯 Trials Completed: {self.current_test['num_trials']}")
        trials_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        results_layout.addWidget(trials_label)
        
        correct_label = QLabel(f"✅ Correct Answers: {self.current_test['correct_answers']}")
        correct_label.setStyleSheet("font-size: 16px; color: #48bb78; font-weight: bold;")
        results_layout.addWidget(correct_label)
        
        acc_label = QLabel(f"🎯 Accuracy: {accuracy:.1f}%")
        acc_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {'#48bb78' if accuracy >= 70 else '#ed8936' if accuracy >= 50 else '#e53e3e'};")
        results_layout.addWidget(acc_label)
        
        time_label = QLabel(f"⏱️ Average Response Time: {avg_time:.2f}s")
        time_label.setStyleSheet(f"font-size: 16px; color: {'#48bb78' if avg_time <= 2.0 else '#ed8936' if avg_time <= 3.0 else '#e53e3e'};")
        results_layout.addWidget(time_label)
        
        results_group.setLayout(results_layout)
        self.main_layout.addWidget(results_group)
        
        # Performance rating with enhanced styling
        rating = self.get_performance_rating(accuracy, avg_time)
        rating_label = QLabel(f"🏆 Performance Rating: {rating}")
        rating_label.setFont(QFont("Arial", 20, QFont.Bold))
        rating_label.setAlignment(Qt.AlignCenter)
        
        # Color code rating
        if rating == "Excellent":
            rating_color = "#ffd700"
        elif rating == "Very Good":
            rating_color = "#48bb78"
        elif rating == "Good":
            rating_color = "#4299e1"
        elif rating == "Fair":
            rating_color = "#ed8936"
        else:
            rating_color = "#e53e3e"
            
        rating_label.setStyleSheet(f"""
            QLabel {{
                color: {rating_color};
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.15), stop:1 rgba(255,255,255,0.08));
                border: 2px solid rgba(255,215,0,0.3);
                border-radius: 15px;
                padding: 12px;
                margin: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                box-shadow: 0 6px 12px rgba(0,0,0,0.2);
            }}
        """)
        self.main_layout.addWidget(rating_label)
        
        # Navigation buttons with enhanced styling
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        restart_btn = QPushButton("🔄 Take Another Test")
        restart_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4299e1, stop:1 #3182ce);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #63b3ed, stop:1 #4299e1);
                transform: translateY(-2px);
                box-shadow: 0 8px 15px rgba(0,0,0,0.3);
            }
        """)
        restart_btn.clicked.connect(self.show_welcome_screen)
        button_layout.addWidget(restart_btn)
        
        stats_btn = QPushButton("📈 View Full Statistics")
        stats_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #48bb78, stop:1 #38a169);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #68d391, stop:1 #48bb78);
                transform: translateY(-2px);
                box-shadow: 0 8px 15px rgba(0,0,0,0.3);
            }
        """)
        stats_btn.clicked.connect(self.show_statistics)
        button_layout.addWidget(stats_btn)
        
        exit_btn = QPushButton("❌ Exit")
        exit_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e53e3e, stop:1 #c53030);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fc8181, stop:1 #e53e3e);
                transform: translateY(-2px);
                box-shadow: 0 8px 15px rgba(0,0,0,0.3);
            }
        """)
        exit_btn.clicked.connect(self.close)
        button_layout.addWidget(exit_btn)
        
        self.main_layout.addLayout(button_layout)
        
    def get_performance_rating(self, accuracy, avg_time):
        """Calculate performance rating based on accuracy and response time"""
        if accuracy >= 90 and avg_time <= 1.5:
            return "Excellent"
        elif accuracy >= 80 and avg_time <= 2.0:
            return "Very Good"
        elif accuracy >= 70 and avg_time <= 2.5:
            return "Good"
        elif accuracy >= 60 and avg_time <= 3.0:
            return "Fair"
        else:
            return "Needs Improvement"
            
    def show_statistics(self):
        """Display user statistics"""
        self.clear_layout()
        
        # Use the user from the current test session instead of UI elements
        user_name = self.current_test.get('user') if self.current_test else None
        
        # If no current test user, try to get from stored data or show error
        if not user_name:
            # Try to get any available user from the data
            if self.user_data:
                user_name = list(self.user_data.keys())[0]  # Get first available user
            else:
                QMessageBox.information(self, "No Data", "No user data available. Please take a test first.")
                self.show_welcome_screen()
                return
        
        if user_name not in self.user_data:
            QMessageBox.information(self, "No Data", f"No statistics available for user '{user_name}'.")
            self.show_welcome_screen()
            return
            
        user_stats = self.user_data[user_name]
        
        # Statistics title with 3D effect using Qt shadows
        title = QLabel(f"📈 Statistics for {user_name}")
        title.setObjectName("title")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel#title {
                color: #ffd700;
                font-weight: bold;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.15), stop:1 rgba(255,255,255,0.08));
                border: 2px solid rgba(255,215,0,0.3);
                border-radius: 20px;
                padding: 15px;
                margin: 10px;
            }
        """)
        # Add native Qt shadow effect
        self.add_shadow_effect(title, blur_radius=15, offset_x=0, offset_y=8, color=QColor(0, 0, 0, 120))
        self.main_layout.addWidget(title)
        
        # Overall stats with enhanced styling
        overall_group = QGroupBox("📊 Overall Performance")
        overall_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                border: 3px solid rgba(255,255,255,0.4);
                border-radius: 12px;
                margin-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.15), stop:1 rgba(255,255,255,0.08));
                padding: 15px;
            }
        """)
        # Add native Qt shadow effect
        self.add_shadow_effect(overall_group, blur_radius=10, offset_x=0, offset_y=6, color=QColor(0, 0, 0, 80))
        overall_layout = QVBoxLayout()
        overall_layout.setSpacing(8)
        
        overall_layout.addWidget(QLabel(f"🎮 Total Tests Taken: {user_stats.get('total_tests', 0)}"))
        overall_layout.addWidget(QLabel(f"🎯 Average Accuracy: {user_stats.get('avg_accuracy', 0):.1f}%"))
        overall_layout.addWidget(QLabel(f"⏱️ Average Response Time: {user_stats.get('avg_response_time', 0):.2f}s"))
        overall_layout.addWidget(QLabel(f"🏆 Best Accuracy: {user_stats.get('best_accuracy', 0):.1f}%"))
        
        overall_group.setLayout(overall_layout)
        self.main_layout.addWidget(overall_group)
        
        # Recent tests with enhanced styling
        if 'recent_tests' in user_stats and user_stats['recent_tests']:
            recent_group = QGroupBox("🕒 Recent Tests")
            recent_group.setStyleSheet("""
                QGroupBox {
                    font-size: 16px;
                    font-weight: bold;
                    color: #ffffff;
                    border: 3px solid rgba(255,255,255,0.4);
                    border-radius: 12px;
                    margin-top: 15px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255,255,255,0.15), stop:1 rgba(255,255,255,0.08));
                    box-shadow: 0 6px 12px rgba(0,0,0,0.2);
                    padding: 15px;
                }
            """)
            recent_layout = QVBoxLayout()
            recent_layout.setSpacing(5)
            
            for i, test in enumerate(user_stats['recent_tests'][-5:]):  # Show last 5 tests
                test_info = f"📅 {test['date']}: {test['test_type']} - {test['accuracy']:.1f}% ({test['difficulty']})"
                test_label = QLabel(test_info)
                test_label.setStyleSheet("color: #e2e8f0; padding: 2px;")
                recent_layout.addWidget(test_label)
                
            recent_group.setLayout(recent_layout)
            self.main_layout.addWidget(recent_group)
        
        # Back button with enhanced styling
        back_btn = QPushButton("⬅️ Back to Main Menu")
        back_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #718096, stop:1 #4a5568);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a0aec0, stop:1 #718096);
                transform: translateY(-2px);
                box-shadow: 0 8px 15px rgba(0,0,0,0.3);
            }
        """)
        back_btn.clicked.connect(self.show_welcome_screen)
        self.main_layout.addWidget(back_btn, alignment=Qt.AlignCenter)
        
    def clear_layout(self):
        """
        Clear all widgets and sub-layouts from the main layout container.

        This method recursively removes and deletes all child widgets and layouts
        from the main layout. It's used when switching between different screens
        (welcome → test → results → statistics) to ensure a clean slate.

        The method properly handles Qt's parent-child relationships and memory
        management by calling deleteLater() on widgets.
        """
        # Iterate through all items in the main layout
        while self.main_layout.count():
            # Remove the first item from layout
            child = self.main_layout.takeAt(0)

            # If it's a widget, schedule it for deletion
            if child.widget():
                child.widget().deleteLater()
            # If it's a sub-layout, recursively clear it
            elif child.layout():
                self.clear_sub_layout(child.layout())
                
    def clear_sub_layout(self, layout):
        """Clear sub-layout recursively"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_sub_layout(child.layout())
                
    def load_user_data(self):
        """
        Load persistent user data from JSON file.

        Attempts to load user profiles, statistics, and test history from
        the local data file. If the file doesn't exist or is corrupted,
        initializes with empty data structure.

        The data includes:
        - User profiles and settings
        - Historical test results
        - Performance statistics
        - Test preferences

        File: stroop_user_data.json (created in application directory)
        """
        try:
            data_file = 'stroop_user_data.json'
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    self.user_data = json.load(f)
                    print(f"Loaded user data for {len(self.user_data)} users")
            else:
                print("No existing user data file found, starting fresh")
                self.user_data = {}
        except Exception as e:
            print(f"Error loading user data: {e}")
            # Initialize with empty data structure on error
            self.user_data = {}
            
    def save_test_results(self):
        """
        Persist completed test results to user data file.

        This method updates the user's statistical profile with the results
        of the current test session. It maintains running totals, calculates
        averages, tracks personal bests, and preserves detailed trial data.

        The method handles:
        - User profile creation for new users
        - Statistical aggregation across all tests
        - Recent test history (last 10 tests)
        - Detailed trial-by-trial data preservation
        - Error handling for file operations
        """
        user_name = self.current_test['user']

        # Step 1: Initialize user profile if this is a new user
        if user_name not in self.user_data:
            self.user_data[user_name] = {
                'total_tests': 0,           # Total number of completed tests
                'total_correct': 0,         # Cumulative correct answers across all tests
                'total_trials': 0,          # Total number of trials attempted
                'total_time': 0.0,          # Total response time across all tests
                'avg_accuracy': 0.0,        # Overall accuracy percentage
                'avg_response_time': 0.0,   # Average response time per trial
                'best_accuracy': 0.0,       # Personal best accuracy percentage
                'recent_tests': [],         # List of recent test summaries
                'all_tests': []             # Complete detailed test data
            }

        # Step 2: Get reference to user's statistical profile
        user_stats = self.user_data[user_name]

        # Step 3: Calculate current test performance metrics
        current_accuracy = (self.current_test['correct_answers'] / self.current_test['num_trials']) * 100
        current_avg_time = self.current_test['total_time'] / self.current_test['num_trials']

        # Step 4: Update cumulative statistics
        user_stats['total_tests'] += 1
        user_stats['total_correct'] += self.current_test['correct_answers']
        user_stats['total_trials'] += self.current_test['num_trials']
        user_stats['total_time'] += self.current_test['total_time']

        # Step 5: Recalculate overall averages
        user_stats['avg_accuracy'] = (user_stats['total_correct'] / user_stats['total_trials']) * 100
        user_stats['avg_response_time'] = user_stats['total_time'] / user_stats['total_trials']
        user_stats['best_accuracy'] = max(user_stats['best_accuracy'], current_accuracy)

        # Step 6: Add current test to recent tests history
        test_summary = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),  # Formatted timestamp
            'test_type': self.current_test['test_type'],        # Test variant used
            'difficulty': self.current_test['difficulty'],     # Difficulty level
            'accuracy': round(current_accuracy, 1),           # Accuracy percentage
            'avg_time': round(current_avg_time, 2),           # Average response time
            'trials': self.current_test['num_trials']          # Number of trials
        }
        user_stats['recent_tests'].append(test_summary)

        # Step 7: Maintain recent tests history (keep only last 10)
        if len(user_stats['recent_tests']) > 10:
            user_stats['recent_tests'] = user_stats['recent_tests'][-10:]

        # Step 8: Preserve complete detailed trial data for research purposes
        if 'all_tests' not in user_stats:
            user_stats['all_tests'] = []
        user_stats['all_tests'].append(self.current_test.copy())

        # Step 9: Persist data to JSON file with error handling
        try:
            with open('stroop_user_data.json', 'w', encoding='utf-8') as f:
                json.dump(self.user_data, f, indent=2, ensure_ascii=False)
            print(f"Successfully saved test results for user: {user_name}")
        except Exception as e:
            error_msg = f"Could not save user data: {str(e)}"
            print(f"ERROR: {error_msg}")
            QMessageBox.warning(self, "Save Error", error_msg)

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Main application entry point.

    Initializes the Qt application framework, creates the main StroopTest window,
    displays the interface, and starts the event loop. The application will run
    until the user closes the main window.

    This follows standard Qt application structure:
    1. Create QApplication instance
    2. Create and configure main window
    3. Show the window
    4. Start event loop with app.exec_()
    5. Clean exit with sys.exit()
    """

    # Step 1: Create Qt application instance
    # QApplication manages the GUI application's control flow and main settings
    app = QApplication(sys.argv)

    # Step 2: Create main application window
    # This initializes the StroopTest class with all UI components and data
    window = StroopTest()

    # Step 3: Display the main window
    # Makes the window visible to the user
    window.show()

    # Step 4: Start the Qt event loop
    # This is the main application loop that processes user interactions,
    # updates the UI, and handles system events until the application exits
    sys.exit(app.exec_())

# ============================================================================
# END OF APPLICATION
# ============================================================================
