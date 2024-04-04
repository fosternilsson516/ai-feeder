from app.db import connect_to_database
import psycopg2

class URLSetup():
    def get_response(self, user_id):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT answer
                    FROM owners
                    WHERE user_id = %s
                """, (user_id,))
                result = cursor.fetchone()[0]
                if result:
                    return result
                else:
                    return None  
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()

    def save_response(self, user_id, text):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE owners
                    SET answer = %s
                    WHERE user_id = %s
                """, (text, user_id,))
                conn.commit()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
                return {"error": "An error occurred while updating the subdomain."}
            finally:
                conn.close()                                                        

    def save_subdomain(self, user_id, subdomain):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                # First, check if the subdomain already exists for another owner
                cursor.execute("""
                    SELECT subdomain
                    FROM owners
                    WHERE subdomain = %s AND user_id != %s
                """, (subdomain, user_id))
                result = cursor.fetchone()
                if result:
                    # Subdomain already taken by another owner
                    return {"error": "Subdomain already taken. Please change your subdomain, or it will not be saved."}
                else:
                    # Proceed with updating the subdomain since it's not taken
                    cursor.execute("""
                        UPDATE owners
                        SET subdomain = %s
                        WHERE user_id = %s
                    """, (subdomain, user_id))
                    conn.commit()
                    return {"success": "Subdomain set."}
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
                return {"error": "An error occurred while updating the subdomain."}
            finally:
                conn.close()    

    def get_subdomain(self, user_id):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT subdomain
                    FROM owners
                    WHERE user_id = %s  
                """, (user_id,))
                subdomain = cursor.fetchone()[0]
                return subdomain
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close() 

    def get_owner_data(self, subdomain):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT answer  
                    FROM owners
                    WHERE subdomain = %s
                """, (subdomain,))
                result = cursor.fetchone()[0]
                return result
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()                                                                                                                