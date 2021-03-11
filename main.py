import sys
import cv2
import imutils
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def showImage(image, title='image'):
  cv2.imshow(title, image)
  cv2.waitKey()
  cv2.destroyAllWindows

def cleanText(text):
  newText = ""

  for char in text:
    print(ord(char))

    '''
    ASCII values

    32      => Space
    48-57   => 0-9
    65-90   => A-Z
    97-122  => a-z
    '''
    if  (
          ord(char) in range(48, 57 + 1) or 
          ord(char) in range(65, 90 + 1) or 
          ord(char) in range(97, 122 + 1) or 
          ord(char) == 32
        ):
      newText += char

  return newText

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print('image path missing')
    print('Usage: python main.py <relative path to image> <debug [True | False]>')
    exit()

  SHOWSTEPS = (sys.argv[2] == 'True')

  # Read image and resize
  image = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)

  if image is None:
    print('Image not found')
    exit()

  image = cv2.resize(image, (600, 400) )

  # Convert to grayscale and apply blur to remove noise
  grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
  grayscale = cv2.bilateralFilter(grayscale, 13, 15, 15) 

  # Find edges using canny algorithm and pick the 10 with biggest area
  edged = cv2.Canny(grayscale, 30, 200)

  contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contours = imutils.grab_contours(contours)
  contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

  # Find a contour with 4 corners
  screenCnt = None

  for cnt in contours:
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.018 * peri, True)

    if len(approx) == 4:
      screenCnt = approx
      break

  if screenCnt is None:
    print ("No numberplate detected")
    exit()
  else:
    if SHOWSTEPS:
      cv2.drawContours(image, [screenCnt], -1, (0, 0, 255), 3)

  # Extract numberplate from image
  mask = np.zeros(grayscale.shape,np.uint8)
  new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
  new_image = cv2.bitwise_and(image, image, mask=mask)

  (x, y) = np.where(mask == 255)
  (topx, topy) = (np.min(x), np.min(y))
  (bottomx, bottomy) = (np.max(x), np.max(y))
  cropped = grayscale[topx:bottomx+1, topy:bottomy+1]

  # Run numberplate through Tesseract
  text = pytesseract.image_to_string(cropped, config='--psm 11')
  text = cleanText(text)

  # Show results
  print("Numberplate: ", text)

  if SHOWSTEPS:
    image = cv2.resize(image,(500,300))
    cropped = cv2.resize(cropped,(400,200))

    showImage(image, "Car with bounding box")
    showImage(cropped, "Numberplate")
