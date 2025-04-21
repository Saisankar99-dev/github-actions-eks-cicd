from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Flask + Jenkins CI/CD on EKS!"

if __name__ == "__main__":
    # listen on 0.0.0.0:5000 for container compatibility
    app.run(host="0.0.0.0", port=5000)
