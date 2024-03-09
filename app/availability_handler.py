from app.db import connect_to_database
import psycopg2

class Availability:
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
                employee_id = cursor.fetchone()

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