import hou
import os
import json
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QDialog, QMenu, QAction, QLabel, QTextEdit
from PySide2 import QtWidgets, QtCore

class TodoListApp(QDialog):
    def __init__(self):
        super().__init__(None, QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Todo List')
        self.setGeometry(100, 100, 400, 300)

        self.todo_file = None  # Initialize todo file path
        self.loadTodoList()
        self.initUI()

        # Connect to Houdini file load event
        hou.hipFile.addEventCallback(self.onHipFileLoad)

        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

    def initUI(self):
        # Layout
        layout = QVBoxLayout()

        # Todo List
        self.todo_list = QListWidget()
        self.populateTodoList()

        # Input Field
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        add_button = QPushButton('Add')
        add_button.clicked.connect(self.addTodo)
        clear_button = QPushButton('Clear All')
        clear_button.clicked.connect(self.clearAll)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(add_button)
        input_layout.addWidget(clear_button)

        layout.addWidget(self.todo_list)
        layout.addLayout(input_layout)

        self.setLayout(layout)

    def loadTodoList(self):
        hipfile = hou.hipFile.path()
        hipfile_name = os.path.basename(hipfile)
        todo_file_name = hipfile_name.rsplit('.', 1)[0] + '_todo.json'  # Construct todo file name
        self.todo_file = os.path.join(os.path.dirname(hipfile), todo_file_name)
        if os.path.exists(self.todo_file):
            with open(self.todo_file, 'r') as f:
                self.todo_data = json.load(f)
        else:
            self.todo_data = []

    def saveTodoList(self):
        try:
            with open(self.todo_file, 'w') as f:
                json.dump(self.todo_data, f)
                print("Todo list saved to:", self.todo_file)
        except Exception as e:
            print("Error saving todo list:", e)

    def populateTodoList(self):
        self.todo_list.clear()
        for todo in self.todo_data:
            item = QListWidgetItem(todo['task'])
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if 'completed' in todo and todo['completed']:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            self.todo_list.addItem(item)

        self.todo_list.itemChanged.connect(self.updateTodoStatus)
        self.todo_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.todo_list.customContextMenuRequested.connect(self.showContextMenu)

    def addTodo(self):
        todo_text = self.input_field.text()
        if todo_text:
            # Create a custom widget with a checkbox and label
            item = {'task': todo_text, 'completed': False, 'comment': ''}
            self.todo_data.append(item)
            self.saveTodoList()
            self.populateTodoList()
            self.input_field.clear()
        else:
            QMessageBox.warning(self, 'Warning', 'Please enter a task!')

    def updateTodoStatus(self, item):
        index = self.todo_list.indexFromItem(item).row()
        self.todo_data[index]['completed'] = (item.checkState() == QtCore.Qt.Checked)
        self.saveTodoList()

    def clearAll(self):
        reply = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to remove all tasks?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.todo_data = []
            self.saveTodoList()
            self.populateTodoList()

    def closeEvent(self, event):
        event.accept()

    def onHipFileLoad(self, event_type):
        # Reload Todo List data when a new file is loaded
        self.loadTodoList()
        self.populateTodoList()

    def showContextMenu(self, pos):
        menu = QMenu(self)
        notes_action = menu.addAction("Notes")
        action = menu.exec_(self.todo_list.mapToGlobal(pos))
        if action == notes_action:
            selected_items = self.todo_list.selectedItems()
            if selected_items:
                index = self.todo_list.indexFromItem(selected_items[0]).row()
                comment_dialog = CommentDialog(self.todo_data[index].get('comment', ''))
                if comment_dialog.exec_():
                    self.todo_data[index]['comment'] = comment_dialog.getComment()
                    self.saveTodoList()

class CommentDialog(QDialog):
    def __init__(self, comment):
        super().__init__()
        self.setWindowTitle('Comment')
        self.setGeometry(200, 200, 300, 200)

        self.comment = QTextEdit()
        self.comment.setPlainText(comment)

        layout = QVBoxLayout()
        layout.addWidget(self.comment)

        button_layout = QHBoxLayout()
        save_button = QPushButton('Save')
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def getComment(self):
        return self.comment.toPlainText()

# Create and show the todo app
app = QApplication.instance() or QApplication([])
todo_app = TodoListApp()
todo_app.show()

# Start the Houdini event loop
hou.ui.setMainEditorGeometry(todo_app.geometry())
app.exec_()

print("Reached end of script.")
