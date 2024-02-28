from app.db import connect_to_database
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

class Users:
    def create_account(self, email, phone_number, password_hash):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (email, phone_number, password_hash) VALUES (%s, %s, %s)",
                               (email, phone_number, password_hash))
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
