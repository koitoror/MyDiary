from app import app

# Runs the application
if __name__ == '__main__':
    app.secret_key = 'nbvjlisghruvnxzdnvdlsfgvbfugfvbjsdkvbusdigkbsdjkval'
    app.config['SESSION_TYPE'] = "filesystem"
    app.run(debug=True)
