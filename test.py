# basic_qrcode.py
from urllib.request import urlopen
from uuid import uuid4
import segno

# qrcode = segno.make_qr(str(uuid4()))
# qrcode.save("basic_qrcode.png")
slts_qrcode = segno.make_qr("https://www.youtube.com/watch?v=hTWKbfoikeg")
nirvana_url = urlopen("https://media.giphy.com/media/LpwBqCorPvZC0/giphy.gif")
slts_qrcode.to_artistic(
    background="/home/khushal/Documents/Django/Ren24/NewLogo.png",
    target="animated_qrcode.png",
    scale=5,
)
