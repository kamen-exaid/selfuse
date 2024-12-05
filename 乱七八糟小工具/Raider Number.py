import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QProgressBar, QHBoxLayout
)
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta


class TaskCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.language = "zh"  # 默认语言为中文
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.translate("任务计算器"))
        self.setGeometry(100, 100, 400, 400)

        # 主布局
        layout = QVBoxLayout()

        # 创建输入部分
        self.label_y = QLabel(self.translate("总任务数 Y:"))
        self.input_y = QLineEdit(self)
        layout.addWidget(self.label_y)
        layout.addWidget(self.input_y)

        self.label_x = QLabel(self.translate("当前任务数 X:"))
        self.input_x = QLineEdit(self)
        layout.addWidget(self.label_x)
        layout.addWidget(self.input_x)

        self.label_minutes = QLabel(self.translate("距离下次刷新任务的分钟数:"))
        self.input_minutes = QLineEdit(self)
        layout.addWidget(self.label_minutes)
        layout.addWidget(self.input_minutes)

        # 创建计算按钮
        self.calc_button = QPushButton(self.translate("计算"), self)
        self.calc_button.clicked.connect(self.calculate)
        layout.addWidget(self.calc_button)

        # 创建进度条
        self.progress_label = QLabel(self.translate("刷新进度:"))
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)

        # 创建语言切换按钮
        lang_layout = QHBoxLayout()
        self.zh_button = QPushButton("中文", self)
        self.zh_button.clicked.connect(lambda: self.set_language("zh"))
        self.en_button = QPushButton("English", self)
        self.en_button.clicked.connect(lambda: self.set_language("en"))
        lang_layout.addWidget(self.zh_button)
        lang_layout.addWidget(self.en_button)
        layout.addLayout(lang_layout)

        # 设置主布局
        self.setLayout(layout)

    def translate(self, text):
        """多语言翻译"""
        translations = {
            "任务计算器": {"en": "Task Calculator", "zh": "任务计算器"},
            "总任务数 Y:": {"en": "Total Tasks Y:", "zh": "总任务数 Y:"},
            "当前任务数 X:": {"en": "Current Tasks X:", "zh": "当前任务数 X:"},
            "距离下次刷新任务的分钟数:": {"en": "Minutes to Next Refresh:", "zh": "距离下次刷新任务的分钟数:"},
            "计算": {"en": "Calculate", "zh": "计算"},
            "刷新进度:": {"en": "Refresh Progress:", "zh": "刷新进度:"},
            "输入错误": {"en": "Input Error", "zh": "输入错误"},
            "请确保所有输入值为有效的整数。": {"en": "Please ensure all input values are valid integers.", "zh": "请确保所有输入值为有效的整数。"},
            "计算结果": {"en": "Calculation Result", "zh": "计算结果"},
        }
        return translations.get(text, {}).get(self.language, text)

    def set_language(self, lang):
        """设置语言并刷新UI"""
        self.language = lang
        self.refresh_ui()

    def refresh_ui(self):
        """根据语言刷新界面文本"""
        self.setWindowTitle(self.translate("任务计算器"))
        self.label_y.setText(self.translate("总任务数 Y:"))
        self.label_x.setText(self.translate("当前任务数 X:"))
        self.label_minutes.setText(self.translate("距离下次刷新任务的分钟数:"))
        self.calc_button.setText(self.translate("计算"))
        self.progress_label.setText(self.translate("刷新进度:"))

    def calculate(self):
        try:
            # 获取用户输入
            y = int(self.input_y.text())
            x = int(self.input_x.text())
            next_refresh_minutes = int(self.input_minutes.text())

            # 固定参数
            refresh_amount = 11
            max_storage = y - 1
            hours_per_refresh = 6

            # 当前时间和刷新时间
            current_time = datetime.now()
            next_morning_time = datetime.combine(
                current_time.date() + timedelta(days=1), datetime.min.time()
            ) + timedelta(hours=10, minutes=10)
            start_time = current_time + timedelta(minutes=next_refresh_minutes)
            time_diff = next_morning_time - start_time

            # 计算刷新次数
            refresh_count = int(time_diff.total_seconds() // (hours_per_refresh * 3600))
            tasks_to_complete = 0
            simulated_tasks = x

            # 更新进度条
            self.progress_bar.setMaximum(refresh_count)
            for i in range(refresh_count):
                simulated_tasks += refresh_amount
                if simulated_tasks > max_storage:
                    tasks_to_complete += simulated_tasks - max_storage
                    simulated_tasks = max_storage
                self.progress_bar.setValue(i + 1)

            # 计算时间信息
            minutes_to_target = int(time_diff.total_seconds() // 60)

            # 构造结果信息
            result_message = (
                f"{self.translate('当前时间')}: {current_time.strftime('%H:%M:%S')}\n"
                f"{self.translate('距离明天10:10还有')} {minutes_to_target} {self.translate('分钟')}。\n"
                f"{self.translate('在此期间，你可以刷新')} {refresh_count} {self.translate('次新任务（每次刷新')} {refresh_amount} {self.translate('个任务）')}。\n"
                f"{self.translate('为避免任务存储溢出，你需要在此期间消耗')} {tasks_to_complete} {self.translate('个任务')}。\n"
                f"{self.translate('到明天早上10:10，你的任务储存将保持在')} {simulated_tasks}/{max_storage} {self.translate('个')}。"
            )

            # 显示结果
            QMessageBox.information(self, self.translate("计算结果"), result_message)

        except ValueError:
            QMessageBox.critical(self, self.translate("输入错误"), self.translate("请确保所有输入值为有效的整数。"))


# 主程序
if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = TaskCalculator()
    calculator.show()
    sys.exit(app.exec_())
