import cv2
import numpy as np

def solution(image_path_a, image_path_b):
    ambient = cv2.imread(image_path_a)
    flash = cv2.imread(image_path_b)

    #STEP 1 - DENOISING
    diameter = 5
    sigma_color = 60.0
    sigma_space = 60.0
    subsampling_factor = 100  
    ambient = cv2.medianBlur(ambient, 5)

    def compute_gaussian_filter(spatial_size, range_size):
      coordinates = np.arange(-spatial_size, spatial_size + 1)
      x_coord, y_coord = np.meshgrid(coordinates, coordinates)

      spatial_gaussian = np.exp(-(x_coord**2 + y_coord**2) / (2 * spatial_size**2))

      intensity_diff_matrix = np.arange(256) - np.arange(256).reshape(-1, 1)
      range_gaussian = np.exp(-intensity_diff_matrix**2 / (2 * range_size**2))

      return spatial_gaussian, range_gaussian

    def symmetric_padding(image, pad_size):
      return np.pad(image, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='symmetric')

    def optimized_bilateral_filter(src_image, ref_image, spatial_size, range_size):
      spatial_filter, range_filter = compute_gaussian_filter(spatial_size, range_size)
      img_height, img_width, img_channels = src_image.shape
      padded_src = symmetric_padding(src_image, spatial_size)
      padded_ref = symmetric_padding(ref_image, spatial_size)

      output_image = np.zeros((img_height, img_width, img_channels), dtype=np.uint8)

      for ch in range(img_channels):
          src_channel = src_image[:, :, ch]
          ref_channel = padded_ref[:, :, ch]

          for row in range(img_height):
              for col in range(img_width):
                  y_start = max(0, row - spatial_size)
                  y_end = min(img_height, row + spatial_size + 1)
                  x_start = max(0, col - spatial_size)
                  x_end = min(img_width, col + spatial_size + 1)

                  src_neighborhood = src_channel[y_start:y_end, x_start:x_end]
                  ref_neighborhood = ref_channel[y_start:y_end, x_start:x_end]

                  intensity_diff = np.abs(ref_neighborhood - ref_channel[row, col])
                  weight_matrix = range_filter[intensity_diff]
                  normalization = np.sum(weight_matrix)

                  output_image[row, col, ch] = np.sum(weight_matrix * padded_src[row, col, ch]) / normalization

      return output_image



    filtered_ambient = optimized_bilateral_filter(ambient,flash, diameter//2, sigma_color)

    ambient = filtered_ambient

    #STEP2 - DETAIL TRANSFER
    scaling = 3
    blurred_flash = cv2.GaussianBlur(flash, (5, 5), 0)
    detail_layer = scaling*cv2.subtract(flash, blurred_flash).astype(np.uint8)
    enhanced_ambient = cv2.add(ambient, detail_layer)
    enhanced_ambient = np.clip(enhanced_ambient, 0, 255)

    ambient = enhanced_ambient

    alpha = 0.1

    alpha = np.clip(alpha, 0, 1)

      # Blend the images
    blended_img = cv2.addWeighted(flash, alpha, ambient, 1 - alpha, 0)

    ambient = blended_img

    return ambient
