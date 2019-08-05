import socket

def get_server_type():
    host_name = socket.gethostname()
    server_type = 'Server-type-Not-defined-or-found'
    if host_name.startswith('maesh'):
        server_type = 'production'
        #server_type = 'test_production'
    elif host_name.startswith('Mikkel'):
        server_type = 'development'
    return server_type
