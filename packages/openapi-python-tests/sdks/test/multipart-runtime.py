import sys

import httpx


def main() -> None:
    sys.path.insert(0, sys.argv[1])
    from multipart_runtime.sdk_gen import Sdk

    image = b"\x89PNG\x00\xff"
    second_image = b"\x89PNG\x01\xfe"

    def handle(request: httpx.Request) -> httpx.Response:
        assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
        if request.url.path == "/images/batch":
            assert request.content.count(b'name="images"; filename="images"') == 2
            assert image in request.content
            assert second_image in request.content
            assert b"batch" in request.content
        else:
            assert b'name="image"; filename="image"' in request.content
            assert image in request.content
            assert b"hello" in request.content
        assert b'name="caption"' in request.content
        return httpx.Response(204)

    with httpx.Client(
        base_url="https://example.test",
        transport=httpx.MockTransport(handle),
    ) as client:
        sdk = Sdk(client=client)
        assert sdk.upload_image(image=image, caption="hello").status_code == 204
        assert sdk.upload_image_ref(image=image, caption="hello").status_code == 204
        assert sdk.upload_images(images=[image, second_image], caption="batch").status_code == 204


if __name__ == "__main__":
    main()
