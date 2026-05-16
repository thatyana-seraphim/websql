import uvicorn

if __name__ == "__main__":
    # Aponta para a variável 'app' dentro do arquivo 'app/main.py'
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)