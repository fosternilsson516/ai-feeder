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

        def post_business_data(self, user_id, logo_url, bio, style_id):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT business_id FROM owners WHERE user_id = %s", (user_id,))
                    business_id = cursor.fetchone()

                    cursor.execute("UPDATE businesses SET logo_path = %s, bio = %s, style_id = %s WHERE business_id = %s", (logo_url, bio, style_id, business_id))
                    conn.commit()
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close()  

        def get_business_data(self, user_id):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT business_id FROM owners WHERE user_id = %s", (user_id,))
                    business_id = cursor.fetchone()

                    cursor.execute("SELECT * FROM businesses WHERE business_id = %s", (business_id))
                    result = cursor.fetchone()
                    return result
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close()    

        def update_business_data(self, user_id, logo_url, bio, style_id):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT business_id FROM owners WHERE user_id = %s", (user_id,))
                    business_id = cursor.fetchone()

                    cursor.execute("UPDATE businesses SET bio = %s, style_id = %s WHERE business_id = %s", (bio, style_id, business_id))
                    conn.commit()
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close() 

        def get_subdomain_data(self, subdomain):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM businesses WHERE subdomain_name = %s", (subdomain,))
                    result = cursor.fetchone()
                    return result
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close()

        def get_business_employee_data(self, business_id):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    # Joining tables to fetch required data
                    query = """
                        SELECT e.*, u.f_name, u.l_name, s.service_name
                        FROM employees e
                        JOIN users u ON e.user_id = u.user_id
                        LEFT JOIN services s ON e.employee_id = s.employee_id
                        WHERE e.owner_id = (
                            SELECT owner_id FROM owners WHERE business_id = %s
                        )
                    """
                    cursor.execute(query, (business_id,))
                    result = cursor.fetchall()

                    # Extracting data from the result
                    employee_user_id = []
                    employee_subdirectory = []
                    employee_bio = []
                    employee_headshot = []
                    emp_f_name = []
                    emp_l_name = []
                    service_names = []

                    for row in result:
                        employee_user_id.append(row[1])
                        employee_subdirectory.append(row[3])
                        employee_bio.append(row[4])
                        employee_headshot.append(row[5])
                        emp_f_name.append(row[6])
                        emp_l_name.append(row[7])
                        service_names.append(row[8])
                    return (employee_user_id, employee_subdirectory, employee_bio, employee_headshot, emp_f_name, emp_l_name, service_names)
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close()  

        def get_styling(self, business_style_id):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT style_setting FROM styles WHERE style_id = %s", (business_style_id,))
                    style_setting = cursor.fetchone()
                    return style_setting
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close()  

        def post_employee_bio(self, user_id, img_url, self_bio):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE employees SET headshot = %s, employee_bio = %s WHERE user_id = %s", (img_url, self_bio, user_id))
                    conn.commit()
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close() 

        def update_employee_bio(self, user_id, img_url, self_bio):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE employees SET employee_bio = %s WHERE user_id = %s", (self_bio, user_id))
                    conn.commit()
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close() 

        def get_employee_bio(self, user_id):
            conn = connect_to_database()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT employee_bio FROM employees WHERE user_id = %s", (user_id,))
                    result = cursor.fetchone()[0]
                    return result
                    cursor.close()
                except psycopg2.Error as e:
                    print("Error executing SQL query:", e)
                finally:
                    conn.close()                                                                                                 