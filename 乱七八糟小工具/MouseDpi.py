import sys
from qtpy.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox
)

class DpiCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DPI Calculator")
        self.setGeometry(100, 100, 400, 200)
        
        # Layouts
        layout = QVBoxLayout()

        # Input fields for current and target resolutions
        self.resolution_input = self.create_input_field("Current Resolution (e.g., 2560x1440):")
        self.target_resolution_input = self.create_input_field("Target Resolution (e.g., 1920x1080):")
        self.base_dpi_input = self.create_input_field("Base DPI (e.g., 2000):")

        # Calculate Button
        self.calculate_button = QPushButton("Calculate Target DPI")
        self.calculate_button.clicked.connect(self.calculate_dpi)
        layout.addWidget(self.calculate_button)

        # Result Label
        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def create_input_field(self, label_text):
        """Helper to create a labeled input field."""
        layout = QHBoxLayout()
        label = QLabel(label_text)
        input_field = QLineEdit()
        layout.addWidget(label)
        layout.addWidget(input_field)
        self.layout().addLayout(layout) if self.layout() else None
        return input_field

    def parse_resolution(self, resolution_text):
        """Parse resolution input like '2560x1440' into width and height."""
        try:
            width, height = map(int, resolution_text.lower().split("x"))
            return width, height
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid resolution format. Use 'widthxheight'.")
            return None, None

    def calculate_dpi(self):
        """Calculate and display the target DPI."""
        # Parse inputs
        current_res = self.resolution_input.text()
        target_res = self.target_resolution_input.text()
        base_dpi = self.base_dpi_input.text()

        try:
            base_dpi = int(base_dpi)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid Base DPI. Enter an integer.")
            return

        current_width, _ = self.parse_resolution(current_res)
        target_width, _ = self.parse_resolution(target_res)

        if not current_width or not target_width:
            return

        # Calculate target DPI
        target_dpi = base_dpi * (target_width / current_width)

        # Update the result label
        self.result_label.setText(f"Target DPI: {target_dpi:.2f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = DpiCalculator()
    calculator.show()
    sys.exit(app.exec_())
