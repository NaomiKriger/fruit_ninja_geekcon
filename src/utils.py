def get_darkened_pixels(frame) -> list:
    middle_row = frame[180]
    middle_row_lighted = [
        pixel[0] > 50 and pixel[1] > 50 and pixel[2] > 50
        for pixel in middle_row
    ]
    return [
        i
        for i, pixel in enumerate(middle_row_lighted)
        if not pixel and 50 < i < 600
    ]


def get_splitter_index(
        darkened_pixels: list,
        allowed_jumps: int,
) -> int:
    for index, pixel_location in enumerate(darkened_pixels):
        if index == 0:
            continue
        if abs(darkened_pixels[index - 1] - pixel_location) > allowed_jumps:
            return index
    return len(darkened_pixels)


def get_darkness_blobs_with_noise(
        darkened_pixels: list,
        allowed_jumps: int = 1,
) -> list:
    darkness_blobs_with_noise = []
    current_list = darkened_pixels

    while len(current_list) > 1:
        splitter_index = get_splitter_index(current_list, allowed_jumps)
        darkness_blobs_with_noise.append(current_list[0:splitter_index])
        current_list = current_list[splitter_index:]

    return darkness_blobs_with_noise


def remove_noise_blobs(
        darkness_blobs: list,
        noise_size: int,
) -> list:
    return [
        darkness_blob
        for darkness_blob in darkness_blobs
        if len(darkness_blob) > noise_size
    ]


def get_darkness_blobs(
        darkened_pixels: list,
        allowed_jumps: int = 1,
        noise_size: int = 1,
) -> list:
    darkness_blobs_with_noise = get_darkness_blobs_with_noise(
        darkened_pixels,
        allowed_jumps
    )
    return remove_noise_blobs(
        darkness_blobs_with_noise,
        noise_size,
    )


def get_main_darkness_blob(
        darkness_blobs: list,
) -> list:
    if len(darkness_blobs) > 0:
        return max(darkness_blobs, key=lambda blob: len(blob))


def get_center_of_main_darkness_blob(
        darkness_blobs: list,
) -> int:
    main_darkness_blob = get_main_darkness_blob(darkness_blobs)
    return get_average_of_list(main_darkness_blob)


def get_average_of_list(
        darkness_blob: list,
) -> int:
    return int(sum(darkness_blob) / len(darkness_blob))


def get_main_darkness_blob_center(
        darkened_pixels: list,
        allowed_jumps: int = 1,
        noise_size: int = 1,
):
    darkness_blobs = get_darkness_blobs(
        darkened_pixels,
        allowed_jumps,
        noise_size,
    )

    return get_center_of_main_darkness_blob(darkness_blobs)

