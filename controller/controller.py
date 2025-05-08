from PySide6.QtCore import QDate
from PySide6.QtWidgets import QInputDialog
from model.model import TransactionModel # Updated import
# view.py will be instantiated and passed in by app.py

class Controller:
    def __init__(self, model: TransactionModel, view):
        self.model = model
        self.view = view 
        self._connect_signals()
        self.load_initial_data()

    def _connect_signals(self):
        """连接视图中的信号到控制器的方法。"""
        self.view.details_tab.submit_button.clicked.connect(self.submit_transaction)
        self.view.details_tab.delete_button.clicked.connect(self.delete_selected_transaction)
        self.view.details_tab.edit_button.clicked.connect(self.start_edit_selected_transaction)

        # 连接首页标签页的信号
        if hasattr(self.view, 'home_tab') and hasattr(self.view.home_tab, 'add_category_button'):
            self.view.home_tab.add_category_button.clicked.connect(self.prompt_add_category)

    def load_initial_data(self):
        """加载初始数据，例如交易列表和汇总统计。"""
        self.refresh_transactions_table()
        self.update_summary_display()
        self.refresh_home_tab_categories()

    def refresh_transactions_table(self):
        """从模型获取所有交易并更新视图中的表格。"""
        transactions = self.model.get_all_transactions()
        self.view.details_tab.populate_transaction_table(transactions)

    def update_summary_display(self):
        """从模型获取汇总统计并更新视图中的标签。"""
        total_income, total_expense, net_balance = self.model.get_summary_stats()
        self.view.details_tab.update_summary_labels(total_income, total_expense, net_balance)

    def submit_transaction(self):
        """处理添加或更新交易的逻辑。"""
        input_data = self.view.details_tab.get_input_data()
        if not input_data:
            return 

        if self.view.details_tab.editing_transaction_id is not None:
            success, message = self.model.update_transaction(
                self.view.details_tab.editing_transaction_id,
                input_data['date'],
                input_data['description'],
                input_data['amount'],
                input_data['type']
            )
        else:
            success, message = self.model.add_transaction(
                input_data['date'],
                input_data['description'],
                input_data['amount'],
                input_data['type']
            )

        if success:
            self.view.show_message("成功", message)
            self.view.details_tab.clear_input_fields()
            self.refresh_transactions_table()
            self.update_summary_display()
        else:
            self.view.show_message("错误", message, "critical")

    def delete_selected_transaction(self):
        """删除表格中选定的交易。"""
        transaction_id = self.view.details_tab.get_selected_transaction_id()
        if not transaction_id:
            return 

        if self.view.confirm_action("确认删除", f"您确定要删除ID为 {transaction_id} 的交易记录吗？"):
            success, message = self.model.delete_transaction(transaction_id)
            if success:
                self.view.show_message("成功", message)
                self.refresh_transactions_table()
                self.update_summary_display()
            else:
                self.view.show_message("错误", message, "critical")

    def start_edit_selected_transaction(self):
        """准备编辑选定的交易。"""
        transaction_id_str = self.view.details_tab.get_selected_transaction_id()
        if not transaction_id_str:
            return

        try:
            transaction_id = int(transaction_id_str)
        except ValueError:
            self.view.show_message("错误", "无效的交易ID。", "critical")
            return

        transaction_to_edit = self.model.get_transaction_by_id(transaction_id)
        
        if transaction_to_edit:
            self.view.details_tab.populate_form_for_edit(transaction_to_edit)
        else:
            self.view.show_message("错误", f"未找到ID为 {transaction_id} 的交易记录。", "critical")

    def prompt_add_category(self):
        """弹出对话框让用户输入新类别的名称和类型，然后尝试添加。"""
        # 1. 获取类别名称
        category_name, ok1 = QInputDialog.getText(self.view, "增加新类别", "类别名称:")
        if not ok1 or not category_name.strip():
            if ok1: # 用户点击了OK但没输入内容
                self.view.show_message("提示", "类别名称不能为空。", "warning")
            return # 用户取消或输入为空

        category_name = category_name.strip()

        # 2. 获取类别类型 (收入/支出)
        types = ["支出", "收入"]
        category_type, ok2 = QInputDialog.getItem(self.view, "选择类别类型", "类别类型:", types, 0, False)
        if not ok2:
            return # 用户取消

        # 3. 调用模型添加类别
        success, message = self.model.add_category(category_name, category_type)

        # 4. 显示结果
        if success:
            self.view.show_message("成功", message)
            self.refresh_home_tab_categories()
        else:
            self.view.show_message("错误", message, "critical")

    def refresh_home_tab_categories(self):
        """从模型获取类别数据并更新首页标签页的显示。"""
        if hasattr(self.view, 'home_tab') and hasattr(self.view.home_tab, 'update_category_cards'):
            all_categories = self.model.get_categories() # 获取所有类别
            self.view.home_tab.update_category_cards(all_categories)
