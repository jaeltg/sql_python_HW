from db.run_sql import run_sql
from models.task import Task
from models.user import User
import repositories.user_repository as user_repository

#  Save
def save(task):
    sql = """
        INSERT INTO tasks 
        (description, user_id, duration, completed)
        VALUES ( %s, %s, %s, %s ) RETURNING *
    """
    # RETURNING * means after you save everything get me back everything of the new created item.
    values =[task.description, task.user.id, task.duration, task.completed]
    # results is a list of one dict type item.
    results = run_sql(sql, values) 
    # To access the id you have to acces the item in the list and then the value of the key id.
    id = results[0]["id"] 
    # you assign the id property of the task object to be the id returned by the database.
    task.id = id 

# get all
def select_all():
    tasks = []
    sql = "SELECT * FROM tasks"
    # results is a list of dict type items (all items in your database).
    results = run_sql(sql)

# For dict type item in results list, get all values stored in keys and create a task object
    for row in results: 
        user = user_repository.select(row["user_id"])
        task = Task(row["description"], 
                    user, 
                    row["duration"], 
                    row["completed"], 
                    row["id"])
 # Append that object to the tasks list created above and return it, then this becomes a list of task items and you can access its properties directly.                   
        tasks.append(task)
    return tasks             

# get one
def select(id):
    task = None
    # select a task given a specific id that we give when we run the function
    sql = "SELECT * FROM tasks WHERE id = %s"
    values = [id]
    # if the id is found, results is a list of one dictionary item that corresponds to the selected id. Then we extract that item and call it result.
    result = run_sql(sql, values)[0]
# if item is found, we convert it into a Task object rather than a dict type item. and then return the task item.
    if result is not None:
        user = user_repository.select(result["user_id"])
        task = Task(result['description'], 
                    user,
                    result["duration"],
                    result["completed"],
                    result["id"])
    return task    
    
# Delete all
def delete_all():
    sql = "DELETE FROM tasks"
    run_sql(sql)

# Delete one
def delete_one(id):
    sql = "DELETE FROM tasks WHERE id = %s"
    values = [id]
    run_sql(sql, values)

# Update
# Make changes through python the use update function to update those changes in the database.
def update(task):
    sql = """
        UPDATE tasks
        SET (description, user_id, duration, completed) = (%s, %s, %s, %s)
        WHERE id = %s
    """
    values = [task.description, task.user.id, task.duration, task.completed, task.id]
    run_sql(sql, values)
    
    
