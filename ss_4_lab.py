import cv2
from skimage.metrics import structural_similarity as ssim
import os


def check_latency(screenshot_paths):

    # assume itial condition still
    flag=0
    # Iterate over consecutive pairs of screensots
    for i in range(0,10,1):
        # Load the current and next screenshots
        # The dynamic number
        current_image = screenshot_paths[i]
        next_image  = screenshot_paths[i+1]
        print(current_image)
        print(next_image)

        current_image = cv2.imread(current_image)
        next_image = cv2.imread(next_image)

        # Compare the current and next screenshots

        gray1 = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(next_image, cv2.COLOR_BGR2GRAY)

        similarity_score = ssim(gray1, gray2)


        # define similarity threshold
        similarity_threshold = .96
        if similarity_score >= similarity_threshold:
            print("moving")
            if flag!=1:
                print("still --> moving")
                #print(current_image)
                #print(next_image)
                ss_paths = screenshot_paths[i:i+4]
                return ss_paths
            #flag=1
        
            
    

file_paths = ['moving_down_lab/','moving_up_lab/']
ss_paths = []
for i in range(len(file_paths)):
    # get the list of files present at file_paths[i]
    screenshot_paths = [os.path.join(file_paths[i], f) for f in os.listdir(file_paths[i])if os.path.isfile(os.path.join(file_paths[i], f))]
    # sort them to ensure frames are in sequence
    screenshot_paths = sorted(screenshot_paths, key=lambda x: int(str(x.split('screenshot_')[1]).split('.')[0]))
    # first four values: moving down
    # last four values: moving up
    ss_paths.extend(check_latency(screenshot_paths))

print(ss_paths[0:4])
print(ss_paths[4:])