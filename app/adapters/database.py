def create_database_url(
    dialect: str,
    user: str,
    host: str,
    port: int,
    database: str,
    driver: str | None = None,
    password: str | None = None,
) -> str:
    scheme = dialect
    if driver:
        scheme += f"+{driver}"
    if password:
        password = f":{password}"
    else:
        password = ""  # nosec: B105

    return f"{scheme}://{user}{password}@{host}:{port}/{database}"
