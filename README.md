# To-Do tool for Houdini
![alt text](https://github.com/ianistor/ian_houdini_todo/blob/main/todo_ui2.png)
Wrote a quick tool to create a TO-DO list in Houdini using PySide.
I'll be honest, the need for it was a bit forced as Houdini's own post it notes do the trick most of the time, but i wanted to see how i would tackle this.
I'm thinking this can be a good base for a feedback tool/or jira/shotgun integration tho.\
![alt_text](https://github.com/ianistor/ian_houdini_todo_tool/blob/main/showcase_todo_tool.gif)
## Features

• Local .json file holds all the information, so it can be submited on p4v/git for others to have access to it.
On each hip file a new _todo.json file gets created, so if you swap between .hip that will update as well.\
![alt text](https://github.com/ianistor/ian_houdini_todo/blob/main/folder2.png)\
![alt text](https://github.com/ianistor/ian_houdini_todo/blob/main/folder1.png)\
• Notes features (each "task" can hold aditional information as notes)\
![alt text](https://github.com/ianistor/ian_houdini_todo/blob/main/todo_ui.png)\

Stylesheet credits : https://github.com/Lumyo/darkorange-pyside-stylesheet
