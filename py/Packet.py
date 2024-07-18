import struct
BUFFER_SIZE = 1024

class packet:
    def read_packet(socket):
        # calcs how much the data will take
        header_size = struct.calcsize('B I')
        header = socket.recv(header_size)
        if not header:
            return None

        # Unpack the header to get request call and data length
        # 'B' stands for unsigned char
        # 'I' stands for unsgined int
        request_call, data_length = struct.unpack('B I', header)

        # Read the data and error parts based on data_length and remaining buffer size
        packet = socket.recv(data_length + 1)  # Data length + 1 byte for error length
        if not packet:
            return None

        # Define the format string for struct.unpack
        format_string = f'{data_length}s B'

        # Unpack the packet
        data_bytes, error_code = struct.unpack(format_string, packet)

        # Decode the data bytes, removing any padding null bytes
        data = data_bytes.rstrip(b'\x00').decode('utf-8')

        return request_call, data, error_code


    def write_packet(socket, request_call, data, error_code):
        # transfers the data to bytes
        data_bytes = data.encode()
        # data_length is now the number of bytes of data_bytes
        data_length = len(data_bytes)

        # Define the format string for struct.pack
        # format string binary data interpreted when packing and unpacking
        format_string = f'B I {data_length}s B'

        # Pack the data into a single packet
        # saving the bytes in the order I declared in format_string
        packet = struct.pack(format_string, request_call, data_length, data_bytes, error_code)

        # Send the packet through the socket to the ip the socket is connected to
        socket.sendall(packet)