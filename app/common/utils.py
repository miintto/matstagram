def is_test():
    """애플리케이션의 테스트 환경 여부를 판별합니다.

    Logic:
        메인 호출자가 `.../site-packages/pytest/__init__.py` 혹은 `.../bin/pytest` 인
        경우는 무조건 테스트 환경이라고 간주합니다.
    """

    import __main__
    return any("pytest" == path for path in __main__.__file__.split("/")[-2:])
