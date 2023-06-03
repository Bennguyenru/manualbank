import requests
import urllib.parse
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio
import time

bot_token = '6007954058:AAHxle2miSH1RH2tyI7iHEqX1NT7pVHfFGA'
chat_id = '-981776977'

# Create a bot instance
bot = Bot(token=bot_token)

# Thông tin đăng nhập
username = "mango@borderlands777.com"
password = "March2023!"

# URL đăng nhập và URL mà bạn muốn trích xuất dữ liệu
login_url = "https://bitter-breeze-1509.borderlands777.com/login"
url1 = "https://bitter-breeze-1509.borderlands777.com/deposits/pending"
url2 = "https://bitter-breeze-1509.borderlands777.com/withdrawals/pending"

# Variables to hold the previous data
prev_data1 = ''
prev_data2 = ''

while True:  # This will create an infinite loop
    # Tạo phiên (session)
    session = requests.Session()
    # Get auth
    response = session.get(login_url)
    soupAuth = BeautifulSoup(response.text, 'html.parser')
    auth = urllib.parse.quote(soupAuth.select_one('meta[name="csrf-token"]').get('content'))
    # Gửi yêu cầu POST để đăng nhập
    login_data = "utf8=%E2%9C%93&authenticity_token="+auth+"&user%5Bemail%5D=mango%40borderlands777.com&user%5Bpassword%5D=March2023%21&commit=Giri%C5%9F+Yap"
    response = session.post(login_url, data=login_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    # Kiểm tra xem có đăng nhập thành công không
    if "Withdrawals" in response.text:
        print("Đăng nhập thành công!")

        # Gửi yêu cầu GET đến URL mà bạn muốn trích xuất dữ liệu
        response1 = session.get(url1)
        response2 = session.get(url2)

        # Sử dụng Beautiful Soup để phân tích HTML
        soup1 = BeautifulSoup(response1.text, 'html.parser')
        soup2 = BeautifulSoup(response2.text, 'html.parser')

        # Lấy dữ liệu mà bạn muốn từ HTML
        data1 = '\n'.join([' '.join(cell.stripped_strings) for cell in soup1.select('table td')])
        data2 = '\n'.join([' '.join(cell.stripped_strings) for cell in soup2.select('table td')])
        
        # Gửi dữ liệu đến Telegram
        # Run the coroutines
        if len(data1) > 0 and data1 != prev_data1:
            asyncio.get_event_loop().run_until_complete(bot.send_message(chat_id, text=data1))
            prev_data1 = data1
        if len(data2) > 0 and data2 != prev_data2:
            asyncio.get_event_loop().run_until_complete(bot.send_message(chat_id, text=data2))
            prev_data2 = data2

    # Wait for 60 seconds (1 minute)
    time.sleep(60)
