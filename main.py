import hou
import os
import json
import PySide2.QtWidgets as QtWidgets
from PySide2 import QtCore

style = "C:/Desktop/stylesheet.css" # Replace this with your own stylesheet
credit_for_stylesheet = "https://github.com/Lumyo/darkorange-pyside-stylesheet" 

# TODO: Add rename function
# TODO: Add delete entry function

class TodoListApp(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TodoListApp, self).__init__(parent)
        self.setWindowTitle('IAN To-Do')
        self.setGeometry(100, 100, 400, 300)
        self.center()
        self.todo_file = None
        self.loadTodoList()
        self.initUI()

        # Connect to Houdini file load event
        hou.hipFile.addEventCallback(self.onHipFileLoad)

        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.comment_dialog = None

        # Apply stylesheet
        self.setStyleSheetFromFile(style)

    def center(self):
        screen_geometry = QtWidgets.QDesktopWidget().screenGeometry()
        center_point = screen_geometry.center()
        self.move(center_point - self.rect().center())

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        self.todo_list = QtWidgets.QListWidget()
        self.populateTodoList()

        input_layout = QtWidgets.QHBoxLayout()
        self.input_field = QtWidgets.QLineEdit()
        add_button = QtWidgets.QPushButton('Add')
        add_button.clicked.connect(self.addTodo)
        clear_button = QtWidgets.QPushButton('Clear All')
        clear_button.clicked.connect(self.clearAll)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(add_button)
        input_layout.addWidget(clear_button)

        layout.addWidget(self.todo_list)
        layout.addLayout(input_layout)

        self.setLayout(layout)

        self.todo_list.itemDoubleClicked.connect(self.showOrUpdateCommentDialog)

    def mousePressEvent(self, event):
        if self.comment_dialog and self.comment_dialog.isVisible():
            self.comment_dialog.close()
        super().mousePressEvent(event)

    def showOrUpdateCommentDialog(self, item):
        index = self.todo_list.indexFromItem(item).row()
        comment = self.todo_data[index].get('comment', '')
        if self.comment_dialog and self.comment_dialog.isVisible():
            current_index = self.comment_dialog.current_index
            if index == current_index:
                self.comment_dialog.updateComment(index, comment)
            else:
                self.comment_dialog.close()
                self.comment_dialog = CommentDialog(comment, index)
                self.comment_dialog.move(self.geometry().right(), self.geometry().top())
                self.comment_dialog.show()
        else:
            self.comment_dialog = CommentDialog(comment, index)
            self.comment_dialog.move(self.geometry().right(), self.geometry().top())
            self.comment_dialog.show()

    # Add rename function
    def renameTodoItem(self, item):
        index = self.todo_list.indexFromItem(item).row()
        current_task = self.todo_data[index]['task']
        new_task, ok = QtWidgets.QInputDialog.getText(self, 'Rename Task', 'Enter new task name:', text=current_task)
        if ok and new_task.strip():
            self.todo_data[index]['task'] = new_task.strip()
            self.saveTodoList()
            self.populateTodoList()
        elif ok:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Task name cannot be empty!')
    
    # Add delete entry function
    def deleteTodoItem(self, item):
        index = self.todo_list.indexFromItem(item).row()
        reply = QtWidgets.QMessageBox.question(
            self,
            'Confirmation',
            f'Are you sure you want to delete the task "{self.todo_data[index]["task"]}"?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            del self.todo_data[index]
            self.saveTodoList()
            self.populateTodoList()
    
    # Modify the context menu to include Rename and Delete
    def showContextMenu(self, pos):
        menu = QtWidgets.QMenu(self)
        notes_action = menu.addAction("Show Notes")
        rename_action = menu.addAction("Rename Task")
        delete_action = menu.addAction("Delete Task")
    
        action = menu.exec_(self.todo_list.mapToGlobal(pos))
        selected_items = self.todo_list.selectedItems()
    
        if selected_items:
            item = selected_items[0]
            if action == notes_action:
                self.showOrUpdateCommentDialog(item)
            elif action == rename_action:
                self.renameTodoItem(item)
            elif action == delete_action:
                self.deleteTodoItem(item)

    def loadTodoList(self):
        hipfile = hou.hipFile.path()
        hipfile_name = os.path.basename(hipfile)
        todo_file_name = hipfile_name.rsplit('.', 1)[0] + '_todo.json'
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
                # print("Todo list saved to:", self.todo_file)
        except Exception as e:
            print("Error saving todo list:", e)

    def populateTodoList(self):
        self.todo_list.clear()
        for todo in self.todo_data:
            item = QtWidgets.QListWidgetItem(todo['task'])
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
            item = {'task': todo_text, 'completed': False, 'comment': ''}
            self.todo_data.append(item)
            self.saveTodoList()
            self.populateTodoList()
            self.input_field.clear()
        else:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Please enter a task!')

    def updateTodoStatus(self, item):
        index = self.todo_list.indexFromItem(item).row()
        self.todo_data[index]['completed'] = (item.checkState() == QtCore.Qt.Checked)
        self.saveTodoList()

    def clearAll(self):
        reply = QtWidgets.QMessageBox.question(self, 'Confirmation', 'Are you sure you want to remove all tasks?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.todo_data = []
            self.saveTodoList()
            self.populateTodoList()

    def closeEvent(self, event):
        event.accept()

    def onHipFileLoad(self, event_type):
        self.loadTodoList()
        self.populateTodoList()

    def showContextMenu(self, pos):
        menu = QtWidgets.QMenu(self)
        notes_action = menu.addAction("Notes")
        action = menu.exec_(self.todo_list.mapToGlobal(pos))
        if action == notes_action:
            selected_items = self.todo_list.selectedItems()
            if selected_items:
                self.showOrUpdateCommentDialog(selected_items[0])

    def updateComment(self, index, comment):
        if index < len(self.todo_data):
            self.todo_data[index]['comment'] = comment
            self.saveTodoList()

    def setStyleSheetFromFile(self, path):
        with open(path, 'r') as file:
            self.setStyleSheet(file.read())

class CommentDialog(QtWidgets.QDialog):
    def __init__(self, comment, index):
        super().__init__()
        self.setWindowTitle('Notes')
        self.setGeometry(200, 200, 300, 200)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint, False)
        self.current_index = index
        self.comment = QtWidgets.QTextEdit()
        self.comment.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.comment.setText(comment)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.comment)

        button_layout = QtWidgets.QHBoxLayout()
        save_button = QtWidgets.QPushButton('Save')
        save_button.clicked.connect(lambda: self.accept(index))
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.setStyleSheetFromFile(style)

    def getComment(self):
        return self.comment.toPlainText()

    def accept(self, index):
        comment = self.getComment()
        super().accept()
        if comment:
            todo_app.updateComment(index, comment)

    def setStyleSheetFromFile(self, path):
        with open(path, 'r') as file:
            self.setStyleSheet(file.read())

app = QtWidgets.QApplication.instance()
todo_app = TodoListApp()
todo_app.show()
