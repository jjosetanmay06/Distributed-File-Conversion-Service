# Distributed File Conversion Service

A distributed system that converts image files using a **Client–Master–Worker architecture** built with Python sockets.
The client uploads an image, the master server distributes the job to a worker node, and the worker performs the image conversion before sending the result back to the client.

---

## Architecture

Client → Master Server → Worker Node → Master Server → Client

* **Client**

  * Sends image file and desired output format.
  * Receives the converted image.

* **Master Server**

  * Accepts client connections.
  * Forwards conversion jobs to worker nodes.
  * Returns the processed result to the client.

* **Worker**

  * Receives image data from the master.
  * Converts the image format.
  * Sends the converted file back to the master.

---

## Features

* Distributed architecture
* TCP socket communication
* Binary file transfer
* Image format conversion (PNG / JPG)
* Works across multiple machines on the same network

---

## Technologies Used

* Python 3
* Socket Programming
* JSON
* Pillow (PIL) for image processing
* Struct module for binary data handling

---

## Project Structure

```
project/
│
├── client.py
├── master_server.py
├── worker.py
├── converted/
├── .gitignore
└── README.md
```

---

## Installation

Install required dependency:

```
pip install pillow
```

---

## Running the System

### 1. Start Worker

```
python worker.py 6001
```

### 2. Start Master Server

```
python master_server.py
```

### 3. Run Client

```
python client.py
```

Enter:

```
Enter image path: path/to/image.jpg
Convert to (png/jpg): png
```

The converted file will be saved in:

```
converted/
```

---

## Example

Input:

```
Cosmic_Cliffs.jpg
```

Output:

```
converted/Cosmic_Cliffs.png
```

---

## Network Setup

For distributed execution across multiple machines:

* Ensure all devices are connected to the **same WiFi network**
* Update the `SERVER` IP address in `client.py`
* Open required firewall ports (5000 for master, 6001 for worker)

---

## Possible Improvements

* Multiple worker nodes with load balancing
* Job queue system
* Fault tolerance
* Performance benchmarking

---

## Author

Distributed Systems Project using Python Socket Programming.
