import sys
import io
import folium # pip install folium
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication, QInputDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from PyQt5.QtCore import *
from PyQt5.QtGui import *

"""
Folium in PyQt5
"""
class MyMarker():
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.marker = folium.Marker(location=[self.x, self.y], popup = self.name, icon=folium.Icon(color = 'red'))
        
    def __str__(self):
        return self.name
        

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        #self.window_width, self.window_height = 800, 600
        #self.setMinimumSize(self.window_width, self.window_height)
        
        self.markers_pull = []
        self.count = 0
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        button_layout = QVBoxLayout()
        button_layout.addStretch(0)
        self.layout.addLayout(button_layout)
        
        
        bluetooth_list_button = QtWidgets.QPushButton()
        bluetooth_list_button.setText("Список устройств")
        bluetooth_list_button.setFixedWidth(500)
        
        button_layout.insertWidget(0, bluetooth_list_button)
        
        goto_point_button = QtWidgets.QPushButton()
        goto_point_button.setText("Переместиться на координаты")
        goto_point_button.setFixedWidth(500)
        goto_point_button.clicked.connect(self.goto_point)
        
        button_layout.insertWidget(0, goto_point_button)
        
        point_list_button = QtWidgets.QPushButton()
        point_list_button.setText("Список точек")
        point_list_button.setFixedWidth(500)
        point_list_button.clicked.connect(self.show_markers)
        
        button_layout.insertWidget(0, point_list_button)
        
        delete_point_button = QtWidgets.QPushButton()
        delete_point_button.setText("Удалить точку")
        delete_point_button.setFixedWidth(500)
        delete_point_button.clicked.connect(self.delete_marker)
        
        button_layout.insertWidget(0, delete_point_button)
        
        set_new_point_button = QtWidgets.QPushButton()
        set_new_point_button.setText("Задать новую точку")
        set_new_point_button.setFixedWidth(500)
        
        button_layout.insertWidget(0, set_new_point_button)
        
        # set_new_point_button.clicked.connect(lambda event, x=55.9321545, y=37.5482585, name='TEST ONE': self.create_marker(event, x, y, name))
        set_new_point_button.clicked.connect(self.create_marker)

        coordinate = (55.9321525, 37.5282565)
        self.m = folium.Map(
        	tiles='Stamen Terrain',
        	zoom_start=13,
        	location=coordinate
        )
        
        
        # save map data to data object
        data = io.BytesIO()
        self.m.save(data, close_file=False)

        self.webView = QWebEngineView()
        self.webView.move(100, 100)
        self.webView.setHtml(data.getvalue().decode())
        self.layout.addWidget(self.webView)
        

    def create_marker(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Введите данные(не используйте запятые!):')
        if ok:
            try:
                values = text.split(' ')
                x = float(values[0])
                y = float(values[1])
                name = values[2]
                print("Hello!")
            except:
                print("Exception occured!")
            else:
                for c in self.markers_pull:
                    if c.name == name:
                        QMessageBox.about(self, "Ошибка", "Такое имя занято!")
                        return
                    
                self.markers_pull.append(MyMarker(x, y, name))
                self.markers_pull[self.count].marker.add_to(self.m)
                self.count += 1
                self.m.location = (x, y)
                data = io.BytesIO()
                self.m.save(data, close_file=False)
                self.webView.setHtml(data.getvalue().decode())



    def delete_marker(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Введите данные(не используйте запятые!):')
        if ok:
            for i in range(len(self.markers_pull)):
                print('текущее значение итератора', i)
                if self.markers_pull[i].name == text:
                    print('found!')
                    del self.markers_pull[i]
                    for a in self.markers_pull:
                        print(a)
                    del self.m
                    self.layout.removeWidget(self.webView)
                    coordinate = (55.9321525, 37.5282565)
                    self.m = folium.Map(
                        tiles='Stamen Terrain',
                        zoom_start=13,
                        location=coordinate
                    )
                    for element in self.markers_pull:
                        element.marker.add_to(self.m)
                    data = io.BytesIO()
                    self.m.save(data, close_file=False)

                    self.webView = QWebEngineView()
                    self.webView.move(100, 100)
                    self.webView.setHtml(data.getvalue().decode())
                    self.layout.addWidget(self.webView)
                    return
            QMessageBox.about(self, "Ошибка", "Нет такой метки!")
                    
        
                        
    def show_markers(self):
        text = ''
        if len(self.markers_pull):
            for c in self.markers_pull:
                text += "x=" + str(c.x) + " y=" + str(c.y) + " name=" + c.name + "\n"
        else:
            text = 'Нет меток'
        print(text)
        QMessageBox.about(self, "Список меток", text)
        
        
    def goto_point(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Введите данные(не используйте запятые!):')
        if ok:
            try:
                values = text.split(' ')
                x = float(values[0])
                y = float(values[1])
            except:
                print("Exception occured!")
            else:
                self.m.location = (x, y)
                data = io.BytesIO()
                self.m.save(data, close_file=False)
                self.webView.setHtml(data.getvalue().decode())
         

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    
    myApp = MyApp()
    myApp.showMaximized()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')