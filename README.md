# Six_Eyes
Six_eyes is an customizable ip-logger which logs the users details when visiting the link. It is written in Python and PHP and uses MySQL to store the details.

## Disclaimer
In the spirit of openness and collaboration, this project is released without a specific license. Users are encouraged to freely modify and adapt the contents of this project for their individual needs. The absence of a license implies an open invitation for users to exercise creativity and customization while respecting legal and ethical boundaries.

Please notify any issues you come across!

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Note](#note)
- [License](#license)

## Installation

**Step-1:** Update apt
```bash
sudo apt update
```

**Step-2:** Install requirements.
```bash
pip3 install -r requirements.txt
```

**Step-3:** Open Terminal and type the following to give privilege to user "root" in MySQL.
```bash
sudo systemctl start mysql
```
```
sudo mysql -u root
```
```sql
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY '' WITH GRANT OPTION;
```
```sql
FLUSH PRIVILEGES;
```
```
EXIT;
```

**Step-4:** Login to [Ngrok](https://ngrok.com/). Grab your AUTH_TOKEN from the dashboard page and add it in line 271 in [grabber.py](grabber.py).

(Ngrok Dashboard -> Your Authtoken -> AUTHTOKEN)

**Step-5:** Login to [bitly](https://bitly.com/). Get the API and add it in line 33 in [grabber.py](grabber.py).

(Bitly Dashboard -> Settings -> developer Settings -> API -> Enter Password -> Generate Token)

## Usage

Run the program
```bash
python3 grabber.py
```

## Note

- The [grabber.py](grabber.py) uses the default username and password for MySQL for database manipulation.
- It asks for port number when running. Provide a valid port. If not it uses 4444 as the default port.
- You can also byepass the Ngrok warning page if you want.

## License

This project is free of license which you can chech [here](LICENSE).
