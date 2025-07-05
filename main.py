import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QFileDialog, QComboBox, QTextEdit, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class LoginPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        self.label = QLabel("Добро пожаловать в WB-Аналитику")
        self.label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: #2c3e50;")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Логин")
        self.username.setMinimumHeight(40)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Пароль")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setMinimumHeight(40)

        self.login_btn = QPushButton("Войти")
        self.login_btn.setMinimumHeight(40)

        layout.addWidget(self.label)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)
        self.login_btn.clicked.connect(self.login)

    def login(self):
        if self.username.text() and self.password.text():
            self.stacked_widget.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")


class DashboardPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.data = None
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.label = QLabel("Загрузка данных (лист 'Товары')")
        self.label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.label.setStyleSheet("color: #2c3e50;")

        self.load_btn = QPushButton("Загрузить Excel")
        self.load_btn.setMinimumHeight(40)

        self.status = QLabel("")
        self.status.setStyleSheet("color: #7f8c8d; font-size: 12px;")

        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(15)

        buttons = [
            ("Аналитика", self.go_to_analytics),
            ("Рекомендации ИИ", self.go_to_ai),
            ("Сравнение периодов", self.go_to_compare),
            ("Анализ по дизайнеру", self.go_to_designer),
            ("Частные запросы", self.go_to_query)
        ]

        for text, handler in buttons:
            btn = QPushButton(text)
            btn.setMinimumHeight(40)
            btn.clicked.connect(handler)
            btn_layout.addWidget(btn)

        layout.addWidget(self.label)
        layout.addWidget(self.load_btn)
        layout.addWidget(self.status)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_btn.clicked.connect(self.load_excel)

    def load_excel(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл Excel",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        if path:
            try:
                self.data = pd.read_excel(path, sheet_name="Товары")
                self.status.setText(f"✓ Успешно загружено: {len(self.data)} строк")
                self.status.setStyleSheet("color: #27ae60; font-size: 12px;")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл: {e}")
                self.status.setText("✗ Ошибка загрузки файла")
                self.status.setStyleSheet("color: #e74c3c; font-size: 12px;")

    def go_to_page(self, index):
        if self.data is not None:
            self.stacked_widget.widget(index).set_data(self.data)
            self.stacked_widget.setCurrentIndex(index)
        else:
            QMessageBox.warning(self, "Ошибка", "Сначала загрузите данные")

    def go_to_analytics(self):
        self.go_to_page(2)

    def go_to_ai(self):
        self.go_to_page(3)

    def go_to_compare(self):
        self.go_to_page(4)

    def go_to_designer(self):
        self.go_to_page(5)

    def go_to_query(self):
        self.go_to_page(6)


class AnalyticsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title = QLabel("Аналитика продаж")
        self.title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #2c3e50;")

        control_layout = QHBoxLayout()
        control_layout.setSpacing(15)

        self.metric_label = QLabel("Метрика:")
        self.metric_label.setStyleSheet("color: #34495e;")

        self.metric_selector = QComboBox()
        self.metric_selector.addItems(["Выкупили, шт", "Выкупили на сумму, ₽"])

        self.plot_btn = QPushButton("Построить график")
        self.plot_btn.setMinimumHeight(40)

        control_layout.addWidget(self.metric_label)
        control_layout.addWidget(self.metric_selector)
        control_layout.addWidget(self.plot_btn)

        self.canvas = FigureCanvas(plt.Figure())
        self.canvas.setStyleSheet("background-color: white; border: 1px solid #ddd; border-radius: 8px;")

        self.back_btn = QPushButton("Назад в меню")
        self.back_btn.setMinimumHeight(40)

        layout.addWidget(self.title)
        layout.addLayout(control_layout)
        layout.addWidget(self.canvas, stretch=1)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)
        self.plot_btn.clicked.connect(self.plot_graph)
        self.back_btn.clicked.connect(self.go_back)

    def set_data(self, data):
        self.data = data

    def plot_graph(self):
        if self.data is None:
            QMessageBox.warning(self, "Нет данных", "Сначала загрузите файл")
            return

        metric = self.metric_selector.currentText()

        try:
            summary = self.data.groupby("Предмет")[metric].sum().sort_values(ascending=False)
            ax = self.canvas.figure.subplots()
            ax.clear()

            # Стилизация графика
            bars = summary.plot(
                kind="bar",
                ax=ax,
                color="#3498db",
                edgecolor="#2980b9",
                linewidth=1
            )

            # Добавляем значения на столбцы
            for bar in bars.patches:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f"{int(bar.get_height()):,}",
                    ha='center',
                    va='bottom',
                    color='#2c3e50'
                )

            ax.set_title(f"{metric} по категориям", pad=20, fontsize=14, color="#2c3e50")
            ax.set_facecolor("#f9f9f9")
            ax.grid(axis='y', linestyle='--', alpha=0.7)

            # Убираем рамку
            for spine in ax.spines.values():
                spine.set_visible(False)

            self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Невозможно построить график: {e}")

    def go_back(self):
        self.parent().setCurrentIndex(1)


class AIPage(QWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.label = QLabel("Рекомендации ИИ")
        self.label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.label.setStyleSheet("color: #2c3e50;")

        self.info = QLabel(
            "Здесь будут отображаться персонализированные рекомендации\n"
            "по улучшению ваших продаж на основе анализа данных."
        )
        self.info.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.back_btn = QPushButton("Назад в меню")
        self.back_btn.setMinimumHeight(40)

        layout.addWidget(self.label)
        layout.addWidget(self.info, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)
        self.back_btn.clicked.connect(self.go_back)

    def set_data(self, data):
        self.data = data

    def go_back(self):
        self.parent().setCurrentIndex(1)


class ComparePeriodPage(QWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title = QLabel("Сравнение периодов")
        self.title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #2c3e50;")

        self.plot_btn = QPushButton("Построить сравнение")
        self.plot_btn.setMinimumHeight(40)

        self.canvas = FigureCanvas(plt.Figure())
        self.canvas.setStyleSheet("background-color: white; border: 1px solid #ddd; border-radius: 8px;")

        self.back_btn = QPushButton("Назад в меню")
        self.back_btn.setMinimumHeight(40)

        layout.addWidget(self.title)
        layout.addWidget(self.plot_btn)
        layout.addWidget(self.canvas, stretch=1)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)
        self.plot_btn.clicked.connect(self.plot_comparison)
        self.back_btn.clicked.connect(self.go_back)

    def set_data(self, data):
        self.data = data

    def plot_comparison(self):
        if self.data is None:
            QMessageBox.warning(self, "Нет данных", "Сначала загрузите файл")
            return

        try:
            current = self.data.groupby("Предмет")["Выкупили на сумму, ₽"].sum()
            previous = self.data.groupby("Предмет")["Выкупили на сумму, ₽ (предыдущий период)"].sum()

            ax = self.canvas.figure.subplots()
            ax.clear()

            # Текущий период
            current.plot(
                kind="bar",
                position=0,
                width=0.4,
                label="Текущий период",
                ax=ax,
                color="#2ecc71",
                edgecolor="#27ae60"
            )

            # Прошлый период
            previous.plot(
                kind="bar",
                position=1,
                width=0.4,
                label="Прошлый период",
                ax=ax,
                color="#95a5a6",
                edgecolor="#7f8c8d"
            )

            ax.set_title("Сравнение выручки по категориям", pad=20, fontsize=14, color="#2c3e50")
            ax.set_facecolor("#f9f9f9")
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            ax.legend()

            # Убираем рамку
            for spine in ax.spines.values():
                spine.set_visible(False)

            self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Невозможно построить график: {e}")

    def go_back(self):
        self.parent().setCurrentIndex(1)


class DesignerSearchPage(QWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.designers = ["VAA", "MVM", "KRG", "BRL", "BAS"]
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title = QLabel("Анализ по дизайнеру")
        self.title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #2c3e50;")

        self.dropdown_label = QLabel("Выберите дизайнера:")
        self.dropdown_label.setStyleSheet("color: #34495e;")

        self.dropdown = QComboBox()
        self.dropdown.addItems(self.designers)

        self.search_btn = QPushButton("Показать статистику")
        self.search_btn.setMinimumHeight(40)

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                color: #2c3e50;
                font-size: 14px;
            }
        """)

        self.back_btn = QPushButton("Назад в меню")
        self.back_btn.setMinimumHeight(40)

        layout.addWidget(self.title)
        layout.addWidget(self.dropdown_label)
        layout.addWidget(self.dropdown)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.result_output, stretch=1)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)
        self.search_btn.clicked.connect(self.show_stats)
        self.back_btn.clicked.connect(self.go_back)

    def set_data(self, data):
        self.data = data

    def show_stats(self):
        designer = self.dropdown.currentText()
        if self.data is None:
            QMessageBox.warning(self, "Ошибка", "Нет загруженных данных")
            return

        filtered = self.data[self.data["Артикул продавца"].str.contains(designer, na=False)]

        if filtered.empty:
            self.result_output.setText("Нет товаров с таким дизайнером")
            return

        count = len(filtered)
        total_sales = filtered["Выкупили, шт"].sum()
        total_revenue = filtered["Выкупили на сумму, ₽"].sum()

        result = (
            f"<h3 style='color:#2c3e50'>Статистика для дизайнера {designer}</h3>"
            f"<p><b>Найдено товаров:</b> {count}</p>"
            f"<p><b>Общее количество продаж:</b> {total_sales}</p>"
            f"<p><b>Общая выручка:</b> {total_revenue:,.2f} ₽</p>"
        )
        self.result_output.setHtml(result)

    def go_back(self):
        self.parent().setCurrentIndex(1)


class PrivateQueryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title = QLabel("Частные запросы")
        self.title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #2c3e50;")

        self.category_label = QLabel("Категория (предмет):")
        self.category_label.setStyleSheet("color: #34495e;")

        self.category_selector = QComboBox()

        self.article_label = QLabel("Артикул продавца:")
        self.article_label.setStyleSheet("color: #34495e;")

        self.article_input = QLineEdit()
        self.article_input.setPlaceholderText("Введите часть артикула (опционально)")

        self.search_btn = QPushButton("Поиск")
        self.search_btn.setMinimumHeight(40)

        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                gridline-color: #eee;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 5px;
                border: none;
            }
        """)

        # Настройка таблицы
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)

        self.back_btn = QPushButton("Назад в меню")
        self.back_btn.setMinimumHeight(40)

        layout.addWidget(self.title)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_selector)
        layout.addWidget(self.article_label)
        layout.addWidget(self.article_input)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.table, stretch=1)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)
        self.search_btn.clicked.connect(self.run_query)
        self.back_btn.clicked.connect(self.go_back)

    def set_data(self, data):
        self.data = data
        if data is not None:
            categories = sorted(data["Предмет"].dropna().unique())
            self.category_selector.clear()
            self.category_selector.addItems(categories)

    def run_query(self):
        if self.data is None:
            QMessageBox.warning(self, "Ошибка", "Нет загруженных данных")
            return

        category = self.category_selector.currentText()
        article_part = self.article_input.text().strip()

        filtered = self.data[self.data["Предмет"] == category]

        if article_part:
            filtered = filtered[filtered["Артикул продавца"].str.contains(article_part, na=False)]

        if filtered.empty:
            QMessageBox.information(self, "Результат", "Ничего не найдено по заданным условиям")
            self.table.setRowCount(0)
            return

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Артикул", "Название", "Выкупили, шт", "Выручка"])
        self.table.setRowCount(len(filtered))

        for i, (_, row) in enumerate(filtered.iterrows()):
            for j, col in enumerate(["Артикул продавца", "Название", "Выкупили, шт", "Выкупили на сумму, ₽"]):
                item = QTableWidgetItem(str(row[col]))
                item.setForeground(QColor("#2c3e50"))  # Черный цвет текста
                self.table.setItem(i, j, item)

    def go_back(self):
        self.parent().setCurrentIndex(1)


STYLE_SHEET = """
    QWidget {
        background-color: #f5f7fa;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    QLabel {
        color: #2c3e50;
        font-size: 14px;
    }
    QPushButton {
        background-color: #3498db;
        color: white;
        padding: 8px 16px;
        border-radius: 6px;
        border: none;
        font-weight: bold;
        min-width: 120px;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
    QPushButton:pressed {
        background-color: #1a5276;
    }
    QLineEdit, QComboBox, QTextEdit {
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 6px;
        color: #2c3e50;
        background-color: white;
        font-size: 14px;
    }
    QComboBox::drop-down {
        border: none;
    }
    QComboBox QAbstractItemView {
        border: 1px solid #ddd;
        selection-background-color: #3498db;
        selection-color: white;
    }
    QTableWidget {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        gridline-color: #eee;
        font-size: 14px;
    }
    QHeaderView::section {
        background-color: #3498db;
        color: white;
        padding: 6px;
        border: none;
        font-weight: bold;
    }
    QMessageBox {
        background-color: #f5f7fa;
    }
    QMessageBox QLabel {
        color: #2c3e50;
    }
"""


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WB-Аналитика")
        self.resize(1200, 800)
        self.setStyleSheet(STYLE_SHEET)

        self.stacked_widget = QStackedWidget(self)

        # Создаем страницы
        self.login_page = LoginPage(self.stacked_widget)
        self.dashboard_page = DashboardPage(self.stacked_widget)
        self.analytics_page = AnalyticsPage()
        self.ai_page = AIPage()
        self.compare_page = ComparePeriodPage()
        self.designer_page = DesignerSearchPage()
        self.query_page = PrivateQueryPage()

        # Добавляем страницы в стек
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.analytics_page)
        self.stacked_widget.addWidget(self.ai_page)
        self.stacked_widget.addWidget(self.compare_page)
        self.stacked_widget.addWidget(self.designer_page)
        self.stacked_widget.addWidget(self.query_page)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Современный стиль Qt

    # Настройка палитры для темного текста
    palette = app.palette()
    palette.setColor(QPalette.ColorRole.WindowText, QColor(44, 62, 80))  # Темно-синий текст
    palette.setColor(QPalette.ColorRole.Text, QColor(44, 62, 80))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())