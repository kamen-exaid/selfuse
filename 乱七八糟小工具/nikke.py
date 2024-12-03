import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout
)
from PyQt5.QtGui import QFont


class TicketCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("票据交货计算器")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

        # 固定的生产速率和兑换规则
        self.production_rates = {"blue": 7283, "yellow": 767, "red": 70}
        self.blue_to_red = 100 / 3350000
        self.blue_to_yellow = 197000 / 3350000

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Input fields
        font = QFont("Arial", 12)

        self.blue_stock_label = QLabel("当前蓝票库存:")
        self.blue_stock_label.setFont(font)
        self.blue_stock_input = QLineEdit()
        self.blue_stock_input.setFont(font)
        form_layout.addRow(self.blue_stock_label, self.blue_stock_input)

        self.yellow_stock_label = QLabel("当前黄票库存:")
        self.yellow_stock_label.setFont(font)
        self.yellow_stock_input = QLineEdit()
        self.yellow_stock_input.setFont(font)
        form_layout.addRow(self.yellow_stock_label, self.yellow_stock_input)

        self.red_stock_label = QLabel("当前红票库存:")
        self.red_stock_label.setFont(font)
        self.red_stock_input = QLineEdit()
        self.red_stock_input.setFont(font)
        form_layout.addRow(self.red_stock_label, self.red_stock_input)

        self.blue_demand_label = QLabel("每次需求蓝票:")
        self.blue_demand_label.setFont(font)
        self.blue_demand_input = QLineEdit()
        self.blue_demand_input.setFont(font)
        form_layout.addRow(self.blue_demand_label, self.blue_demand_input)

        self.yellow_demand_label = QLabel("每次需求黄票:")
        self.yellow_demand_label.setFont(font)
        self.yellow_demand_input = QLineEdit()
        self.yellow_demand_input.setFont(font)
        form_layout.addRow(self.yellow_demand_label, self.yellow_demand_input)

        self.red_demand_label = QLabel("每次需求红票:")
        self.red_demand_label.setFont(font)
        self.red_demand_input = QLineEdit()
        self.red_demand_input.setFont(font)
        form_layout.addRow(self.red_demand_label, self.red_demand_input)

        layout.addLayout(form_layout)

        # Buttons
        self.calculate_button = QPushButton("计算")
        self.calculate_button.setFont(font)
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)

        self.result_label = QLabel("结果:")
        self.result_label.setFont(font)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def calculate(self):
        try:
            # Parse inputs
            blue_stock = int(self.blue_stock_input.text())
            yellow_stock = int(self.yellow_stock_input.text())
            red_stock = int(self.red_stock_input.text())
            blue_demand = int(self.blue_demand_input.text())
            yellow_demand = int(self.yellow_demand_input.text())
            red_demand = int(self.red_demand_input.text())

            # Initialize variables
            total_deliveries = 0
            yellow_needed = 0
            red_needed = 0

            while True:
                # Check how many full deliveries can be made with current stock
                current_deliveries = min(
                    blue_stock // blue_demand,
                    yellow_stock // yellow_demand,
                    red_stock // red_demand
                )

                # If we can complete at least one delivery, update stock and count
                if current_deliveries > 0:
                    total_deliveries += current_deliveries
                    blue_stock -= current_deliveries * blue_demand
                    yellow_stock -= current_deliveries * yellow_demand
                    red_stock -= current_deliveries * red_demand
                else:
                    # If we can't complete a delivery, calculate missing tickets
                    missing_yellow = max(0, yellow_demand - yellow_stock)
                    missing_red = max(0, red_demand - red_stock)

                    # Calculate blue needed for yellow and round to whole tickets
                    blue_for_yellow = int((missing_yellow / self.blue_to_yellow) + 0.9999)

                    # Calculate blue needed for red, ensure red is exchanged in multiples of 100
                    required_red = (missing_red // 100 + (1 if missing_red % 100 != 0 else 0)) * 100
                    blue_for_red = int((required_red / 100) / self.blue_to_red)

                    # If we have enough blue tickets to cover the missing items, trade and continue
                    if blue_for_yellow + blue_for_red <= blue_stock:
                        yellow_stock += missing_yellow
                        red_stock += required_red
                        yellow_needed += missing_yellow
                        red_needed += required_red
                        blue_stock -= (blue_for_yellow + blue_for_red)
                    else:
                        # If not enough blue tickets, break the loop
                        break

            # Output the results
            if total_deliveries > 0:
                self.result_label.setText(
                    f"结果: 可以交货 {total_deliveries} 次，需要兑换 {yellow_needed} 黄票 和 {red_needed} 红票。"
                )
            else:
                # Calculate waiting time for the next delivery
                missing_blue = max(0, blue_demand - blue_stock)
                time_for_blue = missing_blue / self.production_rates["blue"]
                time_for_yellow = max(0, yellow_demand - yellow_stock) / self.production_rates["yellow"]
                time_for_red = max(0, red_demand - red_stock) / self.production_rates["red"]

                wait_time = max(time_for_blue, time_for_yellow, time_for_red)

                self.result_label.setText(f"结果: 库存不足，需等待 {wait_time:.2f} 分钟才能完成一次交货。")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TicketCalculator()
    window.show()
    sys.exit(app.exec_())
