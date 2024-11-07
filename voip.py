import pyaudio
import socket
import threading

# تنظیمات صدا
CHUNK = 512  # تعداد نمونه‌ها در هر بلوک را کاهش دادیم
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# آدرس شبکه
HOST = '0.0.0.0'  # پذیرش از همه IP‌ها برای سمت گیرنده
PORT = 2020  # پورت برای ارسال و دریافت داده‌ها

# ایجاد شی pyaudio
p = pyaudio.PyAudio()

# تابع برای ارسال داده صوتی
def send_audio(sock, target_host, target_port, stream):
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        sock.sendto(data, (target_host, target_port))
        print(f"Data sent: {len(data)} bytes")  # بررسی ارسال داده

# تابع برای دریافت داده صوتی و پخش آن
def receive_audio(sock, stream):
    while True:
        data, addr = sock.recvfrom(CHUNK * 2)  # ممکن است دو برابر CHUNK باشد برای کاهش خش
        print(f"Data received: {len(data)} bytes")  # بررسی دریافت داده
        stream.write(data)

# ایجاد سوکت
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

# تنظیم بافر شبکه برای کاهش خش
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)

# شروع ضبط صدا
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

# آدرس IP سیستم مقصد
target_host = '192.168.1.3'  # آدرس IP سیستم دوم (فرستنده)
target_port = 12346  # پورت برای ارسال داده به سیستم دوم

# ایجاد و شروع Thread‌ها برای ارسال و دریافت صدا
send_thread = threading.Thread(target=send_audio, args=(sock, target_host, target_port, stream))
receive_thread = threading.Thread(target=receive_audio, args=(sock, stream))

send_thread.start()
receive_thread.start()


send_thread.join()
receive_thread.join()
