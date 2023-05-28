# import lib
from socket import *
import sys

# Mendefinisikan host dan port yang akan digunakan
HOST = '192.168.56.1'
PORT = 80

# Membuat objek socket TCP
connectionSocket = socket(AF_INET, SOCK_STREAM) #SOCK_STREAM menandakan socketnya yang dibuat berbasis TCP

# Mengikat socket ke host dan port yang telah ditentukan
connectionSocket.bind((HOST, PORT))

# Mendengarkan koneksi masuk dari klien
connectionSocket.listen(1)

print(f"Server is running {HOST}/{PORT}")

while True:
    # Menerima koneksi dari klien
    client_socket, client_address = connectionSocket.accept()
    print(f"Connected at {client_address[0]}/{client_address[1]}")

    try:
        # Menerima dan membaca data berupa link browser dari klien
        request = client_socket.recv(1024).decode()
        # Membaca nama file request dari permintaan klien
        filename = request.split()[1]
        # Membuka file dan menyimpan kedalam variable f
        f = open(filename[1:], "r")
        # Membaca dan menyimpan file yang telah dibuka ke variable file_contents lalu selanjutnya file ditutup
        file_contents = f.read()
        f.close()
        # Membuat header agar file dapat dibaca oleh browser
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + file_contents
        # Sending isi dari file ke browser klien
        for i in range(0, len(response)):
            client_socket.send(response[i].encode())
        client_socket.send("\r\n".encode())
        client_socket.close()
    # Apabila file permintaan klien tidak ditemukan pada file sistem maka except akan di eksekusi
    except IOError:
        # Membaca file sistem berupa noResponse404.html saja tidak menggunakan request message
        f = open("noResponse404.html", "r")
        noResponse = f.read()
        f.close()
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"+ noResponse
        for i in range(0, len(response)):
            client_socket.send(response[i].encode()) 
        client_socket.send("\r\n".encode())
        client_socket.close()
    # Menutup koneksi dengan klien
    client_socket.close()

connectionSocket.close()
sys.exit()