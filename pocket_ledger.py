import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Property, Slot, QUrl, Qt, QDateTime
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtGui import QGuiApplication, QFontDatabase

# QML代码作为Python字符串
QML_CODE = """
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    id: appWindow
    visible: true
    width: 360; height: 640
    title: qsTr("卡片记账")
    color: "#F8F9FA"
    
    Material.theme: Material.Light
    Material.accent: "#4785FF"
    Material.primary: "#4785FF"
    
    property var expenseCategories: [
        { name: "餐饮", icon: "🍚", color: "#FFE0B2", amount: "¥50" },
        { name: "交通", icon: "🚌", color: "#B3E5FC", amount: "¥8" },
        { name: "购物", icon: "🛍️", color: "#FFCDD2", amount: "¥100" },
        { name: "娱乐", icon: "🎮", color: "#E1BEE7", amount: "¥20" },
        { name: "医疗", icon: "💊", color: "#B2DFDB", amount: "¥50" },
        { name: "居家", icon: "🏠", color: "#FFE0B2", amount: "¥50" }
    ]
    
    property var incomeCategories: [
        { name: "薪金", icon: "💰", color: "#DCEDC8", amount: "¥500" },
        { name: "红包", icon: "🧧", color: "#FFCDD2", amount: "¥200" },
        { name: "工资", icon: "💵", color: "#B2DFDB", amount: "¥1000" }
    ]
    
    // 不使用外部字体，改用Unicode表情符号作为图标

    header: ToolBar {
        height: 60
        Material.elevation: 0
        
        Rectangle {
            anchors.fill: parent
            color: "white"
        }
        
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 16
            anchors.rightMargin: 16
            
            Label {
                text: appWindow.title
                font.pixelSize: 20
                font.weight: Font.Medium
                color: "#333333"
                Layout.fillWidth: true
            }
            
            RoundButton {
                text: "⚙️"
                flat: true
                onClicked: {}
            }
        }
    }

    StackView {
        id: stackView
        anchors.fill: parent
        anchors.bottomMargin: tabBar.height
        initialItem: homePage
    }

    Component {
        id: homePage
        Page {
            background: Rectangle { color: "#F8F9FA" }
            
            ScrollView {
                anchors.fill: parent
                contentWidth: -1
                clip: true
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 20
                    width: parent.width
                    
                    // 日期显示
                    Rectangle {
                        Layout.fillWidth: true
                        height: 40
                        color: "transparent"
                        
                        RowLayout {
                            anchors.fill: parent
                            spacing: 10
                            
                            Rectangle {
                                Layout.preferredWidth: 80
                                height: 30
                                radius: 15
                                color: "#FFD180"
                                
                                Label {
                                    anchors.centerIn: parent
                                    text: "日常账本"
                                    font.pixelSize: 12
                                    color: "#795548"
                                }
                            }
                            
                            Item { Layout.fillWidth: true }
                            
                            Rectangle {
                                Layout.preferredWidth: 60
                                height: 30
                                radius: 15
                                color: "#E3F2FD"
                                
                                Label {
                                    anchors.centerIn: parent
                                    text: "今天"
                                    font.pixelSize: 12
                                    color: "#4785FF"
                                }
                            }
                        }
                    }
                    
                    // 支出总额
                    Rectangle {
                        Layout.fillWidth: true
                        height: 60
                        color: "white"
                        radius: 12
                        
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 16
                            
                            Label {
                                text: "支出"
                                font.pixelSize: 16
                                color: "#333333"
                            }
                            
                            Label {
                                Layout.fillWidth: true
                                horizontalAlignment: Text.AlignRight
                                text: "¥278"
                                font.pixelSize: 20
                                font.weight: Font.DemiBold
                                color: "#F44336"
                            }
                            
                            Rectangle {
                                width: 20
                                height: 20
                                radius: 10
                                color: "#E3F2FD"
                                
                                Label {
                                    anchors.centerIn: parent
                                    text: "i"
                                    font.pixelSize: 12
                                    color: "#4785FF"
                                }
                            }
                        }
                    }
                    
                    // 支出分类
                    GridLayout {
                        Layout.fillWidth: true
                        columns: 3
                        rowSpacing: 12
                        columnSpacing: 12
                        
                        Repeater {
                            model: expenseCategories
                            
                            Rectangle {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 80
                                color: "white"
                                radius: 12
                                
                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.margins: 10
                                    spacing: 4
                                    
                                    Rectangle {
                                        Layout.preferredWidth: 40
                                        Layout.preferredHeight: 40
                                        color: modelData.color
                                        radius: 8
                                        
                                        Label {
                                            anchors.centerIn: parent
                                            text: modelData.icon
                                            font.pixelSize: 18
                                        }
                                    }
                                    
                                    Label {
                                        Layout.fillWidth: true
                                        text: modelData.name
                                        font.pixelSize: 12
                                        horizontalAlignment: Text.AlignHCenter
                                    }
                                    
                                    Label {
                                        Layout.fillWidth: true
                                        text: modelData.amount
                                        color: "#4CAF50"
                                        font.pixelSize: 14
                                        horizontalAlignment: Text.AlignHCenter
                                    }
                                }
                                
                                Rectangle {
                                    anchors.bottom: parent.bottom
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    width: parent.width - 20
                                    height: 2
                                    color: "#4CAF50"
                                    radius: 1
                                }
                                
                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: stackView.push(addEntryPage)
                                }
                            }
                        }
                    }
                    
                    // 收入总额
                    Rectangle {
                        Layout.fillWidth: true
                        height: 60
                        color: "white"
                        radius: 12
                        
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 16
                            
                            Label {
                                text: "收入"
                                font.pixelSize: 16
                                color: "#333333"
                            }
                            
                            Label {
                                Layout.fillWidth: true
                                horizontalAlignment: Text.AlignRight
                                text: "¥1700"
                                font.pixelSize: 20
                                font.weight: Font.DemiBold
                                color: "#4CAF50"
                            }
                            
                            Rectangle {
                                width: 20
                                height: 20
                                radius: 10
                                color: "#E3F2FD"
                                
                                Label {
                                    anchors.centerIn: parent
                                    text: "i"
                                    font.pixelSize: 12
                                    color: "#4785FF"
                                }
                            }
                        }
                    }
                    
                    // 收入分类
                    GridLayout {
                        Layout.fillWidth: true
                        columns: 3
                        rowSpacing: 12
                        columnSpacing: 12
                        
                        Repeater {
                            model: incomeCategories
                            
                            Rectangle {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 80
                                color: "white"
                                radius: 12
                                
                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.margins: 10
                                    spacing: 4
                                    
                                    Rectangle {
                                        Layout.preferredWidth: 40
                                        Layout.preferredHeight: 40
                                        color: modelData.color
                                        radius: 8
                                        
                                        Label {
                                            anchors.centerIn: parent
                                            text: modelData.icon
                                            font.pixelSize: 18
                                        }
                                    }
                                    
                                    Label {
                                        Layout.fillWidth: true
                                        text: modelData.name
                                        font.pixelSize: 12
                                        horizontalAlignment: Text.AlignHCenter
                                    }
                                    
                                    Label {
                                        Layout.fillWidth: true
                                        text: modelData.amount
                                        color: "#F44336"
                                        font.pixelSize: 14
                                        horizontalAlignment: Text.AlignHCenter
                                    }
                                }
                                
                                Rectangle {
                                    anchors.bottom: parent.bottom
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    width: parent.width - 20
                                    height: 2
                                    color: "#F44336"
                                    radius: 1
                                }
                                
                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: stackView.push(addEntryPage)
                                }
                            }
                        }
                    }
                    
                    Item { height: 20 } // 底部间距
                }
            }
        }
    }

    Component {
        id: transactionsPage
        Page {
            background: Rectangle { color: "#F8F9FA" }
            
            ListView {
                id: transList
                anchors.fill: parent
                anchors.margins: 16
                spacing: 10
                clip: true
                model: ListModel {
                    ListElement { date: "05-06"; category: "餐饮"; icon: "🍚"; amount: "¥50.00"; color: "#FFE0B2" }
                    ListElement { date: "05-06"; category: "交通"; icon: "🚌"; amount: "¥8.00"; color: "#B3E5FC" }
                    ListElement { date: "05-05"; category: "购物"; icon: "🛍️"; amount: "¥100.00"; color: "#FFCDD2" }
                    ListElement { date: "05-04"; category: "工资"; icon: "💵"; amount: "+¥1000.00"; color: "#B2DFDB" }
                }
                headerPositioning: ListView.OverlayHeader
                header: Rectangle {
                    z: 2
                    width: transList.width
                    height: 40
                    color: "#F8F9FA"
                    
                    Label {
                        anchors.verticalCenter: parent.verticalCenter
                        text: "最近交易"
                        font.pixelSize: 18
                        font.weight: Font.Medium
                        color: "#333333"
                    }
                }
                
                delegate: Rectangle {
                    width: transList.width
                    height: 70
                    radius: 12
                    color: "white"
                    
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 12
                        spacing: 12
                        
                        Rectangle {
                            width: 45
                            height: 45
                            radius: 8
                            color: color
                            
                            Label {
                                anchors.centerIn: parent
                                text: icon
                                font.pixelSize: 20
                            }
                        }
                        
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 4
                            
                            Label {
                                text: category
                                font.pixelSize: 16
                                color: "#333333"
                            }
                            
                            Label {
                                text: date
                                font.pixelSize: 12
                                color: "#9E9E9E"
                            }
                        }
                        
                        Label {
                            text: amount
                            font.pixelSize: 16
                            font.weight: Font.Medium
                            color: amount.startsWith("+") ? "#4CAF50" : "#F44336"
                        }
                    }
                }
            }
            
            RoundButton {
                text: "+"
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: 16
                width: 56
                height: 56
                font.pixelSize: 24
                Material.background: Material.accent
                highlighted: true
                onClicked: stackView.push(addEntryPage)
            }
        }
    }

    Component {
        id: statsPage
        Page {
            background: Rectangle { color: "#F8F9FA" }
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 16
                
                Label { 
                    text: qsTr("统计分析")
                    font.pixelSize: 18
                    font.weight: Font.Medium
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 200
                    color: "white"
                    radius: 12
                    
                    Label {
                        anchors.centerIn: parent
                        text: "此处将显示统计图表"
                        color: "#9E9E9E"
                    }
                }
                
                GridLayout {
                    Layout.fillWidth: true
                    columns: 2
                    rowSpacing: 12
                    columnSpacing: 12
                    
                    Rectangle {
                        Layout.fillWidth: true
                        height: 100
                        color: "white"
                        radius: 12
                        
                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 12
                            
                            Label {
                                text: "本月支出"
                                font.pixelSize: 14
                                color: "#9E9E9E"
                            }
                            
                            Label {
                                text: "¥1,245.00"
                                font.pixelSize: 20
                                font.weight: Font.Medium
                                color: "#F44336"
                            }
                            
                            Label {
                                text: "较上月 +12%"
                                font.pixelSize: 12
                                color: "#F44336"
                            }
                        }
                    }
                    
                    Rectangle {
                        Layout.fillWidth: true
                        height: 100
                        color: "white"
                        radius: 12
                        
                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 12
                            
                            Label {
                                text: "本月收入"
                                font.pixelSize: 14
                                color: "#9E9E9E"
                            }
                            
                            Label {
                                text: "¥5,400.00"
                                font.pixelSize: 20
                                font.weight: Font.Medium
                                color: "#4CAF50"
                            }
                            
                            Label {
                                text: "较上月 +0%"
                                font.pixelSize: 12
                                color: "#4CAF50"
                            }
                        }
                    }
                }
            }
        }
    }

    Component {
        id: addEntryPage
        Page {
            title: qsTr("添加记录")
            background: Rectangle { color: "#F8F9FA" }
            
            Rectangle {
                anchors.fill: parent
                anchors.margins: 16
                color: "white"
                radius: 12
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 16
                    
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        
                        Button {
                            Layout.preferredWidth: 100
                            text: qsTr("支出")
                            highlighted: true
                            Material.accent: "#F44336"
                        }
                        
                        Button {
                            Layout.preferredWidth: 100
                            text: qsTr("收入")
                            flat: true
                        }
                    }
                    
                    TextField {
                        Layout.fillWidth: true
                        placeholderText: qsTr("¥0.00")
                        font.pixelSize: 24
                        inputMethodHints: Qt.ImhFormattedNumbersOnly
                        horizontalAlignment: TextInput.AlignRight
                    }
                    
                    Rectangle {
                        Layout.fillWidth: true
                        height: 1
                        color: "#EEEEEE"
                    }
                    
                    Label {
                        text: qsTr("分类")
                        font.pixelSize: 16
                        color: "#333333"
                    }
                    
                    GridLayout {
                        Layout.fillWidth: true
                        columns: 4
                        rowSpacing: 12
                        columnSpacing: 12
                        
                        Repeater {
                            model: expenseCategories
                            
                            Rectangle {
                                Layout.preferredWidth: 60
                                Layout.preferredHeight: 60
                                color: modelData.color
                                radius: 8
                                
                                ColumnLayout {
                                    anchors.centerIn: parent
                                    spacing: 4
                                    
                                    Label {
                                        Layout.alignment: Qt.AlignHCenter
                                        text: modelData.icon
                                        font.pixelSize: 20
                                    }
                                    
                                    Label {
                                        Layout.alignment: Qt.AlignHCenter
                                        text: modelData.name
                                        font.pixelSize: 12
                                    }
                                }
                            }
                        }
                    }
                    
                    TextField {
                        Layout.fillWidth: true
                        placeholderText: qsTr("添加备注...")
                    }
                    
                    Item { Layout.fillHeight: true }
                    
                    Button {
                        Layout.fillWidth: true
                        text: qsTr("保存")
                        highlighted: true
                        onClicked: stackView.pop()
                    }
                }
            }
        }
    }

    footer: Rectangle {
        id: tabBar
        height: 60
        color: "white"
        
        Rectangle {
            width: parent.width
            height: 1
            color: "#EEEEEE"
        }
        
        property int currentIndex: 0
        
        Row {
            anchors.fill: parent
            
            // 首页按钮
            Rectangle {
                width: parent.width / 4
                height: parent.height
                color: tabBar.currentIndex === 0 ? "#F5F5F5" : "white"
                
                Column {
                    anchors.centerIn: parent
                    spacing: 4
                    
                    Text { 
                        text: "🏠"
                        font.pixelSize: 20
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                    
                    Text {
                        text: "首页"
                        font.pixelSize: 12
                        color: tabBar.currentIndex === 0 ? "#4785FF" : "#9E9E9E"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                }
                
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        tabBar.currentIndex = 0;
                        stackView.replace(homePage);
                    }
                }
            }
            
            // 明细按钮
            Rectangle {
                width: parent.width / 4
                height: parent.height
                color: tabBar.currentIndex === 1 ? "#F5F5F5" : "white"
                
                Column {
                    anchors.centerIn: parent
                    spacing: 4
                    
                    Text { 
                        text: "📝"
                        font.pixelSize: 20
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                    
                    Text {
                        text: "明细"
                        font.pixelSize: 12
                        color: tabBar.currentIndex === 1 ? "#4785FF" : "#9E9E9E"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                }
                
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        tabBar.currentIndex = 1;
                        stackView.replace(transactionsPage);
                    }
                }
            }
            
            // 统计按钮
            Rectangle {
                width: parent.width / 4
                height: parent.height
                color: tabBar.currentIndex === 2 ? "#F5F5F5" : "white"
                
                Column {
                    anchors.centerIn: parent
                    spacing: 4
                    
                    Text { 
                        text: "📊"
                        font.pixelSize: 20
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                    
                    Text {
                        text: "统计"
                        font.pixelSize: 12
                        color: tabBar.currentIndex === 2 ? "#4785FF" : "#9E9E9E"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                }
                
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        tabBar.currentIndex = 2;
                        stackView.replace(statsPage);
                    }
                }
            }
            
            // 我的按钮
            Rectangle {
                width: parent.width / 4
                height: parent.height
                color: tabBar.currentIndex === 3 ? "#F5F5F5" : "white"
                
                Column {
                    anchors.centerIn: parent
                    spacing: 4
                    
                    Text { 
                        text: "👤"
                        font.pixelSize: 20
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                    
                    Text {
                        text: "我的"
                        font.pixelSize: 12
                        color: tabBar.currentIndex === 3 ? "#4785FF" : "#9E9E9E"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                }
                
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        tabBar.currentIndex = 3;
                    }
                }
            }
        }
    }
}
"""

class LedgerBackend(QObject):
    """简单的后端逻辑类，用于未来扩展功能"""
    
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # 创建后端实例并暴露给QML
    backend = LedgerBackend()
    engine.rootContext().setContextProperty("backend", backend)
    
    # 从字符串加载QML代码
    engine.loadData(QML_CODE.encode('utf-8'))
    
    if not engine.rootObjects():
        sys.exit(-1)
    
    sys.exit(app.exec())
