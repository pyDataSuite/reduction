from pdoc import cli
from argparse import Namespace
from shutil import rmtree, move
from pathlib import Path

directory = Path( __file__ ).parent

if __name__ == "__main__":
    cli.main(
        Namespace(
            modules=["reduction"],
            config=["google_search_query='''site:pydatasuite.github.io'''"],
            filter=None,
            force=True,
            html=True,
            pdf=False,
            output_dir=str( directory/"build/docs" ),
            template_dir=None,
            close_stdin=False,
            html_dir="",
            overwrite=False,
            html_no_source=False,
            link_prefix="",
            external_links=False,
            http='',
            skip_errors=False
        )
    )

    rmtree( directory/"docs", True )
    move( directory/"build/docs/reduction/", directory/"docs" )
    rmtree( directory/"build/docs" )