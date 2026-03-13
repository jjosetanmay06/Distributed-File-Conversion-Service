import socket
import struct
import json
from PIL import Image
import io

PORT = 6001

def recv_all(sock, size):
    data = b''
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data

def recv_file(sock):
    header_len = struct.unpack("!I", recv_all(sock, 4))[0]
    header = json.loads(recv_all(sock, header_len).decode())

    size = struct.unpack("!Q", recv_all(sock, 8))[0]
    data = recv_all(sock, size)

    return header, data

def send_file(sock, header, data):
    header_bytes = json.dumps(header).encode()

    sock.sendall(struct.pack("!I", len(header_bytes)))
    sock.sendall(header_bytes)

    sock.sendall(struct.pack("!Q", len(data)))
    sock.sendall(data)

def convert_image(data, fmt):
    img = Image.open(io.BytesIO(data))

    if fmt in ["jpg", "jpeg"]:
        img = img.convert("RGB")
        fmt = "JPEG"
    else:
        fmt = "PNG"

    out = io.BytesIO()
    img.save(out, format=fmt)

    return out.getvalue()

def main():
    s = socket.socket()
    s.bind(("0.0.0.0", PORT))
    s.listen()

    print("Worker running on", PORT)

    while True:
        conn, _ = s.accept()

        try:
            header, data = recv_file(conn)

            new_data = convert_image(data, header["format"])

            header["filename"] = header["filename"].split(".")[0] + "." + header["format"]

            send_file(conn, header, new_data)

        except Exception as e:
            print("Worker error:", e)

        conn.close()

if __name__ == "__main__":
    main()
