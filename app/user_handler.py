from app.db import connect_to_database
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

class Users:
    def create_account(self, email, phone_number, password_hash, f_name, l_name, business_name, street_address, city, state, zip_code, subdomain_name):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (email, phone_number, password_hash, f_name, l_name) VALUES (%s, %s, %s, %s, %s)",
                               (email, phone_number, password_hash, f_name, l_name))

                # Insert into the businesses table
                cursor.execute("INSERT INTO businesses (business_name, street_address, city, state, zip_code, subdomain_name) VALUES (%s, %s, %s, %s, %s, %s)",
                                (business_name, street_address, city, state, zip_code, subdomain_name))               

                # Fetch the user_id of the newly inserted user
                cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
                user_id = cursor.fetchone()[0]

                # Fetch the user_id of the newly inserted user
                cursor.execute("SELECT business_id FROM businesses WHERE business_name = %s", (business_name,))
                business_id = cursor.fetchone()[0]

                # Insert into the owners table
                cursor.execute("INSERT INTO owners (user_id, business_id) VALUES (%s, %s)",
                                (user_id, business_id))
                conn.commit()
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()
    def email_exists(self, email):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
                count = cursor.fetchone()[0]
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()
                return count > 0
    def authenticate_user(self, email, password):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
                row = cursor.fetchone()
                if row:
                    hashed_password = row[0]

                    # Compare the hashed password with the provided password
                    if check_password_hash(hashed_password, password):
                        return True  # Authentication successful
                    else:
                        return "Incorrect password"  # Password incorrect
                else:
                    return "Email not found"  # Email incorrect
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()
        else:
            print("Failed to connect to the database")
            return "Database connection error"

    def store_user_session(self, email):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
                result = cursor.fetchone()
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close() 
        return result[0] if result else None       

    def submit_avail(self, user_id, days, start_times, stop_times):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                # Fetch the employee_id from the user_id
                cursor.execute("SELECT employee_id FROM employees WHERE user_id = %s", (user_id,))
                employee_id = cursor.fetchone()[0]

                cursor.execute("INSERT INTO availability (employee_id, days, start_times, stop_times) VALUES (%s, %s, %s, %s)",
                               (employee_id, days, start_times, stop_times))
                conn.commit()
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()

    def get_avail(self, user_id):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()

                cursor.execute("SELECT employee_id FROM employees WHERE user_id = %s", (user_id,))
                employee_id = cursor.fetchone()[0]

                cursor.execute("SELECT * FROM availability WHERE employee_id = %s", (employee_id,))
                availability_data = cursor.fetchone()
                    
                if availability_data:
                    # If availability_id exists, availability data exists for the user
                    return True, availability_data
                else:
                    # If availability_id does not exist, availability data does not exist for the user
                    return False, None
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()

    def update_avail(self, user_id, days, start_times, stop_times):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()

                cursor.execute("SELECT employee_id FROM employees WHERE user_id = %s", (user_id,))
                employee_id = cursor.fetchone()[0]

                cursor.execute("UPDATE availability SET days = %s, start_times = %s, stop_times = %s WHERE employee_id = %s", (days, start_times, stop_times, employee_id))
                conn.commit()
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()   

    def save_services(self, user_id, service_n_array, service_t_array, postgresql_prices_array):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()

                cursor.execute("SELECT employee_id FROM employees WHERE user_id = %s", (user_id,))
                employee_id = cursor.fetchone()[0]

                cursor.execute("INSERT INTO services (employee_id, service_name, price_types, prices) VALUES (%s, %s, %s, %s)",
                               (employee_id, service_n_array, service_t_array, postgresql_prices_array))
                conn.commit()
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close() 

    def update_services(self, user_id, service_n_array, service_t_array, postgresql_prices_array):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()

                cursor.execute("SELECT employee_id FROM employees WHERE user_id = %s", (user_id,))
                employee_id = cursor.fetchone()[0]

                cursor.execute("UPDATE services SET service_name = %s, price_types = %s, prices = %s WHERE employee_id = %s", (service_n_array, service_t_array, postgresql_prices_array, employee_id))
                conn.commit()
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close() 

    def get_services(self, user_id):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()

                cursor.execute("SELECT employee_id FROM employees WHERE user_id = %s", (user_id,))
                employee_id = cursor.fetchone()[0]

                cursor.execute("SELECT * FROM services WHERE employee_id = %s", (employee_id,))
                services_data = cursor.fetchone()
                    
                if services_data:
                    
                    return True, services_data
                else:
                    
                    return False, None
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close() 

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


