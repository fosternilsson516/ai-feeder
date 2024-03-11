from app.db import connect_to_database
import psycopg2

class Business():
        def get_subdomain(self, user_id):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT business_id FROM owners WHERE user_id = %s", (user_id,))
                    business_id = cursor.fetchone()

                    cursor = conn.cursor()
                    cursor.execute("SELECT subdomain_name FROM businesses WHERE business_id = %s", (business_id,))
                    subdomain = cursor.fetchone()[0]

                    return subdomain
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close()