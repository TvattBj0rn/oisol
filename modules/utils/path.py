import platform

def generate_path(server_id: int, file: str) -> str:
    if platform.node() == 'fedora':
        return f'./oisol/{server_id}/{file}'
    else:
        return f'/oisol/{server_id}/{file}'
