#!/usr/bin/env python3
import argparse, sys, subprocess, hashlib, time, shutil
from pathlib import Path
import yaml, requests
from rich import print
from rich.progress import Progress

class FetchError(Exception):
    pass

def sha256sum(fp: Path) -> str:
    h = hashlib.sha256()
    with fp.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def download_http(url: str, out: Path, timeout: int, ua: str):
    headers = {"User-Agent": ua}
    with requests.get(url, stream=True, timeout=timeout, headers=headers) as r:
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        with Progress() as prog:
            task = prog.add_task(f"[cyan]GET {url.split('/')[-1]}", total=total)
            with out.open('wb') as f:
                for chunk in r.iter_content(chunk_size=1<<20):
                    if chunk:
                        f.write(chunk)
                        prog.update(task, advance=len(chunk))


def run(cmd: list, cwd: Path = None):
    print(f"[dim]$ {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if res.returncode != 0:
        print(res.stdout)
        raise FetchError(f"Command failed: {' '.join(cmd)}")
    return res.stdout


def fetch_kaggle(slug: str, dest: Path, files: list):
    if shutil.which('kaggle') is None:
        raise FetchError("Kaggle CLI not found. Install with `pip install kaggle` and place API token at ~/.kaggle/kaggle.json")
    dest_tmp = dest / "__tmp__"
    ensure_dir(dest_tmp)
    if files:
        for fn in files:
            run(["kaggle","datasets","download","-d", slug, "-f", fn, "-p", str(dest_tmp), "-q"])
    else:
        run(["kaggle","datasets","download","-d", slug, "-p", str(dest_tmp), "-q"])
    # unzip all zips
    for z in dest_tmp.glob("*.zip"):
        run(["python","-m","zipfile","-e", str(z), str(dest)])
    # move loose files
    for f in dest_tmp.iterdir():
        if f.is_file() and f.suffix != ".zip":
            f.rename(dest/f.name)
    # cleanup
    for f in dest_tmp.glob("*"):
        if f.exists():
            if f.is_file(): f.unlink()
            else: shutil.rmtree(f)
    dest_tmp.rmdir()


def apply_postprocess(dest: Path, actions: list):
    import tarfile, zipfile
    for action in actions or []:
        if 'unzip' in action:
            z = dest / action['unzip']
            with zipfile.ZipFile(z) as zf:
                zf.extractall(dest)
        if 'tar_extract' in action:
            t = dest / action['tar_extract']
            with tarfile.open(t) as tf:
                tf.extractall(dest)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cfg', default='hwr64/configs/datasets.yaml')
    ap.add_argument('--only', nargs='*', help='subset of dataset names to fetch')
    ap.add_argument('--verify', action='store_true', help='verify checksums only, no downloads')
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.cfg).read_text())
    root = Path(cfg.get('root', 'hwr64/data/raw'))
    opts = cfg.get('options', {})
    timeout = int(opts.get('timeout_sec', 1800))
    ua = opts.get('user_agent', 'hwr64-fetch/1.0')

    for ds in cfg['datasets']:
        name = ds['name']
        if args.only and name not in args.only:
            continue
        method = ds['method']
        dest = root / ds['dest']
        if method == 'git':
            dest.parent.mkdir(parents=True, exist_ok=True)
        else:
            ensure_dir(dest)
        print(f"\n[bold green]Dataset:[/bold green] {name} → {dest}")

        if method == 'manual':
            print(f"[yellow]Manual dataset. Instructions:[/yellow]\n{ds.get('instructions','No instructions provided.')}")
            continue

        if method == 'kaggle':
            slug = ds['kaggle']['dataset']
            files = ds['kaggle'].get('files', [])
            fetch_kaggle(slug, dest, files)
            apply_postprocess(dest, ds.get('postprocess', []))
            continue

        if method == 'git':
            run(["git","clone","--depth","1", ds['repo'], str(dest)])
            continue

        if method == 'http':
            for f in ds['files']:
                url = f['url']
                out = dest / Path(url).name
                if out.exists() and not args.verify:
                    print(f"[dim]Skip existing {out.name}")
                else:
                    if not args.verify:
                        download_http(url, out, timeout=timeout, ua=ua)
                if f.get('sha256'):
                    got = sha256sum(out)
                    if got != f['sha256']:
                        raise FetchError(f"Checksum mismatch for {out.name}: {got} != {f['sha256']}")
            apply_postprocess(dest, ds.get('postprocess', []))
            continue

        raise FetchError(f"Unknown method: {method}")

if __name__ == '__main__':
    t0 = time.time()
    try:
        main()
        print(f"\n[bold]Done[/bold] in {time.time()-t0:.1f}s")
    except Exception as e:
        print(f"[red]ERROR:[/red] {e}")
        sys.exit(1)
