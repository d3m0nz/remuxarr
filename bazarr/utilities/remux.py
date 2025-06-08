import os
import subprocess
import logging

from utilities.binaries import get_binary, BinaryNotFound

logger = logging.getLogger(__name__)


def remux(video_path: str) -> None:
    """Remux a video file using mkvmerge.

    The resulting file replaces the original one.
    """
    try:
        mkvmerge = get_binary("mkvmerge")
    except BinaryNotFound:
        logger.error("BAZARR mkvmerge binary not found")
        raise

    if not os.path.exists(video_path):
        raise FileNotFoundError(video_path)

    base, ext = os.path.splitext(video_path)
    tmp_path = f"{base}.remux{ext}"

    try:
        subprocess.check_call([mkvmerge, "-o", tmp_path, video_path])
        os.replace(tmp_path, video_path)
    except subprocess.SubprocessError:
        logger.exception("BAZARR remux failed for %s", video_path)
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
