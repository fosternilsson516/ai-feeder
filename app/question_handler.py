from app.db import connect_to_database
import psycopg2

class Questions():
        def get_next_question(self, user_id):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT q.question_text, a.question_id AS min_question_id
                        FROM answers a
                        INNER JOIN owners o ON a.owner_id = o.owner_id
                        INNER JOIN users u ON o.user_id = u.user_id
                        INNER JOIN questions q ON a.question_id = q.question_id
                        WHERE u.user_id = %s AND a.answer IS NULL
                        ORDER BY a.question_id ASC
                        LIMIT 1;
                    """, (user_id,))
                    result = cursor.fetchone()
                    return result 
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close()  

        def get_answers(self, user_id):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT a.answer, q.question_text, a.question_id
                        FROM answers a
                        INNER JOIN owners o ON a.owner_id = o.owner_id
                        INNER JOIN users u ON o.user_id = u.user_id
                        INNER JOIN questions q ON a.question_id = q.question_id
                        WHERE u.user_id = %s AND a.answer IS NOT NULL
                        ORDER BY a.question_id ASC
                    """, (user_id,))
                    result = cursor.fetchall()
                    if result:
                        return result
                    else:
                        return None  
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close()                                    

        def save_text_answer(self, user_id, question_id, answer_text):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE answers
                        SET answer = %s
                        WHERE owner_id = (
                            SELECT owner_id
                            FROM owners
                            WHERE user_id = %s
                        ) AND question_id = %s
                    """, (answer_text, user_id, question_id))
                    conn.commit()
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close()    

        def save_first_question(self, user_id, service_text):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE owners
                        SET service_text = %s
                        WHERE owner_id = (
                            SELECT owner_id
                            FROM owners
                            WHERE user_id = %s
                        )
                    """, (service_text, user_id))
                    conn.commit()
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close()   

        def save_second_question(self, user_id, special_instructions):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE owners
                        SET special_instructions = %s
                        WHERE owner_id = (
                            SELECT owner_id
                            FROM owners
                            WHERE user_id = %s
                        )
                    """, (special_instructions, user_id))
                    conn.commit()
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close()  

        def save_third_question(self, user_id, business_address):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE owners
                        SET business_address = %s
                        WHERE owner_id = (
                            SELECT owner_id
                            FROM owners
                            WHERE user_id = %s
                        )
                    """, (business_address, user_id))
                    conn.commit()
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close()  

        def save_fourth_question(self, user_id, subdomain):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE owners
                        SET subdomain = %s
                        WHERE owner_id = (
                            SELECT owner_id
                            FROM owners
                            WHERE user_id = %s
                        )
                    """, (subdomain, user_id))
                    conn.commit()
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close()  
                                                                            