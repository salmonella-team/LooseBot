import datetime
import locale
import hashlib

locale.setlocale(locale.LC_TIME, 'ja_JP')

dt = datetime.datetime.today()
print(dt.strftime('%Y/%m/%d(%a) %H:%M:%S'))
print(locale.getlocale(locale.LC_TIME))

id = "987398173982173981739"
id += dt.strftime('%Y/%m/%d(%a)')
print(id)

hs = hashlib.sha256(id.encode()).hexdigest()
print(hs.upper()[10:17])