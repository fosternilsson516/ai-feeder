from app.db import connect_to_database
import psycopg2

class Employee:
    def add_employees(self, user_id, f_name, l_name, email, phone_number, hashed_password):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (f_name, l_name, email, phone_number, password_hash) VALUES (%s, %s, %s, %s, %s)",
                               (f_name, l_name, email, phone_number, hashed_password))

                cursor.execute("SELECT owner_id FROM owners WHERE user_id = %s", (user_id,))
                owner_id = cursor.fetchone()[0]

                cursor.execute("SELECT user_id FROM users WHERE phone_number = %s", (phone_number,))
                emp_user_id = cursor.fetchone()[0]

                cursor.execute("INSERT INTO employees (owner_id, user_id, subdirectory_name) VALUES (%s, %s, %s)",
                               (owner_id, emp_user_id, f_name))
                conn.commit()
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()     

    def update_employees(self, user_id, f_name, l_name, email, phone_number, password):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT user_id FROM users WHERE phone_number = %s", (phone_number,))
                emp_user_id = cursor.fetchone()

                cursor.execute("UPDATE users SET f_name = %s, l_name = %s, email = %s, phone_number = %s, password_hash = %s WHERE user_id = %s", (f_name, l_name, email, phone_number, password, emp_user_id))
                conn.commit()
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close() 

    def get_employees(self, user_id):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT owner_id FROM owners WHERE user_id = %s", (user_id,))
                owner_id = cursor.fetchone()[0]
                cursor.execute("SELECT user_id FROM employees WHERE owner_id = %s", (owner_id,))
                employee_user_ids = cursor.fetchall()
                user_data = []
                for employee_user_id in employee_user_ids:
                    cursor.execute("SELECT * FROM users WHERE user_id = %s", (employee_user_id,))
                    employee_data = cursor.fetchone()
                    user_data.append(employee_data)
                if user_data: 
                    return True, user_data
                else:
                    return False, None
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close() 

    def delete_employees(self, phone):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT user_id FROM users WHERE phone_number = %s", (phone,))
                emp_user_id = cursor.fetchone()
                cursor.execute("SELECT employee_id FROM employees WHERE user_id = %s", (emp_user_id,))
                employee_id = cursor.fetchone()
                cursor.execute("DELETE FROM services WHERE employee_id = %s", (employee_id,))
                cursor.execute("DELETE FROM availability WHERE employee_id = %s", (employee_id,))
                cursor.execute("DELETE FROM appointments WHERE employee_id = %s", (employee_id,))
                cursor.execute("DELETE FROM users WHERE user_id = %s", (emp_user_id,))
                cursor.execute("DELETE FROM employees WHERE user_id = %s", (emp_user_id,))
                conn.commit()
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()

    def get_full_name(self, user_id):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT f_name, l_name FROM users WHERE user_id = %s", (user_id,))
                owner_name = cursor.fetchone()
                return owner_name
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()

