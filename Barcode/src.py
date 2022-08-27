#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip3 install pyzbar opencv-python')


# In[2]:


from pyzbar import pyzbar
import cv2


# In[3]:


def draw_barcode(decoded, image):
    # n_points = len(decoded.polygon)
    # for i in range(n_points):
    #     image = cv2.line(image, decoded.polygon[i], decoded.polygon[(i+1) % n_points], color=(0, 255, 0), thickness=5)
    # uncomment above and comment below if you want to draw a polygon and not a rectangle
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top), 
                            (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                            color=(0, 255, 0),
                            thickness=5)
    return image


# In[4]:


def decode(image):
    # decodes all barcodes from an image
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        # draw the barcode
        print("detected barcode:", obj)
        image = draw_barcode(obj, image)
        # print barcode type & data
        print("Type:", obj.type)
        print("Data:", obj.data)
        print()

    return image


# In[5]:


if __name__ == "__main__":
    from glob import glob
    cam = cv2.VideoCapture(0)
    ret,img = cam.read()
    barcodes = img
    while ret:
        # load the image to opencv
        ret,img = cam.read()
        if cv2.waitKey(1)==ord('q'):
            img = decode(img)
        # show the image
        cv2.imshow("img", img)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cam.release()
    cv2.destroyAllWindows()


# In[ ]:




