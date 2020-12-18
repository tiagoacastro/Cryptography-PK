import cv2
import Crypto.Util.number as cu

def decode_image(img_loc):
  img = cv2.imread(img_loc)
  key1 = 0b0
  key2 = 0b0
  key3 = 0b0
  key4 = 0b0
  key5 = 0b0
  print(img[0][0])
  for i in range(len(img)):
    for j in range(len(img[i])):
      if(j == 1):
        if (img[i - 1][j - 1][0] != 255):
          key1 = 0b1 | (key1 << 1)
        else:
          key1 = key1 << 1
        if (img[i - 1][j - 1][1] != 255):
          key1 = 0b1 | (key1 << 1)
        else:
          key1 = key1 << 1
        if (img[i - 1][j - 1][2] != 255):
          key1 = 0b1 | (key1 << 1)
        else:
          key1 = key1 << 1
      if (j == 101):
        if (img[i - 1][j - 1][0] != 255):
          key2 = key2 | (0b1 << (i - 1) * 3)
        else:
          key2 = key2 << 1
        if (img[i - 1][j - 1][1] != 255):
          key2 = key2 | (0b1 << (i - 1) * 3 + 1)
        else:
          key2 = key2 << 1
        if (img[i - 1][j - 1][2] != 255):
          key2 = key2 | (0b1 << (i - 1) * 3 + 2)
        else:
          key2 = key2 << 1
      if (j == 201):
        if (img[i - 1][j - 1][0] != 255):
          key3 = key3 | (0b1 << (i - 1) * 3)
        else:
          key3 = key3 << 1
        if (img[i - 1][j - 1][1] != 255):
          key3 = key3 | (0b1 << (i - 1) * 3 + 1)
        else:
          key3 = key3 << 1
        if (img[i - 1][j - 1][2] != 255):
          key3 = key3 | (0b1 << (i - 1) * 3 + 2)
        else:
          key3 = key3 << 1
      if (j == 301):
        if (img[i - 1][j - 1][0] != 255):
          key4 = key4 | (0b1 << (i - 1) * 3)
        else:
          key4 = key4 << 1
        if (img[i - 1][j - 1][1] != 255):
          key4 = key4 | (0b1 << (i - 1) * 3 + 1)
        else:
          key4 = key4 << 1
        if (img[i - 1][j - 1][2] != 255):
          key4 = key4 | (0b1 << (i - 1) * 3 + 2)
        else:
          key4 = key4 << 1
      if (j == 401):
        if (img[i - 1][j - 1][0] != 255):
          key5 = key5 | (0b1 << (i - 1) * 3)
        else:
          key5 = key5 << 1
        if (img[i - 1][j - 1][1] != 255):
          key5 = key5 | (0b1 << (i - 1) * 3 + 1)
        else:
          key5 = key5 << 1
        if (img[i - 1][j - 1][2] != 255):
          key5 = key5 | (0b1 << (i - 1) * 3 + 2)
        else:
          key5 = key5 << 1
      if(img[i-1][j-1][0] != 255):
        img[i - 1][j - 1][0] = 0
        #key = key | (0b1 << (j-1 * 3 + (i - 1) * len(img[0]) * 3))
      if (img[i - 1][j - 1][1] != 255):
        img[i - 1][j - 1][1] = 0
        #key = key | (0b1 << (j-1 * 3 + (i - 1) * len(img[0]) * 3 + 1))
      if (img[i - 1][j - 1][2] != 255):
        img[i - 1][j - 1][2] = 0
        #key = key | (0b1 << (j-1 * 3 + (i - 1) * len(img[0]) * 3 + 2))


  #print(cu.long_to_bytes(key1).decode())
  """
  print(cu.long_to_bytes(key2).decode())
  print(cu.long_to_bytes(key3).decode())
  print(cu.long_to_bytes(key4).decode())
  print(cu.long_to_bytes(key5).decode())
  """
  print(bin(key1))
  print(bin(key2))
  print(bin(key3))
  print(bin(key4))
  print(bin(key5))

  cv2.imwrite('color_img.jpg', img)

decode_image("blank.png")