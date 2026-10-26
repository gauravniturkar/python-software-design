"""
CASE STUDY: FILE STORAGE SERVICE

Everyday picture: a locker service.
You hand over a bag and get a token. Behind the counter, the bag might go to
a cupboard in the back room (local disk), a bank vault (S3) or a warehouse.
You never care which. You just show your token to get it back.

Requirements
  - Users upload profile pictures and documents.
  - Dev uses the local disk; production uses cloud storage (S3).
  - Business rules (size limit, allowed types, unique names) must be the same
    everywhere and must not know which storage is used.

Concepts used
  Ports & adapters (architecture/)  -> FileStorage is a port
  Adapter (design-patterns/)        -> wraps a cloud SDK with a different API
  Dependency Inversion (solid/)     -> the service depends on the port only
  Composition root (DI)             -> pick storage at startup
"""
import tempfile
import uuid
from pathlib import Path
from typing import Protocol


# ===========================================================================
# PORT: what the core needs from "storage"
# ===========================================================================
class FileStorage(Protocol):
    def put(self, key: str, data: bytes) -> None: ...
    def get(self, key: str) -> bytes: ...
    def exists(self, key: str) -> bool: ...


# ===========================================================================
# CORE: business rules for uploads, with no storage details
# ===========================================================================
class UploadRejected(Exception):
    pass


class UploadService:
    MAX_BYTES = 1_000_000
    ALLOWED_EXTENSIONS = {".png", ".jpg", ".pdf"}

    def __init__(self, storage: FileStorage):
        self.storage = storage

    def upload(self, user_id: str, filename: str, data: bytes) -> str:
        extension = Path(filename).suffix.lower()
        if extension not in self.ALLOWED_EXTENSIONS:
            raise UploadRejected(f"'{extension}' files are not allowed")
        if len(data) > self.MAX_BYTES:
            raise UploadRejected("file is larger than 1 MB")

        # Unique key so two users uploading 'photo.png' don't overwrite each other
        key = f"{user_id}/{uuid.uuid4().hex}{extension}"
        self.storage.put(key, data)
        return key  # the "locker token"

    def download(self, key: str) -> bytes:
        if not self.storage.exists(key):
            raise FileNotFoundError(key)
        return self.storage.get(key)


# ===========================================================================
# ADAPTERS
# ===========================================================================
class InMemoryStorage:
    """For tests: a dictionary."""

    def __init__(self):
        self.files: dict[str, bytes] = {}

    def put(self, key: str, data: bytes) -> None:
        self.files[key] = data

    def get(self, key: str) -> bytes:
        return self.files[key]

    def exists(self, key: str) -> bool:
        return key in self.files


class LocalDiskStorage:
    """For development: real files in a folder."""

    def __init__(self, root: Path):
        self.root = root

    def put(self, key: str, data: bytes) -> None:
        path = self.root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def get(self, key: str) -> bytes:
        return (self.root / key).read_bytes()

    def exists(self, key: str) -> bool:
        return (self.root / key).exists()


class FakeCloudSDK:
    """Pretend third-party SDK (like boto3) with its OWN method names."""

    def __init__(self):
        self._buckets: dict[str, dict[str, bytes]] = {}

    def put_object(self, Bucket: str, Key: str, Body: bytes) -> dict:
        self._buckets.setdefault(Bucket, {})[Key] = Body
        return {"ETag": "abc"}

    def get_object(self, Bucket: str, Key: str) -> dict:
        return {"Body": self._buckets[Bucket][Key]}

    def list_keys(self, Bucket: str) -> list[str]:
        return list(self._buckets.get(Bucket, {}))


class CloudStorageAdapter:
    """ADAPTER: makes the SDK's API fit our FileStorage port."""

    def __init__(self, sdk: FakeCloudSDK, bucket: str):
        self.sdk = sdk
        self.bucket = bucket

    def put(self, key: str, data: bytes) -> None:
        self.sdk.put_object(Bucket=self.bucket, Key=key, Body=data)

    def get(self, key: str) -> bytes:
        return self.sdk.get_object(Bucket=self.bucket, Key=key)["Body"]

    def exists(self, key: str) -> bool:
        return key in self.sdk.list_keys(Bucket=self.bucket)


# ===========================================================================
# COMPOSITION ROOT: choose the adapter once, at startup
# ===========================================================================
def build_upload_service(environment: str, local_root: Path) -> UploadService:
    if environment == "production":
        return UploadService(CloudStorageAdapter(FakeCloudSDK(), bucket="user-files"))
    if environment == "test":
        return UploadService(InMemoryStorage())
    return UploadService(LocalDiskStorage(local_root))


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        for env in ["development", "production", "test"]:
            service = build_upload_service(env, Path(tmp))
            token = service.upload("user42", "avatar.PNG", b"\x89PNG...fake image bytes")
            data = service.download(token)
            print(f"{env:<12} stored as {token[:20]}...  -> got back {len(data)} bytes")

        service = build_upload_service("test", Path(tmp))
        for name, payload in [("virus.exe", b"x"), ("huge.pdf", b"x" * 2_000_000)]:
            try:
                service.upload("user42", name, payload)
            except UploadRejected as error:
                print(f"Rejected {name}: {error}")

# EXERCISE
#   Add a `delete(key)` method. Notice you must update the port AND every
#   adapter. That's the cost of an abstraction, so keep ports small (ISP).
