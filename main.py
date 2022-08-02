from DeviceData import create_app

app= create_app()

# main script to run the server

if __name__ == '__main__':
    app.run(debug=True)