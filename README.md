# PocketLedger
一个简单的个人记账应用。

## 技术栈

- Python
- PySide6
- SQLite

## 如何开始

1.  **环境设置**

    确保你已经安装了 Python 3.11 和 pip。

2.  **克隆仓库 (如果适用)**

    ```bash
    # git clone <repository_url>
    # cd PocketLedger
    ```

3.  **创建并激活虚拟环境**

    ```bash
    conda create -n pocketledger python=3.11 -y
    conda activate pocketledger
    ```

4.  **安装依赖**

    ```bash
    pip install -r requirements.txt
    ```

5.  **运行应用**

    ```bash
    python app.py
    ```

    应用将启动一个桌面窗口。

## 项目结构 (初步)

```
PocketLedger/
├── app.py            # PySide6 应用主文件
├── pocketledger.db   # SQLite 数据库文件 (自动生成)
├── requirements.txt  # Python 依赖
├── README.md         # 项目说明
└── venv/             # Python 虚拟环境 (自动生成)
