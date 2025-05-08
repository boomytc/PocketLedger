from PySide6.QtWidgets import (
    QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QComboBox, QDateEdit, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QMessageBox,
    QTabWidget, QScrollArea, QGridLayout, QDialog
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

class DetailsTab(QWidget):
    """包含交易明细、输入表单和汇总统计的标签页内容。"""
    def __init__(self):
        super().__init__()
        self.editing_transaction_id = None # 用于存储正在编辑的交易ID

        # 主布局 (原 MainWindow 的内容)
        main_layout = QVBoxLayout(self) # 将布局应用到这个 QWidget

        # 输入区域
        input_form_layout = QFormLayout()
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        input_form_layout.addRow("日期:", self.date_edit)
        self.description_edit = QLineEdit()
        input_form_layout.addRow("描述:", self.description_edit)
        self.amount_edit = QLineEdit()
        input_form_layout.addRow("金额:", self.amount_edit)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["支出", "收入"])
        input_form_layout.addRow("类型:", self.type_combo)
        self.submit_button = QPushButton("添加交易")
        input_form_layout.addRow(self.submit_button)
        input_widget = QWidget()
        input_widget.setLayout(input_form_layout)
        main_layout.addWidget(input_widget)

        # 表格操作按钮区域
        table_actions_layout = QHBoxLayout()
        self.edit_button = QPushButton("编辑选定交易")
        table_actions_layout.addWidget(self.edit_button)
        self.delete_button = QPushButton("删除选定交易")
        table_actions_layout.addStretch(1)
        table_actions_layout.addWidget(self.delete_button)
        main_layout.addLayout(table_actions_layout)

        # 交易显示区域
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(5)
        self.transactions_table.setHorizontalHeaderLabels(["ID", "日期", "描述", "金额", "类型"])
        self.transactions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.transactions_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.transactions_table.setSelectionBehavior(QTableWidget.SelectRows)
        main_layout.addWidget(self.transactions_table)

        # 汇总统计区域
        summary_group_layout = QHBoxLayout()
        summary_widget = QWidget()
        summary_widget.setLayout(summary_group_layout)
        self.total_income_label = QLabel("总收入: 0.00")
        self.total_expense_label = QLabel("总支出: 0.00")
        self.net_balance_label = QLabel("净额: 0.00")
        summary_group_layout.addWidget(self.total_income_label)
        summary_group_layout.addStretch()
        summary_group_layout.addWidget(self.total_expense_label)
        summary_group_layout.addStretch()
        summary_group_layout.addWidget(self.net_balance_label)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        main_layout.addWidget(summary_widget)

        self.setLayout(main_layout) # 确保 DetailsTab 设置了自己的布局

    # --- 以下方法是原 MainWindow 的 UI 操作方法，现在属于 DetailsTab ---
    def clear_input_fields(self):
        self.date_edit.setDate(QDate.currentDate())
        self.description_edit.clear()
        self.amount_edit.clear()
        self.type_combo.setCurrentIndex(0) # 默认为支出
        self.submit_button.setText("添加交易")
        self.editing_transaction_id = None

    def populate_transaction_table(self, transactions):
        self.transactions_table.setRowCount(0)
        for row_index, row_data in enumerate(transactions):
            self.transactions_table.insertRow(row_index)
            for col_index, data in enumerate(row_data):
                item_text = str(data)
                if col_index == 3:
                    try:
                        item_text = f"{float(data):.2f}"
                    except ValueError:
                        pass
                item = QTableWidgetItem(item_text)
                if col_index == 3:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.transactions_table.setItem(row_index, col_index, item)

    def update_summary_labels(self, total_income, total_expense, net_balance):
        self.total_income_label.setText(f"总收入: {total_income:.2f}")
        self.total_expense_label.setText(f"总支出: {total_expense:.2f}")
        self.net_balance_label.setText(f"净额: {net_balance:.2f}")

    def get_selected_transaction_id(self):
        selected_rows = self.transactions_table.selectionModel().selectedRows()
        if not selected_rows:
            # 注意: show_message 方法现在在 MainWindow 中，需要调整调用方式
            # Controller 会处理消息显示，或 MainWindow 提供一个全局消息接口
            QMessageBox.information(self, "提示", "请先在表格中选择一条交易记录。")
            return None
        selected_row_index = selected_rows[0].row()
        transaction_id_item = self.transactions_table.item(selected_row_index, 0)
        if not transaction_id_item:
            QMessageBox.critical(self, "错误", "无法获取选中交易的ID。")
            return None
        return transaction_id_item.text()

    def get_input_data(self):
        date = self.date_edit.date().toString("yyyy-MM-dd")
        description = self.description_edit.text()
        amount_text = self.amount_edit.text()
        transaction_type = self.type_combo.currentText()
        if not amount_text:
            QMessageBox.warning(self, "输入错误", "金额不能为空。")
            return None
        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "输入错误", "金额必须是有效的数字。")
            return None
        return {
            "date": date,
            "description": description,
            "amount": amount,
            "type": transaction_type
        }

    def populate_form_for_edit(self, transaction_data):
        self.editing_transaction_id = transaction_data[0]
        self.date_edit.setDate(QDate.fromString(transaction_data[1], "yyyy-MM-dd"))
        self.description_edit.setText(transaction_data[2])
        self.amount_edit.setText(str(transaction_data[3]))
        self.type_combo.setCurrentText(transaction_data[4])
        self.submit_button.setText("更新交易")

class HomeTab(QWidget):
    """首页标签页，将包含类别卡片和增加类别的功能。"""
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10) # 添加一些边距
        main_layout.setSpacing(15) # 控件间的间距

        # 顶部标题
        title_label = QLabel("我的类别")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 类别卡片区域 - 使用 QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }") # 可选：移除边框

        self.categories_widget = QWidget() # 滚动区域内的实际内容Widget
        self.categories_container_layout = QVBoxLayout(self.categories_widget) # 主容器，用于放置支出和收入部分
        self.categories_container_layout.setAlignment(Qt.AlignTop)
        self.categories_container_layout.setSpacing(20) # 支出和收入部分之间的间距
        
        self.scroll_area.setWidget(self.categories_widget)
        main_layout.addWidget(self.scroll_area, 1) # 占据主要空间

        # 底部区域: 增加类别按钮
        self.add_category_button = QPushButton("➕ 增加类别")
        # 我们可以稍后美化这个按钮，使其更像一个“卡片”
        self.add_category_button.setFixedHeight(50) # 给按钮一个合适的高度
        # 可以设置一些基本样式
        self.add_category_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        main_layout.addWidget(self.add_category_button, 0, Qt.AlignBottom)

        self.setLayout(main_layout)

    def update_category_cards(self, categories_data):
        """根据提供的类别数据更新首页的类别卡片显示。"""
        # 清除旧的内容 (整个 categories_container_layout)
        while self.categories_container_layout.count():
            child = self.categories_container_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout(): # 清理可能的子布局
                # Implement recursive clearing if layouts can contain other layouts
                pass # For now, assuming only widgets or simple section layouts

        if not categories_data:
            no_categories_label = QLabel("暂无类别，请点击下方按钮添加新类别。")
            no_categories_label.setAlignment(Qt.AlignCenter)
            self.categories_container_layout.addWidget(no_categories_label)
            return

        expense_categories = [cat for cat in categories_data if cat[2] == '支出']
        income_categories = [cat for cat in categories_data if cat[2] == '收入']

        # Helper function to create a grid section for categories
        def create_category_section(title, categories, base_bg_color):
            if not categories:
                return

            section_widget = QWidget()
            section_layout = QVBoxLayout(section_widget)
            section_layout.setContentsMargins(0,0,0,0)
            section_layout.setSpacing(10)

            title_label = QLabel(title)
            title_font = QFont()
            title_font.setPointSize(16)
            title_font.setBold(True)
            title_label.setFont(title_font)
            title_label.setStyleSheet("margin-bottom: 5px;")
            section_layout.addWidget(title_label)

            grid_widget = QWidget()
            grid_layout = QGridLayout(grid_widget)
            grid_layout.setSpacing(10) # 卡片之间的间距
            grid_layout.setContentsMargins(0,0,0,0)
            
            row, col = 0, 0
            for cat_id, name, cat_type in categories:
                card_frame = QFrame()
                card_frame.setFrameShape(QFrame.StyledPanel)
                card_frame.setFrameShadow(QFrame.Raised)
                card_frame.setMinimumSize(100, 100) # 更接近方形
                card_frame.setMaximumSize(130, 130)
                # 简单的颜色区分，可以根据图片进一步细化
                bg_color = base_bg_color
                card_frame.setStyleSheet(f"""
                    QFrame {{
                        background-color: {bg_color};
                        border: 1px solid #d0d0d0;
                        border-radius: 10px;
                        padding: 10px;
                    }}
                """)

                card_content_layout = QVBoxLayout(card_frame)
                card_content_layout.setAlignment(Qt.AlignCenter) # 内容居中

                # 以后可以加图标 QLabel
                # icon_label = QLabel("ICON") 
                # icon_label.setAlignment(Qt.AlignCenter)

                name_label = QLabel(name)
                name_font = QFont()
                name_font.setPointSize(12)
                name_font.setBold(True)
                name_label.setFont(name_font)
                name_label.setAlignment(Qt.AlignCenter)
                name_label.setWordWrap(True)

                # type_label = QLabel(cat_type) # 类型已在分组标题中体现，卡片内可省略
                # type_label.setAlignment(Qt.AlignCenter)

                # card_content_layout.addWidget(icon_label)
                card_content_layout.addWidget(name_label)
                # card_content_layout.addWidget(type_label)
                card_frame.setLayout(card_content_layout)

                grid_layout.addWidget(card_frame, row, col)
                col += 1
                if col >= 3:
                    col = 0
                    row += 1
            
            # 确保网格填满，即使最后一行的卡片不足3个
            # 如果需要，可以添加空的 QSpacerItem 来填充，但通常 QGridLayout 会自动处理对齐
            grid_widget.setLayout(grid_layout)
            section_layout.addWidget(grid_widget)
            self.categories_container_layout.addWidget(section_widget)

        # 创建支出部分
        create_category_section("支出类别", expense_categories, "#e6f3ff") # 淡蓝色背景
        # 创建收入部分
        create_category_section("收入类别", income_categories, "#fff0e6") # 淡橙色背景

        # 如果没有任何类别被实际添加到布局中（例如，只有支出或只有收入，但另一方为空）
        # 并且最初 categories_data 不为空，则不需要再添加“暂无类别”标签
        if self.categories_container_layout.count() == 0 and categories_data:
             # This case should ideally not happen if categories_data is not empty and create_category_section handles it.
             # However, if both expense_categories and income_categories are empty (which means categories_data was empty initially)
             # The initial check for not categories_data already handles it.
             pass
        elif self.categories_container_layout.count() == 0 and not categories_data: # Redundant due to initial check
            no_categories_label = QLabel("暂无类别，请点击下方按钮添加新类别。")
            no_categories_label.setAlignment(Qt.AlignCenter)
            self.categories_container_layout.addWidget(no_categories_label)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.editing_transaction_id = None # 移至 DetailsTab

        self.setWindowTitle("PocketLedger")
        self.setGeometry(100, 100, 850, 800) # 稍微增大窗口以适应标签页

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # 创建各个标签页
        self.home_tab = HomeTab() # 使用新的 HomeTab 类
        self.details_tab = DetailsTab() # 包含原UI的标签页
        self.calendar_tab = QWidget() # 占位符
        self.reports_tab = QWidget() # 占位符
        self.settings_tab = QWidget() # 占位符

        # 添加标签页到 QTabWidget
        self.tab_widget.addTab(self.home_tab, "首页")
        self.tab_widget.addTab(self.details_tab, "明细")
        self.tab_widget.addTab(self.calendar_tab, "日历")
        self.tab_widget.addTab(self.reports_tab, "报表")
        self.tab_widget.addTab(self.settings_tab, "设置")

        # 为占位符标签页添加简单内容，以便区分
        calendar_layout = QVBoxLayout(self.calendar_tab)
        calendar_layout.addWidget(QLabel("日历功能 (功能开发中)"))
        self.calendar_tab.setLayout(calendar_layout)

        reports_layout = QVBoxLayout(self.reports_tab)
        reports_layout.addWidget(QLabel("报表功能 (功能开发中)"))
        self.reports_tab.setLayout(reports_layout)

        settings_layout = QVBoxLayout(self.settings_tab)
        settings_layout.addWidget(QLabel("设置功能 (功能开发中)"))
        self.settings_tab.setLayout(settings_layout)

    # --- MainWindow 现在主要负责整体窗口和消息显示/确认 ---
    # clear_input_fields 等方法已移至 DetailsTab
    # populate_transaction_table 等方法已移至 DetailsTab
    # update_summary_labels 等方法已移至 DetailsTab
    # get_selected_transaction_id 等方法已移至 DetailsTab
    # get_input_data 等方法已移至 DetailsTab
    # populate_form_for_edit 等方法已移至 DetailsTab

    def show_message(self, title, message, level="information"):
        """显示一个消息框。level可以是 'information', 'warning', 'critical'。"""
        if level == "warning":
            QMessageBox.warning(self, title, message)
        elif level == "critical":
            QMessageBox.critical(self, title, message)
        else: # information or any other
            QMessageBox.information(self, title, message)

    def confirm_action(self, title, message):
        """显示一个确认对话框，返回 True (Yes) 或 False (No)。"""
        reply = QMessageBox.question(self, title, message,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes
