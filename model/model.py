import sqlite3

DATABASE_FILE = "pocketledger.db"

def init_db():
    """初始化数据库，创建 transactions 表和 categories 表 (如果不存在)。"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    # 确保 type 字段的 CHECK 约束使用中文，与 UI 和插入逻辑一致
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT, 
            amount REAL NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('收入', '支出'))
        )
    ''')
    # 创建 categories 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL CHECK(type IN ('收入', '支出')) 
        )
    ''')
    conn.commit()
    conn.close()

class TransactionModel:
    """处理所有与交易数据相关的数据库操作。"""
    def __init__(self):
        init_db()  

    def add_transaction(self, date, description, amount, transaction_type):
        """向数据库添加一条新的交易记录。"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO transactions (date, description, amount, type) VALUES (?, ?, ?, ?)",
                (date, description, amount, transaction_type)
            )
            conn.commit()
            return True, "交易已成功添加。"
        except sqlite3.Error as e:
            return False, f"添加交易失败: {e}"
        finally:
            conn.close()

    def get_all_transactions(self):
        """获取所有交易记录，按日期和ID降序排列。"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, date, description, amount, type FROM transactions ORDER BY date DESC, id DESC")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"获取交易记录时出错: {e}")
            return []
        finally:
            conn.close()

    def delete_transaction(self, transaction_id):
        """根据ID删除一条交易记录。"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            conn.commit()
            return True, f"交易记录 (ID: {transaction_id}) 已成功删除。"
        except sqlite3.Error as e:
            return False, f"删除交易记录失败: {e}"
        finally:
            conn.close()
            
    def update_transaction(self, transaction_id, date, description, amount, transaction_type):
        """根据ID更新一条现有的交易记录。"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE transactions SET date=?, description=?, amount=?, type=? WHERE id=?",
                (date, description, amount, transaction_type, transaction_id)
            )
            conn.commit()
            return True, f"交易 (ID: {transaction_id}) 已成功更新。"
        except sqlite3.Error as e:
            return False, f"更新交易失败: {e}"
        finally:
            conn.close()

    def get_transaction_by_id(self, transaction_id):
        """根据ID获取单条交易记录。"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, date, description, amount, type FROM transactions WHERE id = ?", (transaction_id,))
            return cursor.fetchone() 
        except sqlite3.Error as e:
            print(f"获取交易记录 (ID: {transaction_id}) 时出错: {e}")
            return None
        finally:
            conn.close()

    def add_category(self, name, category_type):
        """向数据库添加一个新的类别。"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO categories (name, type) VALUES (?, ?)",
                (name, category_type)
            )
            conn.commit()
            return True, f"类别 '{name}' 已成功添加。"
        except sqlite3.IntegrityError: 
            return False, f"类别 '{name}' 已存在。"
        except sqlite3.Error as e:
            return False, f"添加类别失败: {e}"
        finally:
            conn.close()

    def get_categories(self, category_type=None):
        """获取类别列表，可选按类型（'收入' 或 '支出'）筛选。"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        try:
            if category_type:
                cursor.execute("SELECT id, name, type FROM categories WHERE type = ? ORDER BY name ASC", (category_type,))
            else:
                cursor.execute("SELECT id, name, type FROM categories ORDER BY type ASC, name ASC")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"获取类别时出错: {e}")
            return []
        finally:
            conn.close()

    def get_summary_stats(self):
        """计算并返回总收入、总支出和净额。"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        total_income = 0.0
        total_expense = 0.0
        try:
            cursor.execute("SELECT amount, type FROM transactions")
            records = cursor.fetchall()
            for record in records:
                amount, type_ = record
                if type_ == "收入":
                    total_income += amount
                elif type_ == "支出":
                    total_expense += amount
            
            net_balance = total_income - total_expense
            return total_income, total_expense, net_balance
        except sqlite3.Error as e:
            print(f"计算汇总统计时出错: {e}")
            return 0.0, 0.0, 0.0
        finally:
            conn.close()
