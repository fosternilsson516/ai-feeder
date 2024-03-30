from app.db import connect_to_database
import psycopg2
import psycopg2.extras

class Availability:
    def get_avail(self, user_id):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT availability   
                    FROM owners
                    WHERE owner_id = (
                        SELECT owner_id
                        FROM owners
                        WHERE user_id = %s
                    )
                """, (user_id,))
                availability_data = cursor.fetchone()[0]
                if availability_data:
                    # If availability_id exists, availability data exists for the user
                    return availability_data
                else:
                    # If availability_id does not exist, availability data does not exist for the user
                    return None
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()

    def update_avail(self, user_id, availability_json):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE owners
                    SET availability = %s
                    WHERE owner_id = (
                        SELECT owner_id
                        FROM owners
                        WHERE user_id = %s
                    )
                """, (availability_json, user_id))
                conn.commit()
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
                    SELECT owner_id, availability, calendar_ids, service_text, special_instructions, business_address   
                    FROM owners
                    WHERE subdomain = %s
                """, (subdomain,))
                owner_data = cursor.fetchone()
                return owner_data
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()

    def save_user_credentials(self, user_id, access_token, refresh_token, token_uri, client_id, client_secret, scopes):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE owners
                    SET token = %s, refresh_token = %s, token_uri = %s, client_id = %s, client_secret = %s, scopes = %s
                    WHERE owner_id = (
                        SELECT owner_id
                        FROM owners
                        WHERE user_id = %s
                    )
                """, (access_token, refresh_token, token_uri, client_id, client_secret, scopes, user_id))
                conn.commit()
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()  

    def get_user_credentials(self, user_id):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute("""
                    SELECT token, refresh_token, token_uri, client_id, client_secret, scopes
                    FROM owners
                    WHERE owner_id = (
                        SELECT owner_id
                        FROM owners
                        WHERE user_id = %s
                    )
                """, (user_id,))
                credential_record = cursor.fetchone()
                if credential_record:
                    # Convert DictRow to a regular dict
                    credentials_dict = dict(credential_record)
                    credentials_dict['scopes'] = credentials_dict['scopes'].split(' ')
                    return credentials_dict
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()  

    def save_cal_id(self, user_id, calendar_ids):
        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE owners
                    SET calendar_ids = %s
                    WHERE owner_id = (
                        SELECT owner_id
                        FROM owners
                        WHERE user_id = %s
                    )
                """, (calendar_ids, user_id))
                conn.commit()
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
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
                    WHERE owner_id = (
                        SELECT owner_id
                        FROM owners
                        WHERE user_id = %s
                    )
                """, (user_id,))
                subdomain = cursor.fetchone()[0]
                return subdomain
                cursor.close()
            except psycopg2.Error as e:
                print("Error executing SQL query:", e)
            finally:
                conn.close()                                                     
