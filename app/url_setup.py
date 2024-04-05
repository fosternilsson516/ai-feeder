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

    def save_subdirectory(self, user_id, subdirectory):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                # First, check if the subdirectory already exists for another owner
                cursor.execute("""
                    SELECT subdirectory
                    FROM owners
                    WHERE subdirectory = %s AND user_id != %s
                """, (subdirectory, user_id))
                result = cursor.fetchone()
                if result:
                    # subdirectory already taken by another owner
                    return {"error": "subdirectory already taken. Please change your subdirectory, or it will not be saved."}
                else:
                    # Proceed with updating the subdirectory since it's not taken
                    cursor.execute("""
                        UPDATE owners
                        SET subdirectory = %s
                        WHERE user_id = %s
                    """, (subdirectory, user_id))
                    conn.commit()
                    return {"success": "subdirectory set."}
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
                return {"error": "An error occurred while updating the subdirectory."}
            finally:
                conn.close()    

    def get_subdirectory(self, user_id):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT subdirectory
                    FROM owners
                    WHERE user_id = %s  
                """, (user_id,))
                subdirectory = cursor.fetchone()[0]
                return subdirectory
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close() 

    def get_owner_data(self, subdirectory):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT answer  
                    FROM owners
                    WHERE subdirectory = %s
                """, (subdirectory,))
                result = cursor.fetchone()[0]
                return result
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()                                                                                                                