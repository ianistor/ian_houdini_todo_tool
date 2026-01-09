# for pyside 2

import hou
import os
import json
import PySide2.QtWidgets as QtWidgets
from PySide2 import QtCore

css = """
QToolTip
{
     border: 1px solid black;
     background-color: #ffa02f;
     padding: 1px;
     border-radius: 3px;
     opacity: 50;
}

QWidget
{
    color: #ffffff;
    background-color: #323232;
}

QHeaderView::section {
    background-color: #836666; /* Set the background color to transparent */
    /* Other style properties */
}

QWidget:item:hover
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #C27923, stop: 1 #ffa02f);
    color: #000000;
}

QWidget:item:selected
{
    background-color: #ffa02f;
}

QMenuBar::item
{
    background: transparent;
}

QMenuBar::item:selected
{
    background: transparent;
    border: 0.1px solid #24221e;
}

QLabel[tag="groupbox_title"] {
    background: transparent;
    color: rgb(240,240,240);
}
/********* QLabel ********/
QLabel, QLabel:enabled {
    background: transparent;
}
QMenuBar::item:pressed
{
    background: #444;
    border: 1px solid #000;
    background-color: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:1 #212121,
        stop:0.4 #343434/,
        stop:0.2 #343434,
        stop:0.1 #ffaa00/
    );
    margin-bottom:-1px;
    padding-bottom:1px;
}

QMenu
{
    border: 1px solid #000;
}

QMenu::item
{
    padding: 2px 20px 2px 20px;
}

QMenu::item:selected
{
    color: #000000;
}

QAbstractItemView
{
    background-color:#242424;
}

QWidget:focus
{
    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}

QLineEdit
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);
    padding: 1px;
    border-style: solid;
    border: 1px solid #1e1e1e;
    border-radius: 5;
}

QPushButton
{
    color: white;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
    border-width: 1px;
    border-color: #1e1e1e;
    border-style: solid;
    border-radius: 6;
    padding: 3px;
    font-size: 12px;
    padding-left: 5px;
    padding-right: 5px;
}

QPushButton:pressed
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
}

QComboBox
{
    selection-background-color: #ffaa00;
    background-color:#b1b1b1 ;
    border-style: solid;
    border: 1px solid #1e1e1e;
    border-radius: 5;
}

QComboBox:hover,QPushButton:hover
{
    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}

QComboBox:on
{
    padding-top: 3px;
    padding-left: 4px;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
    selection-background-color: #ffaa00;
}

QComboBox QAbstractItemView
{
    border: 2px solid rgb(77, 76, 76);
    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}

QComboBox::drop-down
{
     subcontrol-origin: padding;
     subcontrol-position: top right;
     width: 15px;

     border-left-width: 0px;
     border-left-color: darkgray;
     border-left-style: solid; /* just a single line */
     border-top-right-radius: 3px; /* same radius as the QComboBox */
     border-bottom-right-radius: 3px;
 }


QGroupBox:focus
{
border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}

QTextEdit:focus
{
    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}

QScrollBar:horizontal {
     border: 1px solid #222222;
     background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);
     height: 7px;
     margin: 0px 16px 0 16px;
}

QScrollBar::handle:horizontal
{
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);
      min-height: 20px;
      border-radius: 2px;
}

QScrollBar::add-line:horizontal {
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);
      width: 14px;
      subcontrol-position: right;
      subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);
      width: 14px;
     subcontrol-position: left;
     subcontrol-origin: margin;
}

QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal
{
      border: 1px solid black;
      width: 1px;
      height: 1px;
      background: white;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
{
      background: none;
}

QScrollBar:vertical
{
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);
      width: 7px;
      margin: 16px 0 16px 0;
      border: 1px solid #222222;
}

QScrollBar::handle:vertical
{
      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);
      min-height: 20px;
      border-radius: 2px;
}

QScrollBar::add-line:vertical
{
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
      height: 14px;
      subcontrol-position: bottom;
      subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical
{
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 1 #ffa02f);
      height: 14px;
      subcontrol-position: top;
      subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
{
      border: 1px solid black;
      width: 1px;
      height: 1px;
      background: white;
}


QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
{
      background: none;
}

QTextEdit
{
    background-color: #242424;
}

QPlainTextEdit
{
    background-color: #242424;
}

QHeaderView::section
{
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);
    color: white;
    padding-left: 4px;
    border: 1px solid #6c6c6c;
}

QCheckBox:disabled
{
color: #414141;
}

QDockWidget::title
{
    text-align: center;
    spacing: 3px; /* spacing between items in the tool bar */
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);
}

QDockWidget::close-button, QDockWidget::float-button
{
    text-align: center;
    spacing: 1px; /* spacing between items in the tool bar */
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);
}

QDockWidget::close-button:hover, QDockWidget::float-button:hover
{
    background: #242424;
}

QDockWidget::close-button:pressed, QDockWidget::float-button:pressed
{
    padding: 1px -1px -1px 1px;
}

QMainWindow::separator
{
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);
    color: white;
    padding-left: 4px;
    border: 1px solid #4c4c4c;
    spacing: 3px; /* spacing between items in the tool bar */
}


QMainWindow::separator:hover
{

    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);
    color: white;
    padding-left: 4px;
    border: 1px solid #6c6c6c;
    spacing: 3px; /* spacing between items in the tool bar */
}

QToolBar::handle
{
     spacing: 3px; /* spacing between items in the tool bar */
     background: url(:/images/handle.png);
}

QMenu::separator
{
    height: 2px;
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);
    color: white;
    padding-left: 4px;
    margin-left: 10px;
    margin-right: 5px;
}

QProgressBar
{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center;
}

QProgressBar::chunk
{
    background-color: #d7801a;
    width: 2.15px;
    margin: 0.5px;
}

QTabBar::tab {
    color: #b1b1b1;
    border: 1px solid #444;
    border-bottom-style: none;
    background-color: #323232;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 2px;
    margin-right: -1px;
}

QTabWidget::pane {
    border: 1px solid #444;
    top: 1px;
}

QTabBar::tab:last
{
    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
    border-top-right-radius: 3px;
}

QTabBar::tab:first:!selected
{
 margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */


    border-top-left-radius: 3px;
}

QTabBar::tab:!selected
{
    color: #b1b1b1;
    border-bottom-style: solid;
    margin-top: 3px;
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #343434);
}

QTabBar::tab:selected
{
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    margin-bottom: 0px;
}

QTabBar::tab:!selected:hover
{
    border-top: 2px solid #ffaa00;
    padding-bottom: 3px; */
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #343434, stop:0.2 #343434, stop:0.1 #ffaa00);
}

QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{
    color: #b1b1b1;
    background-color: #323232;
    border: 1px solid #b1b1b1;
    border-radius: 6px;
}

QRadioButton::indicator:checked
{
    background-color: qradialgradient(
        cx: 0.5, cy: 0.5,
        fx: 0.5, fy: 0.5,
        radius: 1.0,
        stop: 0.25 #ffaa00,
        stop: 0.3 #323232
    );
}

QCheckBox::indicator{
    color: #b1b1b1;
    background-color: #323232;
    border: 1px solid #b1b1b1;
    width: 9px;
    height: 9px;
}

QRadioButton::indicator
{
    border-radius: 6px;
}

QRadioButton::indicator:hover, QCheckBox::indicator:hover
{
    border: 1px solid #d7801a;
}

QCheckBox::indicator:checked
{
    image:url(:/images/checkbox.png);
}

QCheckBox::indicator:disabled, QRadioButton::indicator:disabled
{
    border: 1px solid #444;
}

QDialog::title {
    background-color: #d7801a; /* Make the header transparent */
    /* Other style properties */
}

"""

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
        
        # Ask for confirmation before deletion
        reply = QtWidgets.QMessageBox.question(
            self,
            'Confirmation',
            f'Are you sure you want to delete the task "{self.todo_data[index]["task"]}"?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        # If confirmed, proceed with deletion
        if reply == QtWidgets.QMessageBox.Yes:
            del self.todo_data[index]
            self.saveTodoList()
            self.todo_list.takeItem(index)



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
                menu.close()

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

    def updateComment(self, index, comment):
        if index < len(self.todo_data):
            self.todo_data[index]['comment'] = comment
            self.saveTodoList()


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


    def getComment(self):
        return self.comment.toPlainText()

    def accept(self, index):
        comment = self.getComment()
        super().accept()
        if comment:
            todo_app.updateComment(index, comment)
    


app = QtWidgets.QApplication.instance()
app.setStyleSheet( css )
todo_app = TodoListApp()
todo_app.show()
