import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#from smartcard.System import readers              #когда есть считыватель можно убрать коммент этих трех библиотек
#from smartcard.util import toHexString
#from smartcard.Exceptions import NoCardException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/work_portal"

Base = declarative_base()

is_logging_out = False

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    login = Column(String)
    password = Column(String)
    uid = Column(String)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

driver = None
current_uid = None
#reader_list = readers()         #когда есть считыватель можно убрать коммент
reader_list = []                 # ← заглушка, чтобы остальной код не упал(если считыватель имеется, можно удалить)

def read_card_uid(reader_index=0):
    try:
        if len(reader_list) <= reader_index:
            return None
        connection = reader_list[reader_index].createConnection()
        connection.connect()
        data, sw1, sw2 = connection.transmit([0xFF, 0xCA, 0x00, 0x00, 0x00])
        if sw1 == 0x90 and sw2 == 0x00:
            return toHexString(data).replace(" ", "")
    except NoCardException:
        pass
    except Exception as e:
        print(f"⚠️ Ошибка считывания: {e}")
    return None

def authorize_user(uid):
    global driver, current_uid

    uid = uid.replace(" ", "").upper()

    db = SessionLocal()
    users = db.query(User).all()
    user = next((u for u in users if u.uid.replace(" ", "").upper() == uid), None)
    db.close()

    if not user:
        print("❌ UID не найден.")
        return

    print(f"🔐 Найден пользователь: {user.name}")

    options = Options()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("http://127.0.0.1:8000")
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "login-btn").click()
        time.sleep(0.5)
        driver.find_element(By.ID, "login").send_keys(user.login)
        driver.find_element(By.ID, "password").send_keys(user.password)
        driver.find_element(By.CLASS_NAME, "login-submit").click()
        current_uid = uid
        print("✅ Вход выполнен")
    except Exception as e:
        print(f"❌ Ошибка входа: {e}")
        if driver:
            driver.quit()
        driver = None
        current_uid = None

def logout_user():
    global driver, current_uid, is_logging_out
    is_logging_out = True
    print("🚪 Выход пользователя...")

    try:
        logout_btn = driver.find_element(By.CSS_SELECTOR, 'a i.ri-logout-box-line')
        logout_btn.click()
        time.sleep(2)
    except Exception:
        print("⚠️ Не удалось нажать logout.")

    if driver:
        driver.quit()
        print("✅ Браузер закрыт.")

    driver = None
    current_uid = None
    is_logging_out = False

# ✅ ЭТО — ЕДИНСТВЕННАЯ ТОЧКА ЗАПУСКА:
def start_reader_loop():
    global current_uid, driver, is_logging_out

    while True:
        print("💳 Ожидание карты...")

        if is_logging_out:
            time.sleep(0.5)
            continue

        uid_in = read_card_uid(0)
        uid_out = read_card_uid(1) if len(reader_list) > 1 else None

        uid_in = uid_in.replace(" ", "").upper() if uid_in else None
        uid_out = uid_out.replace(" ", "").upper() if uid_out else None

        # Повторный пик = выход
        if uid_in and uid_in == current_uid:
            print("🔁 Повторный пик. Выходим...")
            logout_user()
            time.sleep(2)
            continue

        if uid_out and uid_out == current_uid:
            print("📤 Выход через второй считыватель.")
            logout_user()
            time.sleep(2)
            continue

        # Вход
        if uid_in:
            if current_uid:
                print("⚠️ Уже вошли. Ждём выхода.")
            else:
                authorize_user(uid_in)
            time.sleep(2)

        time.sleep(0.5)
