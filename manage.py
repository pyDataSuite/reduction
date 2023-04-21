from argparse import ArgumentParser, Namespace
from pathlib import Path
from pdoc import cli
import os
import shutil

d = Path( __file__ ).parent.resolve()

if __name__ == "__main__":
    parser = ArgumentParser( 
        description=( "Executing reduction as a package gives access to a variety of "
                      "build tools for internal project development. Through it you can " 
                      "generate documentation, run unit tests, and more (maybe)! " )
    )

    parser.add_argument( "--test", help="Run unit tests", action="store_true" )
    parser.add_argument( "--benchmark", help="Run benchmarks", action="store_true" )
    parser.add_argument( "--build", help="Builds the package and its documentation", action="store_true" )
    
    args = parser.parse_args()
    
    if args.build:
        os.chdir( d )
        os.system( "python setup.py build_ext --inplace" )

        cli.main(
            Namespace(
                modules=["reduction"],
                config=["google_search_query='''site:pydatasuite.github.io'''"],
                filter=None,
                force=True,
                html=True,
                pdf=False,
                output_dir=str( d/"build/docs" ),
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

        shutil.rmtree( d/"docs", True )
        shutil.move( d/"build/docs/reduction/", d/"docs" )
        shutil.rmtree( d/"build/docs" )

        # Copy html files into documentation directory, maintaining their directory structure from the root of the package
        os.chdir( d/'reduction')
        files = Path( '.' ).rglob( "*.html" )
        for f in files:
            if not ( d/'docs'/f ).parent.is_dir():
                ( d/'docs'/f ).mkdir( parents=True )
            shutil.move( f, d/'docs'/f )

        # Do the same for C files
        os.chdir( d/'reduction')
        files = Path( '.' ).rglob( "*.c" )
        for f in files:
            if not ( d/'docs'/f ).parent.is_dir():
                ( d/'docs'/f ).mkdir( parents=True )
            shutil.move( f, d/'docs'/f )

        


        