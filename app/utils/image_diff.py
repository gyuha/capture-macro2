import cv2
from skimage.metrics import structural_similarity as compare_ssim


class ImageDiff:
    def __init__(self):
        self.preImage = None

    def reset(self):
        self.preImage = None

    def readFile(self, filePath):
        image = cv2.imread(filePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray

    def diff(self, imagePath):
        if self.preImage is None:
            self.preImage = self.readFile(imagePath)
            return False
        try:
            currentImage = self.readFile(imagePath)

            (score, diff) = compare_ssim(self.preImage, currentImage, full=True)
            diff = (diff * 255).astype("uint8")
            self.preImage = currentImage
            return True if score >= 1.0 else False
        except Exception as e:
            print(e)
            return False
