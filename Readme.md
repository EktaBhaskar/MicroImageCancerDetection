# **How to Run program(On Mac):**
### 1. create virtual env :- 
    python -m venv dragonfruit
### 2. Activate 
    source dragonfruit/bin/activate
### 3. Install requirements
    pip install -r requirements.txt
4. Create a folder(if not present) :- "Cancer_Images" in same directory as main.py
5. Run main.py > Results.txt with any given input image_size, , I implemented an end-to-end procedure from simulation to processing to validation.
6. Close the series of displayed images as they appear to continue running the program.
7. Check contents of Results.txt for the results.

###  Note:- 
    Since the worst case space complexity for running 100,000X100,000 image is ~ 9 GB. If you're running with 100,000X100,000 image size, make sure to run on a system that can         handle that much otherwise it might cash. Ideally running on a 16 GB RAM Mac should work.
    Rest other image sizes works great even on 8GB RAM Macbook.



# **Data Structures for Image Representation:**

## Microscope Image(Storing and calculating Cancer):

### 1. Representation: 
    a. For storing input image :- Only storing (x,y) coordinate of centre and radius of circular parasite.
### 2. Explanation: 
    a. To identify blob of parasite image, we only need location of it's centre and it's radius. Hence I store only these 2 information. It provides very efficient storage of binary sparse matrix where we don't actucally need to store big matrix.
### 3. Estimate: 
    a. For storing input image :- 
        i. storing 3 values (x, y radius) 
        ii. 8 X 3 :- 24 bytes
    

## Dye Sensor Image(Storing and calculating Cancer):
### 1. Representation: 
       4 coordinates of dye-rectangle
### 2. Explanation: 
       Coordinates are stored as (x1, x2, x3, x4), compactly representing dye locations without storing the entire image.
### 3. Estimate: 
        Since we're storing only 4 corner coordinates of the dye blob(rectangle), worst case scenario:-
        a. For each point: 2 coordinates×4 bytes/coordinate=8 bytes
        b. 4 points×8 bytes/point = 32 bytes
## In worst case, storing information for Dye-Sensor image would be 32 bytes.



## For generating output images(Microscopic and Dye) :- 

### 1. Representation: 
    a. A NumPy array of integers (0 or 1), where each element represents a pixel in the image.
### 2. Explanation: 
    a. While generating image :- NumPy arrays provide efficient storage for binary images. Each pixel is represented by a single bit, minimizing storage space.
### 3. Estimate: 
        For a 100,000×100,000 image, the worst-case storage size is:-
        i. total pixels :- 100,000×100,000=10,000,000,000 
        ii. Taking each pixel requires 8 bits (1 byte) of storage,  size in bytes:  10,000,000,000 pixels×1 byte/pixel=10,000,000,000 bytes.
        iii. 10,000,000,000 bytes÷(1024×1024) ≈ 9536.74 MB
        iv. Gigabytes (GB): 9536.74MB ÷ 1024 ≈ 9.31GB

## Additional Optimizations:-

### Microscope Image (Parasite):
1. Run-Length Encoding (RLE):
    Compression: Encode consecutive pixels with the same value (0 or 1) as a single value and count.
    Impact on Runtime: Compression involves additional encoding and decoding steps, which might marginally increase runtime.

2. Differential Encoding:
    Compression: Store the differences between consecutive pixel values.
    Impact on Runtime: Minimal impact, especially for sparse changes in pixel values.

### Dye Sensor Image:

1. Quantization:
    Compression: Reduce the precision of coordinate values (e.g., rounding to integers).
    Impact on Runtime: Minimal impact as quantization is a simple operation.

## Runtime and Storage Measurement:

1. Runtime Measurement:

    Used Python's time module to measure the execution time of functions.
    
    Storage Measurement:

    Utilized Python's tracemalloc to estimate the size of data structures.

## My Results:-
    a. Image size:- 100X100
        overlapped  0.9480310389904015
        Parasite 1 Has Cancer: True
        overlapped  0.0
        Parasite 2 Has Cancer: False
        overlapped  0.0
        Parasite 3 Has Cancer: False
        overlapped  0.04872090094649858
        Parasite 4 Has Cancer: False
        overlapped  0.7726357955830067
        Parasite 5 Has Cancer: True
        overlapped  0.04872090094649858
        Parasite 6 Has Cancer: False
        Elapsed time: 5.5072550773620605 seconds
        Current memory usage: 3.648064 MB
        Peak memory usage: 18.109443 MB

    b. Image size:- 1000X1000
        Overlapped  0.8816484744896846
        Parasite 1 Has Cancer: True
        overlapped  0.0
        Parasite 2 Has Cancer: False
        overlapped  0.0
        Parasite 3 Has Cancer: False
        overlapped  0.0
        Parasite 4 Has Cancer: False
        overlapped  0.0
        Parasite 5 Has Cancer: False
        overlapped  0.0
        Parasite 6 Has Cancer: False
        Elapsed time: 7.8468098640441895 seconds
        Current memory usage: 7.101266 MB
        Peak memory usage: 49.529884 MB

    c. Image size:- 10000X10000
        overlapped  0.0
        Parasite 1 Has Cancer: False
        overlapped  0.0
        Parasite 2 Has Cancer: False
        overlapped  0.0
        Parasite 3 Has Cancer: False
        overlapped  0.0
        Parasite 4 Has Cancer: False
        overlapped  0.0
        Parasite 5 Has Cancer: False
        overlapped  0.0
        Parasite 6 Has Cancer: False
        Elapsed time: 69.67661094665527 seconds
        Current memory usage: 503.460249 MB
        Peak memory usage: 4702.859697 MB

    d. Image size:- 100000X100000
        overlapped  0.0
        Parasite 1 Has Cancer: False
        overlapped  0.0
        Parasite 2 Has Cancer: False
        overlapped  0.0
        Parasite 3 Has Cancer: False
        overlapped  0.0
        Parasite 4 Has Cancer: True
        overlapped  0.0
        Parasite 5 Has Cancer: False
        overlapped  0.0
        Parasite 6 Has Cancer: False
        Elapsed time: 200.59681702663542 seconds
        Current memory usage: 1003.460249 MB
        Peak memory usage: 9702.859697 MB


# Optimisations for Faster Speed:-
1. To improve speed, I took advatage of the fact that both parasite and dye are consolidated blob and not scattered.
2. Instead of storing all 0's or 1's, I just stored coordinates of boundary of Parasite(radius, centre_x, centre_y), Dye(start_x, end_x, start_y, end_y) which significantly improved speed and space by 10s of folds as it takes maximum of 32 byte to store these informations.
3. To calculate if a micro-organism has cancer or not, now insead of iterating through each cell in image which has 1, I took inspiration from below mentioned algorithm and calculated overlap between 2 shapes(Parasite and Dye) just by checking few boundary conditions.
This significanlty improved time complexity from O(image size) to O(1), making it a constant time algorithm.
4. Almost all of the space and time is consumed by displaying the images on plots, in real world scenario, if researchers are only interested in predicting if a parasite has cancer or not , then this time consumption can be reduced significantly.
    

## Tools:- Github, leetcode, geeksforgeeks for looking efficient algorithm for finding overlap and syntaxes
1. Took motivation of optimised algorithm from here:-
  a. https://stackoverflow.com/questions/9324339/how-much-do-two-rectangles-overlap
  b. https://www.geeksforgeeks.org/check-if-any-point-overlaps-the-given-circle-and-rectangle/amp/

2. Took motivation of how to store information of sparse matrix from editorial of this algorithm:-
    https://leetcode.com/problems/sparse-matrix-multiplication/
