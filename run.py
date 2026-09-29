import uvicorn
import os
import sys

def main():
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8100"))
    print(f"🚀 Iniciando LayaLog em http://{host if host != '0.0.0.0' else 'localhost'}:{port}")
    uvicorn.run("layalog.app:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    main()
