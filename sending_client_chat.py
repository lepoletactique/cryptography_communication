SERVER = "http://mxg.together.org.il/hub"
KEYS = {'981': "Stav", "415": "Gianni"}
MY_KEY = '415'


def send_message(plain_text):
    to_whom = plain_text[:3]
    encrypted_text = encrypt(plain_text[4:])
    encrypted_message = ''+ MY_KEY + ''.join(to_whom) + encrypted_text
    Hub.send(encrypted_message)
    print("Message sent...")


def receive_messages(frame):
    if ''.join(frame[:3]) == MY_KEY:
        if ''.join(frame[3:6])in KEYS.keys:
            decrypted_message = decrypt(''.join(frame[6:]))
            print(decrypted_message)


def decrypt(encrypted_message):
    return "Heyyyy!!!"


def encrypt(message):
    return "Message encrypted...."


def keep_chat_open():
    while True:
        message = input("Insert a message to send: \n")
        send_message(message)


keep_chat_open()
