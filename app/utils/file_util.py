import os


def current_dir_path():
    return os.getcwd()


def removePathFiles(files):
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print(f"Error: {f}: {e.strerror}")


def dir_outer(path):
    dir_path_splits = path.split("/")[:-1]
    return "/".join(dir_path_splits)


def create_directory_path(path):
    """
    주어진 경로의 모든 디렉토리를 생성합니다.

    :param path: 생성할 디렉토리 경로
    :return: 경로 생성 성공 시 True, 실패 시 False
    """
    try:
        os.makedirs(path, exist_ok=True)
        print(f"경로가 생성되었습니다: {path}")
        return True
    except PermissionError:
        print(f"권한 오류: {path} 경로를 생성할 수 있는 권한이 없습니다.")
        return False
    except OSError as e:
        print(f"경로 생성 중 오류 발생: {e}")
        return False


def rename(src, dis):
    if not os.path.exists(dis):
        os.rename(src, dis)
        return dis
    else:
        return 0
