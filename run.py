import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    # 明示的に 8080 ポートを指定
    port = 8080
    app.run(host="0.0.0.0", port=port)
