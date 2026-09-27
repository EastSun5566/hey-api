import sys

import httpx


def main() -> None:
    sys.path.insert(0, sys.argv[1])
    from multipart_runtime.sdk_gen import Sdk

    image = b"\x89PNG\x00\xff"

    def handle(request: httpx.Request) -> httpx.Response:
        assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
        assert b'name="image"; filename="image"' in request.content
        assert image in request.content
        assert b'name="caption"' in request.content
        assert b"hello" in request.content
        return httpx.Response(204)

    with httpx.Client(
        base_url="https://example.test",
        transport=httpx.MockTransport(handle),
    ) as client:
        response = Sdk(client=client).upload_image(image=image, caption="hello")
        assert response.status_code == 204


if __name__ == "__main__":
    main()
