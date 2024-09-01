from pytest import importorskip, fmt_output
from inline_snapshot import snapshot


def test_demo(capsys):
    importorskip("demo")
    captured = capsys.readouterr()
    assert fmt_output(captured.out) == snapshot(["1", "3", "3"])
    assert fmt_output(captured.err) == snapshot(
        [
            """\
        script:
        file='rich_script.py'
        func='hello'\
""",
            """\
        ```
        # /// script
        # dependencies = [
        #   "rich",
        # ]
        # ///
        import rich


        def hello():
            rich.print("Hello, World!")
            return 1


        def add(a, b):
            return a + b


        if __name__ == "__main__":
            import pickle
            with open('tmp.pickle', 'wb') as f:
                pickle.dump(hello( ), f)
        ```
        script:
        file='rich_script.py'
        func='add'\
""",
            """\
        ```
        # /// script
        # dependencies = [
        #   "rich",
        # ]
        # ///
        import rich


        def hello():
            rich.print("Hello, World!")
            return 1


        def add(a, b):
            return a + b


        if __name__ == "__main__":
            import pickle
            with open('tmp.pickle', 'wb') as f:
                pickle.dump(add(1, 2,  ), f)
        ```
        script:
        file='rich_script.py'
        func='add'\
""",
            """\
        ```
        # /// script
        # dependencies = [
        #   "rich",
        # ]
        # ///
        import rich


        def hello():
            rich.print("Hello, World!")
            return 1


        def add(a, b):
            return a + b


        if __name__ == "__main__":
            import pickle
            with open('tmp.pickle', 'wb') as f:
                pickle.dump(add( a=1, b=2), f)
        ```\
""",
        ]
    )
