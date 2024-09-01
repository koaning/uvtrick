from pytest import importorskip
from inline_snapshot import snapshot
from textwrap import indent


def fmt_output(text: str) -> list[str]:
    if "```" in text:
        # Logged script code: indent multi-line paragraphs (code blocks)
        return [
            indent(section, prefix=" " * 8).strip("\n")
            for section in text.split("code=")
        ]
    else:
        # Actual program output
        return text.splitlines()


def test_hello(capsys):
    importorskip("examples.hello")
    captured = capsys.readouterr()
    assert fmt_output(captured.out) == snapshot(["hello()=1"])
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
        ```\
""",
        ],
    )


def test_add(capsys):
    importorskip("examples.add")
    captured = capsys.readouterr()
    assert fmt_output(captured.out) == snapshot(
        ["add(1, 2)=3", "add(a=1, b=2)=3"],
    )
    assert fmt_output(captured.err) == snapshot(
        [
            """\
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
        ],
    )


def test_rich_versions(capsys):
    importorskip("examples.rich_versions")
    captured = capsys.readouterr()
    assert fmt_output(captured.out) == snapshot(
        [
            "Now iterating through rich_versions=(10, 11, 12, 13):",
            " --> add(1, 2) = 3",
            " --> add(1, 2) = 3",
            " --> add(1, 2) = 3",
            " --> add(1, 2) = 3",
        ],
    )
    assert fmt_output(captured.err) == snapshot([])


def test_simple(capsys):
    importorskip("examples.simple.main")
    captured = capsys.readouterr()
    assert fmt_output(captured.out) == snapshot(
        ["3"],
    )
    assert fmt_output(captured.err) == snapshot(
        [
            """\
        script:
        file='some_script.py'
        func='add'\
""",
            """\
        ```
        # /// script
        # dependencies = [
        # ]
        # ///


        def add(a: int, b: int):
            return a + b


        if __name__ == "__main__":
            import pickle
            with open('tmp.pickle', 'wb') as f:
                pickle.dump(add(1, 2,  ), f)
        ```\
""",
        ],
    )
