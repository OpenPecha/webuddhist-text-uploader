from fastapi import FastAPI


app = FastAPI(title="Webuddhist Text Uploader", version="0.1.0")


@app.get("/")
def read_root() -> dict[str, str]:
	return {"status": "ok", "message": "Webuddhist Text Uploader API"}


@app.get("/health")
def health_check() -> dict[str, str]:
	return {"status": "healthy"}


