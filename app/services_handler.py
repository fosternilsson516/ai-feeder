from app.db import connect_to_database
import psycopg2

class Services:
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