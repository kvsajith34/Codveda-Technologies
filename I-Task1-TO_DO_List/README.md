# 📝 To-Do List Application

A clean, professional, and beginner-friendly command-line To-Do List application built with Python. This project demonstrates modular programming, proper error handling, and persistent data storage using JSON.

---

## 🎯 Project Overview

This application allows users to manage their daily tasks through a simple terminal interface. Tasks are stored persistently in a JSON file, ensuring data remains available even after the application closes.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ➕ **Add Task** | Create new tasks with custom descriptions |
| 📋 **View Tasks** | Display all tasks with completion status |
| ✅ **Mark Complete** | Change task status from pending to completed |
| 🗑️ **Delete Task** | Remove tasks from the list with confirmation |
| 📊 **Statistics** | View total, completed, and pending task counts |
| 💾 **JSON Storage** | Persistent data storage in `tasks.json` |
| 🛡️ **Error Handling** | Graceful handling of invalid inputs and file errors |

---

## 📁 Project Structure

```
todo_list_project/
│
├── main.py              # Main application code
├── tasks.json           # Task data storage (auto-created)
── README.md            # This documentation file
── screenshots/         # Folder for sample outputs
    └── sample_output.png
```

---

## 🚀 How to Run

### Prerequisites

- Python 3.6 or higher
- No external packages required (uses only standard library)

### Installation & Execution

1. **Clone or download the project:**
   ```bash
   git clone https://github.com/kvsajith34/Codveda-Technologies.git
   cd I-Task1-TO_DO_List
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Interact with the menu:**
   - Enter `1` to add a new task
   - Enter `2` to view all tasks
   - Enter `3` to mark a task as completed
   - Enter `4` to delete a task
   - Enter `5` to exit the application

---

## 📖 Usage Examples

### Adding a Task
```
Enter your choice (1-5): 1
Enter task description: Complete Python assignment
✅ Success: Task 'Complete Python assignment' added successfully!
```

### Viewing Tasks
```
Enter your choice (1-5): 2

 Statistics: Total: 3 | Completed: 1 | Pending: 2
--------------------------------------------------
1. [✓] Complete Python assignment
   Status: Completed | Created: 2026-01-15 10:30:00
2. [○] Review code changes
   Status: Pending | Created: 2026-01-15 11:00:00
3. [○] Submit internship report
   Status: Pending | Created: 2026-01-15 11:15:00
```

### Marking Task as Completed
```
Enter your choice (1-5): 3
Enter task number to mark as completed: 2
✅ Success: Task 'Review code changes' marked as completed!
```

### Deleting a Task
```
Enter your choice (1-5): 4
Enter task number to delete: 3
Are you sure you want to delete 'Submit internship report'? (y/n): y
✅ Success: Task 'Submit internship report' deleted successfully!
```

---

## 🛡️ Error Handling

The application handles the following error scenarios:

| Error Type | Handling |
|------------|----------|
| Invalid menu choice | Displays error message, prompts again |
| Invalid task number | Shows valid range, prevents crash |
| Empty task input | Validates and rejects empty descriptions |
| Missing JSON file | Auto-creates new file automatically |
| Corrupted JSON file | Warns user and starts fresh |
| Keyboard interrupt | Graceful exit with goodbye message |

---

##  Technical Details

### Functions Used

| Function | Purpose |
|----------|---------|
| `load_tasks()` | Load tasks from JSON file |
| `save_tasks()` | Save tasks to JSON file |
| `add_task()` | Add new task to list |
| `view_tasks()` | Display all tasks with statistics |
| `mark_task_completed()` | Mark specific task as done |
| `delete_task()` | Remove task from list |
| `display_menu()` | Show main menu options |
| `main()` | Application entry point |

### Data Structure

Each task is stored as a dictionary:
```json
{
    "id": 1,
    "title": "Task description",
    "completed": false,
    "created_at": "2026-01-15 10:30:00"
}
```

---

## 📝 Code Quality

- ✅ Modular programming with separate functions
- ✅ Clear variable and function names
- ✅ Comprehensive comments
- ✅ Proper exception handling
- ✅ Follows Python best practices (PEP 8)
- ✅ Beginner-friendly logic flow

---

## 🎓 Learning Outcomes

This project demonstrates:

1. **File Handling** - Reading and writing JSON files
2. **Error Handling** - Try-except blocks for robust code
3. **Data Persistence** - Storing data between sessions
4. **User Input Validation** - Preventing invalid operations
5. **Modular Design** - Separating concerns into functions
6. **Menu-Driven Interface** - Interactive CLI applications

---

## 👨‍💻 Author

--KVS Ajith
  
Built using Python

