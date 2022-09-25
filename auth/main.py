from authServer import AuthServer


def main():
    auth_server = AuthServer()
    auth_server.start_server()


if __name__ == '__main__':
    main()