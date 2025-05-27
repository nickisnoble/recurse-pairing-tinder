from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from pairing-tinder!"}



def main():
    print("Hello from pairing-tinder!")


if __name__ == "__main__":
    main()
