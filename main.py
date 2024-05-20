from fastapi import FastAPI, HTTPException, status
import mysql.connector
import uvicorn
import os

app = FastAPI()

# Database connection configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}
'''
# Database connection configuration
db_config = {
    'host': 'hr-database.cfy80wwcwo87.us-east-2.rds.amazonaws.com',
    'user': 'adminrobert',
    'password': 'awshrdatabasepass',
    'database': 'hr_schema'
}
'''

# Connect to MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the HR API. Use this API to manage employees, departments, and more."}


# Employees Endpoints
@app.get("/employees/")
def get_employees():
    cursor.execute("SELECT * FROM Employees")
    employees = cursor.fetchall()
    return employees

@app.post("/employees/")
def create_employee(employee_data: dict):
    query = "INSERT INTO Employees (FirstName, LastName, Email, PhoneNumber, DateOfBirth, Gender, Address, HireDate, DepartmentID, PositionID, SupervisorID) VALUES (%(FirstName)s, %(LastName)s, %(Email)s, %(PhoneNumber)s, %(DateOfBirth)s, %(Gender)s, %(Address)s, %(HireDate)s, %(DepartmentID)s, %(PositionID)s, %(SupervisorID)s)"
    cursor.execute(query, employee_data)
    conn.commit()
    return {"message": "Employee created successfully"}

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    cursor.execute("SELECT * FROM Employees WHERE EmployeeID = %s", (employee_id,))
    employee = cursor.fetchone()
    if employee:
        return employee
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee_data: dict):
    query = "UPDATE Employees SET FirstName = %(FirstName)s, LastName = %(LastName)s, Email = %(Email)s, PhoneNumber = %(PhoneNumber)s, DateOfBirth = %(DateOfBirth)s, Gender = %(Gender)s, Address = %(Address)s, HireDate = %(HireDate)s, DepartmentID = %(DepartmentID)s, PositionID = %(PositionID)s, SupervisorID = %(SupervisorID)s WHERE EmployeeID = %(EmployeeID)s"
    employee_data["EmployeeID"] = employee_id
    cursor.execute(query, employee_data)
    conn.commit()
    return {"message": f"Employee with ID {employee_id} updated successfully"}

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    cursor.execute("DELETE FROM Employees WHERE EmployeeID = %s", (employee_id,))
    conn.commit()
    return {"message": f"Employee with ID {employee_id} deleted successfully"}


# Departments Endpoints
@app.get("/departments/")
def get_departments():
    cursor.execute("SELECT * FROM Departments")
    departments = cursor.fetchall()
    return departments

@app.post("/departments/")
def create_department(department_name: str):
    query = "INSERT INTO Departments (DepartmentName) VALUES (%s)"
    cursor.execute(query, (department_name,))
    conn.commit()
    return {"message": "Department created successfully"}

@app.get("/departments/{department_id}")
def get_department(department_id: int):
    cursor.execute("SELECT * FROM Departments WHERE DepartmentID = %s", (department_id,))
    department = cursor.fetchone()
    if department:
        return department
    else:
        raise HTTPException(status_code=404, detail="Department not found")

@app.put("/departments/{department_id}")
def update_department(department_id: int, department_name: str):
    query = "UPDATE Departments SET DepartmentName = %s WHERE DepartmentID = %s"
    cursor.execute(query, (department_name, department_id))
    conn.commit()
    return {"message": f"Department with ID {department_id} updated successfully"}

@app.delete("/departments/{department_id}")
def delete_department(department_id: int):
    cursor.execute("DELETE FROM Departments WHERE DepartmentID = %s", (department_id,))
    conn.commit()
    return {"message": f"Department with ID {department_id} deleted successfully"}

# For Azure, ensure to use `if __name__ == "__main__"` block
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))