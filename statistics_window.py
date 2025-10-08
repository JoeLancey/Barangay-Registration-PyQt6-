"""
Statistics window showing demographic data visualizations.
Displays pie chart for gender distribution, bar graph for age groups, and total population.
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QLinearGradient
from styles import Styles
import math


class StatisticsWindow(QWidget):
    """Statistics and data visualization window"""

    def __init__(self, db_manager, main_window):
        super().__init__()
        self.db_manager = db_manager
        self.main_window = main_window
        self.setWindowTitle("Barangay Statistics")
        self.showMaximized()
        self.setStyleSheet("background-color: #f5f5f5; font-family: 'Segoe UI';")
        self._setup_ui()
        self._load_statistics()

    def _setup_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 5, 30, 15)
        layout.setSpacing(8)

        # Title
        title = QLabel("Population Statistics Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 40px;
            font-weight: bold;
            color: #0D47A1;
            margin: 0px;
            padding: 0px;
        """)
        layout.addWidget(title)

        # Statistics cards row
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(10)
        cards_layout.setContentsMargins(0, 0, 0, 0)

        # Total Population Card
        self.total_card = self._create_stat_card("Total Population", "0", "#1976D2")
        cards_layout.addWidget(self.total_card)

        # Male Card
        self.male_card = self._create_stat_card("Male Residents", "0", "#2196F3")
        cards_layout.addWidget(self.male_card)

        # Female Card
        self.female_card = self._create_stat_card("Female Residents", "0", "#E91E63")
        cards_layout.addWidget(self.female_card)

        layout.addLayout(cards_layout)

        # Charts container - FLEXIBLE HEIGHT
        charts_container = QWidget()
        charts_container.setMinimumHeight(600)
        charts_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
            }
        """)

        charts_layout = QHBoxLayout(charts_container)
        charts_layout.setContentsMargins(20, 20, 20, 20)
        charts_layout.setSpacing(25)

        # Pie chart section
        pie_section = QWidget()
        pie_layout = QVBoxLayout(pie_section)
        pie_layout.setSpacing(8)
        pie_layout.setContentsMargins(0, 0, 0, 0)

        pie_title = QLabel("Gender Distribution")
        pie_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pie_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #333333;
        """)
        pie_layout.addWidget(pie_title)

        self.pie_chart = PieChartWidget()
        self.pie_chart.setMinimumHeight(500)
        pie_layout.addWidget(self.pie_chart)

        charts_layout.addWidget(pie_section)

        # Bar chart section
        bar_section = QWidget()
        bar_layout = QVBoxLayout(bar_section)
        bar_layout.setSpacing(8)
        bar_layout.setContentsMargins(0, 0, 0, 0)

        bar_title = QLabel("Age Group Distribution")
        bar_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bar_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #333333;
        """)
        bar_layout.addWidget(bar_title)

        self.bar_chart = BarChartWidget()
        self.bar_chart.setMinimumHeight(500)
        bar_layout.addWidget(self.bar_chart)

        charts_layout.addWidget(bar_section)

        layout.addWidget(charts_container)

        # Button layout - matching admin dashboard exactly
        button_layout = QHBoxLayout()

        back_btn = QPushButton("Back to Main Menu")
        back_btn.setStyleSheet(Styles.BUTTON_SECONDARY)
        back_btn.clicked.connect(self.go_back)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        button_layout.addStretch()
        button_layout.addWidget(back_btn)

        layout.addLayout(button_layout)

    def _create_stat_card(self, title, value, color):
        """Create a statistics card widget"""
        card = QWidget()
        card.setFixedHeight(130)
        card.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}, stop:1 {self._darken_color(color)});
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.95);
            letter-spacing: 0.5px;
        """)

        value_label = QLabel(value)
        value_label.setObjectName("value_label")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet("""
            font-size: 42px;
            font-weight: bold;
            color: white;
        """)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()

        return card

    def _darken_color(self, hex_color):
        """Darken a hex color for gradient effect"""
        color_map = {
            "#1976D2": "#1565C0",
            "#2196F3": "#1976D2",
            "#E91E63": "#C2185B"
        }
        return color_map.get(hex_color, hex_color)

    def _load_statistics(self):
        """Load and calculate statistics from database"""
        records = self.db_manager.get_all_records()

        # Total population
        total = len(records)

        # Gender distribution
        male_count = sum(1 for r in records if r['sex'] == 'Male')
        female_count = sum(1 for r in records if r['sex'] == 'Female')

        # Update cards
        self.total_card.findChild(QLabel, "value_label").setText(str(total))
        self.male_card.findChild(QLabel, "value_label").setText(str(male_count))
        self.female_card.findChild(QLabel, "value_label").setText(str(female_count))

        # Update charts
        self.pie_chart.set_data(male_count, female_count)

        # Age distribution
        age_groups = {
            '0-17': 0,
            '18-30': 0,
            '31-45': 0,
            '46-60': 0,
            '61+': 0
        }

        for record in records:
            age = record['age']
            if age <= 17:
                age_groups['0-17'] += 1
            elif age <= 30:
                age_groups['18-30'] += 1
            elif age <= 45:
                age_groups['31-45'] += 1
            elif age <= 60:
                age_groups['46-60'] += 1
            else:
                age_groups['61+'] += 1

        self.bar_chart.set_data(age_groups)

    def go_back(self):
        """Return to main window"""
        self.close()
        self.main_window.show()


class PieChartWidget(QWidget):
    """Custom widget for displaying gender distribution pie chart"""

    def __init__(self):
        super().__init__()
        self.male_count = 0
        self.female_count = 0

    def set_data(self, male, female):
        """Set pie chart data"""
        self.male_count = male
        self.female_count = female
        self.update()

    def paintEvent(self, event):
        """Draw the pie chart"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        size = min(width, height) - 80
        center_x = width // 2
        center_y = (height - 40) // 2
        x = center_x - size // 2
        y = center_y - size // 2

        total = self.male_count + self.female_count

        if total == 0:
            painter.setFont(QFont('Segoe UI', 12))
            painter.setPen(QColor('#999999'))
            painter.drawText(0, height // 2, width, 30, Qt.AlignmentFlag.AlignCenter, "No data available")
            return

        # Calculate angles
        male_angle = int((self.male_count / total) * 360 * 16)

        # Draw shadow
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 25))
        painter.drawEllipse(x + 4, y + 4, size, size)

        # Draw male slice (blue)
        painter.setBrush(QColor('#2196F3'))
        painter.setPen(QPen(QColor('#ffffff'), 2))
        painter.drawPie(x, y, size, size, 90 * 16, -male_angle)

        # Draw female slice (pink)
        painter.setBrush(QColor('#E91E63'))
        painter.drawPie(x, y, size, size, 90 * 16 - male_angle, -(360 * 16 - male_angle))

        # Draw center circle (donut effect)
        inner_size = int(size * 0.55)
        inner_x = x + (size - inner_size) // 2
        inner_y = y + (size - inner_size) // 2
        painter.setBrush(QColor('#ffffff'))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(inner_x, inner_y, inner_size, inner_size)

        # Draw total in center
        painter.setPen(QColor('#333333'))
        painter.setFont(QFont('Segoe UI', 20, QFont.Weight.Bold))
        painter.drawText(inner_x, inner_y, inner_size, inner_size,
                         Qt.AlignmentFlag.AlignCenter, str(total))

        # Draw legend
        legend_y = y + size + 15
        legend_spacing = width // 2

        # Male legend
        painter.setBrush(QColor('#2196F3'))
        painter.setPen(Qt.PenStyle.NoPen)
        male_x = center_x - legend_spacing // 2 - 65
        painter.drawRoundedRect(male_x, legend_y, 12, 12, 2, 2)

        painter.setPen(QColor('#333333'))
        painter.setFont(QFont('Segoe UI', 10, QFont.Weight.DemiBold))
        male_percent = (self.male_count / total * 100) if total > 0 else 0
        painter.drawText(male_x + 18, legend_y + 10, f"Male: {self.male_count} ({male_percent:.1f}%)")

        # Female legend
        painter.setBrush(QColor('#E91E63'))
        painter.setPen(Qt.PenStyle.NoPen)
        female_x = center_x + 25
        painter.drawRoundedRect(female_x, legend_y, 12, 12, 2, 2)

        painter.setPen(QColor('#333333'))
        female_percent = (self.female_count / total * 100) if total > 0 else 0
        painter.drawText(female_x + 18, legend_y + 10, f"Female: {self.female_count} ({female_percent:.1f}%)")


class BarChartWidget(QWidget):
    """Custom widget for displaying age distribution bar chart"""

    def __init__(self):
        super().__init__()
        self.age_data = {}

    def set_data(self, age_groups):
        """Set bar chart data"""
        self.age_data = age_groups
        self.update()

    def paintEvent(self, event):
        """Draw the bar chart"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        if not self.age_data or sum(self.age_data.values()) == 0:
            painter.setFont(QFont('Segoe UI', 12))
            painter.setPen(QColor('#999999'))
            painter.drawText(0, height // 2, width, 30, Qt.AlignmentFlag.AlignCenter, "No data available")
            return

        # Chart dimensions
        margin_left = 45
        margin_right = 25
        margin_top = 15
        margin_bottom = 45

        chart_width = width - margin_left - margin_right
        chart_height = height - margin_top - margin_bottom

        # Find max value for scaling
        max_value = max(self.age_data.values()) if self.age_data.values() else 1
        if max_value == 0:
            max_value = 1

        # Draw Y-axis labels and grid
        painter.setFont(QFont('Segoe UI', 8))

        for i in range(6):
            y = margin_top + (chart_height * i // 5)
            value = max_value - (max_value * i // 5)

            # Grid line
            painter.setPen(QColor('#f0f0f0'))
            painter.drawLine(margin_left, y, width - margin_right, y)

            # Y-axis label
            painter.setPen(QColor('#666666'))
            painter.drawText(5, y - 6, margin_left - 10, 12,
                             Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                             str(value))

        # Draw bars
        bar_spacing = 12
        total_bars = len(self.age_data)
        bar_width = (chart_width - (total_bars - 1) * bar_spacing) // total_bars
        x_position = margin_left

        colors = [
            ('#FF6384', '#FF4569'),
            ('#36A2EB', '#2196F3'),
            ('#FFCE56', '#FFC107'),
            ('#4BC0C0', '#26A69A'),
            ('#9966FF', '#7E57C2')
        ]

        for i, (age_group, count) in enumerate(self.age_data.items()):
            # Calculate bar height
            bar_height = int((count / max_value) * chart_height) if max_value > 0 else 0
            bar_y = margin_top + chart_height - bar_height

            # Draw bar shadow
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(0, 0, 0, 18))
            painter.drawRoundedRect(x_position + 2, bar_y + 2, bar_width, bar_height, 3, 3)

            # Draw bar with gradient
            gradient = QLinearGradient(x_position, bar_y, x_position, bar_y + bar_height)
            gradient.setColorAt(0, QColor(colors[i % len(colors)][0]))
            gradient.setColorAt(1, QColor(colors[i % len(colors)][1]))

            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(x_position, bar_y, bar_width, bar_height, 3, 3)

            # Draw value on top of bar
            if bar_height > 18:
                painter.setPen(QColor('#ffffff'))
                painter.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
                painter.drawText(x_position, bar_y + 2, bar_width, 16,
                                 Qt.AlignmentFlag.AlignCenter, str(count))
            else:
                painter.setPen(QColor('#333333'))
                painter.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
                painter.drawText(x_position, bar_y - 14, bar_width, 12,
                                 Qt.AlignmentFlag.AlignCenter, str(count))

            # Draw age group label
            painter.setPen(QColor('#666666'))
            painter.setFont(QFont('Segoe UI', 9, QFont.Weight.DemiBold))
            painter.drawText(x_position, height - margin_bottom + 6,
                             bar_width, 22, Qt.AlignmentFlag.AlignCenter, age_group)

            x_position += bar_width + bar_spacing

        # Draw axes
        painter.setPen(QPen(QColor('#cccccc'), 2))
        painter.drawLine(margin_left, margin_top + chart_height,
                         width - margin_right, margin_top + chart_height)
        painter.drawLine(margin_left, margin_top,
                         margin_left, margin_top + chart_height)
