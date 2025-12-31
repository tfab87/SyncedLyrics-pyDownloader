import click
import os
import sys
import scanner as scanner
import metadata as metadata
import api as api

scan_directory = scanner.scan_directory
get_metadata = metadata.get_metadata
get_lyrics = api.get_lyrics

@click.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False))
@click.option('--force', is_flag=True, help="Overwrite existing .lrc files.")
@click.option('--verbose', is_flag=True, help="Show detailed output.")
def cli(directory, force, verbose):
    """
    Scans DIRECTORY for audio files and downloads lyrics from lrclib.net.
    """
    click.echo(f"Scanning {directory}...")
    
    # 1. Convert generator to list to get total count for percentage
    all_files = list(scan_directory(directory))
    total_files = len(all_files)
    
    files_processed = 0
    lyrics_downloaded = 0
    errors = 0
    last_folder = ""

    # 2. Iterate with index to calculate progress
    for index, file_path in enumerate(all_files, 1):
        
        # 3. Check if folder changed and print it
        current_folder = os.path.dirname(file_path)
        if current_folder != last_folder:
            # Print a newline to separate from the previous progress bar
            click.echo(f"\nDirectory: {current_folder}")
            last_folder = current_folder

        # 4. Print Percentage (overwrites the line using \r)
        percent = (index / total_files) * 100
        sys.stdout.write(f"\rProgress: [{percent:.1f}%] - File {index} of {total_files}")
        sys.stdout.flush()

        base_path, _ = os.path.splitext(file_path)
        lrc_path = base_path + ".lrc"

        if os.path.exists(lrc_path) and not force:
            if verbose:
                # Clear line before printing verbose msg
                sys.stdout.write("\r" + " " * 50 + "\r") 
                click.echo(f"Skipping {os.path.basename(file_path)} (LRC exists)")
            continue

        try:
            metadata = get_metadata(file_path)
            if not metadata or not metadata.get('title'):
                if verbose:
                    sys.stdout.write("\r" + " " * 50 + "\r")
                    click.echo(f"Skipping {os.path.basename(file_path)} (No metadata)")
                continue

            # API Call
            if verbose:
                sys.stdout.write("\r" + " " * 50 + "\r")
                click.echo(f"Searching for: {metadata['title']} - {metadata['artist']}")
            
            result = get_lyrics(
                title=metadata['title'],
                artist=metadata['artist'],
                album=metadata['album'],
                duration=metadata['duration']
            )

            if result:
                lyrics_content = None
                if result.get('syncedLyrics'):
                    lyrics_content = result['syncedLyrics']
                elif result.get('plainLyrics'):
                    lyrics_content = result['plainLyrics']
                
                if lyrics_content:
                    with open(lrc_path, 'w', encoding='utf-8') as f:
                        f.write(lyrics_content)
                    # Clear line for clean output
                    sys.stdout.write("\r" + " " * 50 + "\r") 
                    click.echo(f"Downloaded: {os.path.basename(file_path)}")
                    lyrics_downloaded += 1
                else:
                    if verbose:
                        sys.stdout.write("\r" + " " * 50 + "\r")
                        click.echo(f"No lyrics found for: {os.path.basename(file_path)}")
            else:
                if verbose:
                    sys.stdout.write("\r" + " " * 50 + "\r")
                    click.echo(f"Not found: {os.path.basename(file_path)}")

        except Exception as e:
            sys.stdout.write("\r" + " " * 50 + "\r")
            click.echo(f"Error processing {os.path.basename(file_path)}: {e}", err=True)
            errors += 1
        
        files_processed += 1

    click.echo("\n" + "-" * 40)
    click.echo(f"Done! Processed: {files_processed}, Downloaded: {lyrics_downloaded}, Errors: {errors}")

if __name__ == '__main__':
    # Standard Click invocation handles sys.argv automatically
    cli()
