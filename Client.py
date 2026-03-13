import socket
import struct
import json
import os

SERVER = ("192.168.137.1", 5000)

def recv_all(sock, size):
    data = b''
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data

def send_file(sock, filepath, target_format):
    filename = os.path.basename(filepath)

    with open(filepath, "rb") as f:
        filedata = f.read()

    header = {
        "filename": filename,
        "format": target_format
    }

    header_bytes = json.dumps(header).encode()

    sock.sendall(struct.pack("!I", len(header_bytes)))
    sock.sendall(header_bytes)

    sock.sendall(struct.pack("!Q", len(filedata)))
    sock.sendall(filedata)

def recv_file(sock):
    header_len = struct.unpack("!I", recv_all(sock, 4))[0]
    header = json.loads(recv_all(sock, header_len).decode())

    size = struct.unpack("!Q", recv_all(sock, 8))[0]
    data = recv_all(sock, size)

    return header["filename"], data

def main():
    path = input("Enter image path: ")
    fmt = input("Convert to (png/jpg): ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(SERVER)

        send_file(s, path, fmt)

        name, data = recv_file(s)

    os.makedirs("converted", exist_ok=True)

    with open("converted/" + name, "wb") as f:
        f.write(data)

    print("Saved:", name)

if __name__ == "__main__":
    main()
