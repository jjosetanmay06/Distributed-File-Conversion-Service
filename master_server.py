import socket
import struct
import json
import threading

WORKER = ("127.0.0.1", 6001)

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

def handle_client(client, addr):
    print("Client connected:", addr)

    try:
        header, data = recv_file(client)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as w:
            w.connect(WORKER)

            send_file(w, header, data)

            new_header, new_data = recv_file(w)

        send_file(client, new_header, new_data)

    except Exception as e:
        print("Error:", e)

    client.close()

def main():
    server = socket.socket()
    server.bind(("0.0.0.0", 5000))
    server.listen()

    print("Master listening on 5000")

    while True:
        c, addr = server.accept()
        threading.Thread(target=handle_client, args=(c, addr)).start()

if __name__ == "__main__":
    main()
