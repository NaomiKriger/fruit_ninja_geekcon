from src.utils import get_darkness_blobs_with_noise, remove_noise_blobs, get_main_darkness_blob, \
    get_main_darkness_blob_center


def test_get_darkness_blobs_with_noise():
    result = get_darkness_blobs_with_noise([0, 1, 2, 3, 6, 7, 8, 10, 11])
    assert result == [[0, 1, 2, 3], [6, 7, 8], [10, 11]]


def test_get_darkness_blobs_with_noise_with_allowed_jumps():
    result = get_darkness_blobs_with_noise([0, 1, 2, 3, 5, 7, 10, 11], 2)
    assert result == [[0, 1, 2, 3, 5, 7], [10, 11]]


def test_remove_noise_blobs():
    darkness_blobs = [
        [0, 1, 2, 3],
        [6, 7, 8],
        [10, 11],
        [200, 201, 202, 203, 204],
        [650],
    ]
    result = remove_noise_blobs(darkness_blobs, 2)
    assert result == [
        [0, 1, 2, 3],
        [6, 7, 8],
        [200, 201, 202, 203, 204]
    ]

    result = remove_noise_blobs(darkness_blobs, 3)
    assert result == [
        [0, 1, 2, 3],
        [200, 201, 202, 203, 204]
    ]


def test_get_main_darkness_blob():
    darkness_blobs = [
        [0, 1, 2, 3],
        [6, 7, 8],
        [10, 11],
        [200, 201, 202, 203, 204],
        [650],
    ]
    result = get_main_darkness_blob(
        darkness_blobs
    )
    assert result == [200, 201, 202, 203, 204]


def test_get_main_darkness_blob_center():
    darkness_blobs = [
        0, 1, 2, 3,
        6, 7, 8, 10, 11,
        200, 201, 202, 203, 204,
        650,
    ]
    result = get_main_darkness_blob_center(
        darkness_blobs,
        allowed_jumps=1,
        noise_size=1,
    )
    assert result == 202

    result = get_main_darkness_blob_center(
        darkness_blobs,
        allowed_jumps=2,
        noise_size=2,
    )
    assert result == 8

    result = get_main_darkness_blob_center(
        darkness_blobs,
        allowed_jumps=2,
        noise_size=5,
    )
    assert result is None
