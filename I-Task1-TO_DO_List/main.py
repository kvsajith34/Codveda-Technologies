#!/usr/bin/env python3
"""
To-Do List Application
Internship Project - Codveda Technologies
Level 2: Intermediate Task

A command-line application to manage daily tasks with JSON storage.
"""

import json
import os
from datetime import datetime

# Constants
TASKS_FILE = "tasks.json"


def load_tasks():
    """
    Load tasks from JSON file.
    Returns an empty list if file doesn't exist or is corrupted.
    """
    if not os.path.exists(TASKS_FILE):
        return []
    
    try:
        with open(TASKS_FILE, 'r') as file:
            tasks = json.load(file)
            return tasks if isinstance(tasks, list) else []
    except (json.JSONDecodeError, IOError) as e:
        print(f"\n️  Warning: Could not load tasks file. Starting fresh.")
        return []


def save_tasks(tasks):
    """
    Save tasks to JSON file.
    Handles file writing errors gracefully.
    """
    try:
        with open(TASKS_FILE, 'w') as file:
            json.dump(tasks, file, indent=2)
        return True
    except IOError as e:
        print(f"\n❌ Error: Could not save tasks. {e}")
        return False


def add_task(tasks):
    """
    Add a new task to the list.
    Validates input and assigns unique ID.
    """
    print("\n" + "=" * 50)
    print("📝 ADD NEW TASK")
    print("=" * 50)
    
    task_title = input("Enter task description: ").strip()
    
    # Validate empty input
    if not task_title:
        print("\n❌ Error: Task description cannot be empty!")
        return
    
    # Create task object
    new_task = {
        "id": len(tasks) + 1,
        "title": task_title,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    tasks.append(new_task)
    
    if save_tasks(tasks):
        print(f"\n✅ Success: Task '{task_title}' added successfully!")
    else:
        print("\n❌ Error: Failed to save task.")


def view_tasks(tasks):
    """
    Display all tasks with their status.
    Shows statistics (total, completed, pending).
    """
    print("\n" + "=" * 50)
    print("📋 YOUR TASKS")
    print("=" * 50)
    
    if not tasks:
        print("\n📭 No tasks found. Add a new task to get started!")
        return
    
    # Display statistics
    total = len(tasks)
    completed = sum(1 for task in tasks if task["completed"])
    pending = total - completed
    
    print(f"\n Statistics: Total: {total} | Completed: {completed} | Pending: {pending}")
    print("-" * 50)
    
    # Display each task
    for index, task in enumerate(tasks, 1):
        status = "✓" if task["completed"] else "○"
        status_text = "Completed" if task["completed"] else "Pending"
        print(f"{index}. [{status}] {task['title']}")
        print(f"   Status: {status_text} | Created: {task['created_at']}")
    
    print("-" * 50)


def mark_task_completed(tasks):
    """
    Mark a specific task as completed.
    Validates task number input.
    """
    print("\n" + "=" * 50)
    print("✅ MARK TASK AS COMPLETED")
    print("=" * 50)
    
    if not tasks:
        print("\n No tasks available. Add a task first!")
        return
    
    # Show tasks first
    view_tasks(tasks)
    
    try:
        task_num = int(input("\nEnter task number to mark as completed: "))
        
        # Validate task number
        if task_num < 1 or task_num > len(tasks):
            print(f"\n❌ Error: Invalid task number. Please enter 1-{len(tasks)}.")
            return
        
        # Check if already completed
        if tasks[task_num - 1]["completed"]:
            print("\n⚠️  This task is already marked as completed!")
            return
        
        # Mark as completed
        tasks[task_num - 1]["completed"] = True
        tasks[task_num - 1]["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if save_tasks(tasks):
            print(f"\n✅ Success: Task '{tasks[task_num - 1]['title']}' marked as completed!")
        else:
            print("\n❌ Error: Failed to save changes.")
            
    except ValueError:
        print("\n❌ Error: Please enter a valid number.")


def delete_task(tasks):
    """
    Delete a specific task from the list.
    Validates task number and confirms deletion.
    """
    print("\n" + "=" * 50)
    print("🗑️  DELETE TASK")
    print("=" * 50)
    
    if not tasks:
        print("\n📭 No tasks available to delete!")
        return
    
    # Show tasks first
    view_tasks(tasks)
    
    try:
        task_num = int(input("\nEnter task number to delete: "))
        
        # Validate task number
        if task_num < 1 or task_num > len(tasks):
            print(f"\n❌ Error: Invalid task number. Please enter 1-{len(tasks)}.")
            return
        
        # Confirm deletion
        task_title = tasks[task_num - 1]["title"]
        confirm = input(f"Are you sure you want to delete '{task_title}'? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("\n⚠️  Deletion cancelled.")
            return
        
        # Delete the task
        deleted_task = tasks.pop(task_num - 1)
        
        # Reassign IDs to maintain sequential numbering
        for index, task in enumerate(tasks, 1):
            task["id"] = index
        
        if save_tasks(tasks):
            print(f"\n✅ Success: Task '{task_title}' deleted successfully!")
        else:
            print("\n❌ Error: Failed to save changes.")
            
    except ValueError:
        print("\n❌ Error: Please enter a valid number.")


def display_menu():
    """
    Display the main menu options.
    """
    print("\n" + "=" * 50)
    print(" TODO LIST APPLICATION")
    print("   Codveda Technologies - Internship Project")
    print("=" * 50)
    print("\n1. ➕ Add Task")
    print("2. 📋 View Tasks")
    print("3. ✅ Mark Task as Completed")
    print("4. 🗑️  Delete Task")
    print("5. 🚪 Exit")
    print("=" * 50)


def main():
    """
    Main function - Application entry point.
    Runs the menu-driven interface loop.
    """
    print("\n" + "🎉" * 25)
    print("   Welcome to To-Do List Application!")
    print("" * 25)
    
    # Load existing tasks
    tasks = load_tasks()
    
    if tasks:
        print(f"\n📂 Loaded {len(tasks)} existing task(s) from storage.")
    
    # Main application loop
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                add_task(tasks)
            elif choice == "2":
                view_tasks(tasks)
            elif choice == "3":
                mark_task_completed(tasks)
            elif choice == "4":
                delete_task(tasks)
            elif choice == "5":
                print("\n" + "=" * 50)
                print("👋 Thank you for using To-Do List Application!")
                print("   See you next time!")
                print("=" * 50 + "\n")
                break
            else:
                print("\n❌ Error: Invalid choice. Please enter a number between 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Application interrupted by user.")
            print("👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n Unexpected error: {e}")
            print("⚠️  Please try again.")


# Run the application
if __name__ == "__main__":
    main()
