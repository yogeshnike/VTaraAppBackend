from app import create_app

server = create_app()
print('Starting server on http://localhost:5000')

if __name__ == '__main__':
    server.serve_forever()
