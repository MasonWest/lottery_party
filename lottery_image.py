# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 17:18:41 2023

@author: Administrator
"""
import os
from PyQt5.QtCore import QThread,pyqtSignal,QTimer,Qt
from PyQt5.QtGui import QResizeEvent,QPixmap,QFont,QLinearGradient,QColor,QGradient,QBrush,QPalette,QFontMetrics
from PyQt5.QtWidgets import QMainWindow,QApplication,QLabel,QVBoxLayout,QHBoxLayout,QLineEdit,QPushButton,QWidget,QGraphicsView,QGraphicsScene,QGraphicsPixmapItem,QGraphicsTextItem
import json
import random

class Lottery(QThread):
    signal = pyqtSignal(list)
    def __init__(self, num,image_files):
        super().__init__()

    def run(self):
        selected_names = random.sample(self.list,self.num)
        self.signal.emit(selected_names)

        
class LotteryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_folder = "avatar" # 你的头像文件夹路径
        self.initUI()
        self.warningDialog = None # 警告对话框
    
    def read_program_name(self):
            with open('config.json', 'r', encoding="utf-8") as file:
                config = json.load(file)
                return config['program_name']
    def read_title(self):
            with open('config.json', 'r', encoding="utf-8") as file:
                config = json.load(file)
                return config['title']
    def closeEvent(self, event):
        self.lottery.terminate()
        self.lottery.wait()
        event.accept()
        #
    def initUI(self):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        self.setGeometry(0, 0, 1600, 1000)
        # title=self.read_title()
        self.setWindowTitle(self.read_program_name())
        self.backgroundLabel = QLabel(self)
        self.backgroundLabel.setGeometry(self.rect())
        self.backgroundLabel.setPixmap(QPixmap("lottery_bg.png"))
        self.backgroundLabel.setScaledContents(True)
        self.list = self.getPeopleList()
        

        layout = QVBoxLayout(self)
        hbox = QHBoxLayout()
        self.noteLable = QLabel(self)
        self.noteLable.setText("请输入抽奖人数：")
        
        self.noteLable.setStyleSheet("color: black;")
        font = QFont("楷体",15)  # 设置字体为楷体，大小为20
        self.noteLable.setFont(font)
        hbox.addWidget(self.noteLable)
        
        self.input = QLineEdit(self)
        font = QFont("楷体", 15)  # 设置输入框字体大小
        self.input.setFont(font)
        
        self.resetBt = QPushButton(self)
        self.resetBt.setText("重置")
        self.resetBt.clicked.connect(self.resetList)
        
        
        hbox.addWidget(self.input)
        hbox.addWidget(self.resetBt)
        layout.addLayout(hbox)
        
        hbox2 = QHBoxLayout()
        self.dateLabel = QLabel(self)
        self.dateLabel.setText(self.read_title())

        self.dateLabel.setFont(QFont("微软雅黑",90))  # 设置初始字体大小

        layout.addWidget(self.dateLabel)
        
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        gradient = QLinearGradient(0, 0, 300, 0)
        gradient.setColorAt(0, QColor(148, 0, 211)) # 紫色
        gradient.setColorAt(0.2, QColor(186, 85, 211)) # 深紫色
        gradient.setColorAt(0.4, QColor(218, 112, 214)) # 粉紫色
        gradient.setColorAt(0.6, QColor(238, 130, 238)) # 蓝紫色
        gradient.setColorAt(0.8, QColor(255, 105, 180)) # 热情粉红色
        gradient.setColorAt(1, QColor(255, 20, 147)) # 深粉红色
        gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        brush = QBrush(gradient)
        # 创建调色板对象并设置画刷
        palette = QPalette()
        palette.setBrush(self.dateLabel.foregroundRole(), brush)
        self.dateLabel.setPalette(palette)
        hbox2.addWidget(self.dateLabel)
        
        self.resultLable = QLabel(self)
        self.resultLable.setStyleSheet("border: 2px solid white;")
        self.resultLable.setWordWrap(True)  # 设置自动换行
        font = QFont("楷体", 60)  # 设置名单人员字体为楷体，大小为20
        self.resultLable.setFont(font) 
        self.resultLable.setStyleSheet("color: white;")
        hbox2.addWidget(self.resultLable)      
        self.resultImage = QLabel(self)   
        hbox2.addWidget(self.resultImage)
        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.setStyleSheet("background: transparent;")
        hbox2.addWidget(self.graphics_view)
        layout.addLayout(hbox2)      
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.startLottery)
        self.startBt = QPushButton(self)
        self.startBt.setText("开始抽奖")

        layout.addWidget(self.startBt)
        self.startBt.clicked.connect(self.startLottery)
        self.confirmBt = QPushButton(self)
        self.confirmBt.setText("停止")
        layout.addWidget(self.confirmBt)

        self.confirmBt.clicked.connect(self.stopLottery)
        self.setLayout(layout)
              
        self.lottery = Lottery(0,[])
        self.lottery.signal.connect(self.showResult)
        
    def resizeEvent(self , event: QResizeEvent):
        self.backgroundLabel.setGeometry(self.rect())
        self.adjustFontSize()
        super().resizeEvent(event)

    def adjustFontSize(self):
        font = self.dateLabel.font()
        fm = QFontMetrics(font)
        textWidth = fm.width(self.dateLabel.text())
        windowWidth = self.centralWidget().width()

    # 根据窗口宽度和文本宽度来调整字体大小
        if textWidth > windowWidth:
            fontSize = font.pointSize() * windowWidth / textWidth
            font.setPointSizeF(fontSize)
            self.dateLabel.setFont(font)
        
    def getPeopleList(self):
        
        list = []

        for filename in os.listdir(self.image_folder):
            if filename.endswith(".png"):
                participant_name = os.path.splitext(filename)[0]
                participant_image = os.path.join(self.image_folder, filename)
                list.append((participant_name))
        return list
    
    
    def startLottery(self):
        num = self.insert_point()
        if num:
            num = int(num)
            if num > len(self.list):
                QMessageBox.warning(self, "警告", "抽取数量超过了可抽人数！剩余可抽人数为："+str(len(self.list)))
            else:
                
                self.lottery.num = num
                self.lottery.list = self.list
                self.lottery.start()
                self.timer.start(70)
            
    def insert_point(self):
        var = self.input.text()
        return var
    def showResult(self, selected_names):
        # self.image_folder = "avatar"
        self.graphics_scene.clear()
        self.text_items = [] 
        
        # 计算总高度
        total_height = len(selected_names) * 190
    
        # 计算开始位置，使其垂直居中
        offset_y = (self.graphics_view.height() - total_height) / 2
    
        # 遍历所有头像
        for i, image_name in enumerate(selected_names):
            person_name = os.path.splitext(image_name)[0]
            image_path = os.path.join(self.image_folder, image_name)
            
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaledToWidth(150)
        
            # 创建 QGraphicsPixmapItem
            pixmap_item = QGraphicsPixmapItem(pixmap)
            pixmap_item.setPos(0, offset_y + i * 190)  # 设置每张图片的垂直位置，加入偏移量
            
            text_item = QGraphicsTextItem(person_name)
            font = QFont("楷体", 60)  # 选择字体和大小
            text_item.setFont(font)  # 设置字体
            text_color = QColor(255, 255, 255)  # 设置为白色
            text_item.setDefaultTextColor(text_color)
            text_item.setPos(-300, offset_y + i * 190 + 50)  # 调整文本位置，加入偏移量
        
            self.graphics_scene.addItem(pixmap_item)
            self.graphics_scene.addItem(text_item)
            self.text_items.append(text_item)
        
        # 将 QGraphicsView 添加到布局中
        self.layout().addWidget(self.graphics_view)


            
    def stopLottery(self):
        self.timer.stop()   
        result_names = [item.toPlainText() for item in self.text_items]
        result = "\n".join(result_names)
        print(result)
        with open("名单.txt", "a") as file:
            file.write(result + "\n")
        self.used_list = []
        with open("名单.txt", "r") as file:
            self.used_list = file.read().splitlines()
        filtered_list = [name for name in self.list if name not in self.used_list]
        self.list = filtered_list
        self.input.setText("")  # 清空输入框
              
    def resetList(self):
        with open("名单.txt", "w") as file:
            file.write("")
        self.used_list=[]
        self.list = self.getPeopleList()
        self.resultLable.setText("")  # 清空结果标签
        self.graphics_view.scene().clear()
if __name__ == '__main__':
    app = QApplication([])
    
    window = LotteryWindow()
    window.show()
    app.exec_()
    
    