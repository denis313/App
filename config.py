import environs


def db_config(path: str | None = None) -> str:
    env = environs.Env()
    env.read_env(path)
    url = env('DATABASE_URL')
    return url