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
            self.preImage = currentImage
            threshold = 0.995 # 1이면 완전히 같은 이미지, 0이면 완전히 다른 이미지
            return True if score >= threshold else False
        except Exception as e:
            return False
