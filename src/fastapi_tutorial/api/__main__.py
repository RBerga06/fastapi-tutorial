import uvicorn

uvicorn.run(  # pyright: ignore[reportUnknownMemberType]
    "fastapi_tutorial.api.main:app", reload=True,
)
