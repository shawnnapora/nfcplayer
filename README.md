# Setup

Insert the following into `/etc/udev/rules.d/nfcdev.rules`:
```
SUBSYSTEM=="usb", ACTION=="add", ATTRS{idVendor}=="072f", ATTRS{idProduct}=="2200", GROUP="wheel"
```

Then create a virtual env:
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Run the reader:
```
./reader.py
```

Write a tag (the reader must be killed):
```
python writer.py "nfcalbum:SomeArtist/SomeAlbum"
```
