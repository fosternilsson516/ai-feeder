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

                cursor.execute("SELECT availability_id FROM availability WHERE employee_id = %s", (employee_id,))
                availability_id = cursor.fetchone()[0]

                cursor.execute("UPDATE availability SET days = %s, start_times = %s, stop_times = %s WHERE availability_id = %s", (days, start_times, stop_times, availability_id))
                conn.commit()
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()            


