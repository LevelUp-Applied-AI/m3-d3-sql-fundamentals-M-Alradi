import sqlite3
from typing import List, Tuple

db_path = "drill.db"

def top_departments(db_path: str) -> List[Tuple[str, float]]:
    """
    Top 3 departments by total salary expenditure.
    """
    query = """
        SELECT d.name, SUM(e.salary) AS total_salary
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_id
        ORDER BY total_salary DESC
        LIMIT 3
    """

    with sqlite3.connect(db_path) as conn:
        return conn.execute(query).fetchall()


def employees_with_projects(db_path: str) -> List[Tuple[str, str]]:
    """
    Employees assigned to at least one project.
    """
    query = """
        SELECT e.name, p.name
        FROM employees e
        INNER JOIN project_assignments pa 
            ON e.emp_id = pa.emp_id
        INNER JOIN projects p 
            ON pa.project_id = p.project_id
        ORDER BY e.name, p.name
    """

    with sqlite3.connect(db_path) as conn:
        return conn.execute(query).fetchall()


def salary_rank_by_department(db_path: str) -> List[Tuple[str, str, float, int]]:
    """
    Salary rank within each department using RANK window function.
    """
    query = """
        SELECT e.name, d.name, e.salary,
            RANK() OVER(
                PARTITION BY e.dept_id
                ORDER BY e.salary DESC
            ) AS salary_rank
        FROM employees e
        JOIN departments d 
            ON e.dept_id = d.dept_id
        ORDER BY d.name, salary_rank
    """

    with sqlite3.connect(db_path) as conn:
        return conn.execute(query).fetchall()
    
if __name__ == "__main__":
    print("Top Departments by Total Salary Expenditure:\n")
    print(top_departments(db_path))
    print("\nEmployees Assigned to Projects:\n")    
    print(employees_with_projects(db_path))
    print("\nSalary Rank by Department:\n")
    print(salary_rank_by_department(db_path))