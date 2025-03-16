from datetime import datetime
import pytz

def current_time():
  tashkent_time = datetime.now(pytz.timezone('Asia/Tashkent'))
  return str(tashkent_time.strftime('%m.%d.%Y | %H:%M:%S'))