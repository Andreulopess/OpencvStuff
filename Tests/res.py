import numpy as np
import cv2

cap = cv2.VideoCapture(0)

def vectorized_form(img):
    R,G,B = [img[:,:,x] for x in range(3)]
    delta15 = np.abs(R.astype(np.int8) - G.astype(np.int8)) > 15  # watch out for np.abs(R-G): because of the UNsigned numbers, they could get clipped!
    more_R_than_B = (R > B)
    is_skin_coloured_during_daytime = ((R > 95) & (G > 40) & (B > 20) &
        (img.ptp(axis=-1) > 15) & delta15 & (R > G) & more_R_than_B)
    is_skin_coloured_under_flashlight = ((R > 220) & (G > 210) & (B > 170) &
        ~delta15 & more_R_than_B & (G > B))
    return np.logical_or(is_skin_coloured_during_daytime, is_skin_coloured_under_flashlight)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    result = vectorized_form(frame)
    print(result)
    print("-------------------")

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()