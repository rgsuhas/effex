import streamlit as st 
from PIL import Image 
from io import BytesIO 
import numpy as np 
import cv2 # computer vision 

# Set page configuration
st.set_page_config(layout="wide")

# function to convert an image to a watercolor sketch 
def convertto_watercolorsketch(inp_img):
    # Initial smoothing to preserve edges and reduce noise
    img_smoothed = cv2.edgePreservingFilter(inp_img, flags=1, sigma_s=64, sigma_r=0.6)
    
    # Apply stylization to give a watercolor effect with vibrant colors
    img_stylized = cv2.stylization(img_smoothed, sigma_s=150, sigma_r=0.25)
    
    # Additional edge enhancement to create stronger outlines
    gray = cv2.cvtColor(inp_img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    enhanced_watercolor = cv2.addWeighted(img_stylized, 0.9, edges_colored, 0.3, 0)

    return enhanced_watercolor

# function to convert an image to a pencil sketch 
def pencilsketch(inp_img): 
    img_pencil_sketch, pencil_color_sketch = cv2.pencilSketch( 
        inp_img, sigma_s=50, sigma_r=0.07, shade_factor=0.0825) 
    return img_pencil_sketch 

def sharpen_effect(inp_img):
    # Convert to YCrCb color space
    ycrcb_img = cv2.cvtColor(inp_img, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb_img)
    
    # Apply sharpening kernel to the luminance channel
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
    y_sharpened = cv2.filter2D(y, -1, kernel)
    y_sharpened = np.clip(y_sharpened, 0, 255).astype(np.uint8)
    
    # Merge channels back together
    sharpened_ycrcb = cv2.merge((y_sharpened, cr, cb))
    # Convert back to BGR color space
    sharpened_bgr = cv2.cvtColor(sharpened_ycrcb, cv2.COLOR_YCrCb2BGR)
    return sharpened_bgr

# Cartoon effect
def cartoon_effect(inp_img):
    # Ensure the image is in the correct format
    if inp_img.dtype != np.uint8:
        inp_img = np.uint8(inp_img)
    if inp_img.ndim == 2:  # If grayscale, convert to BGR
        inp_img = cv2.cvtColor(inp_img, cv2.COLOR_GRAY2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(inp_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )
    # Apply bilateral filter for smoothening
    color = cv2.bilateralFilter(inp_img, 9, 300, 300)
    # Combine edges and color
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

# Sepia effect
def sepia_effect(inp_img):
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    sepia_img = cv2.transform(inp_img, sepia_filter)
    sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
    return sepia_img

# HDR effect
def hdr_effect(inp_img):
    # Convert the image to LAB color space to work on lightness
    lab_img = cv2.cvtColor(inp_img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_img)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to the lightness channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    # Merge the modified lightness channel back with A and B channels
    enhanced_lab_img = cv2.merge((l, a, b))
    enhanced_img = cv2.cvtColor(enhanced_lab_img, cv2.COLOR_LAB2BGR)
    
    # Add detail enhancement for texture boost
    detail = cv2.detailEnhance(enhanced_img, sigma_s=15, sigma_r=0.3)
    
    # Increase vibrancy by slightly boosting saturation
    hsv_img = cv2.cvtColor(detail, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_img)
    s = cv2.add(s, 30)  # Increase saturation (clipping handled automatically)
    hdr_vibrant = cv2.merge((h, s, v))
    hdr = cv2.cvtColor(hdr_vibrant, cv2.COLOR_HSV2BGR)

    return hdr

# function to load an image 
def load_an_image(image): 
    img = Image.open(image) 
    return img 

# Add a background style
st.markdown("""
    <style>
    .stApp {
        background-color: #1d1d2a; /* Steel Gray */
        padding: 20px;
        border-radius: 10px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #e1c6c6; /* Dust Storm */
    }
    p, label {
        color: #606071; /* Mid Gray */
    }
    div.stButton > button {
        background-color: #40404f; /* Gun Powder */
        color: #e1c6c6; /* Dust Storm */
        border: 1px solid #9f7f7f; /* Pharlap */
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #9f7f7f; /* Pharlap */
        color: #1d1d2a; /* Steel Gray */
    }
    img {
        border: 5px solid #40404f; /* Gun Powder */
        border-radius: 10px;
    }
    section[data-testid="stSidebar"] {
        background-color: #40404f; /* Gun Powder */
        color: #e1c6c6; /* Dust Storm */
    }
    </style>
""", unsafe_allow_html=True)

# the main function which has the code for 
# the web application 
def main():
    st.title('Image Filter Application')
    st.write("Apply artistic filters like watercolor, pencil sketch, cartoon, sepia, HDR, and sharpen effects to your images.")

    # Toggle for dark and light mode
    dark_mode = st.sidebar.checkbox("Dark Mode", value=True)

    if dark_mode:
        st.markdown("""
            <style>
            .stApp {
                background-color: #1d1d2a; /* Steel Gray */
                padding: 20px;
                border-radius: 10px;
            }
            h1, h2, h3, h4, h5, h6 {
                color: #e1c6c6; /* Dust Storm */
            }
            p, label {
                color: #606071; /* Mid Gray */
            }
            div.stButton > button {
                background-color: #40404f; /* Gun Powder */
                color: #e1c6c6; /* Dust Storm */
                border: 1px solid #9f7f7f; /* Pharlap */
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 16px;
            }
            div.stButton > button:hover {
                background-color: #9f7f7f; /* Pharlap */
                color: #1d1d2a; /* Steel Gray */
            }
            img {
                border: 5px solid #40404f; /* Gun Powder */
                border-radius: 10px;
            }
            section[data-testid="stSidebar"] {
                background-color: #40404f; /* Gun Powder */
                color: #e1c6c6; /* Dust Storm */
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp {
                background-color: #ffffff; /* White */
                padding: 20px;
                border-radius: 10px;
            }
            h1, h2, h3, h4, h5, h6 {
                color: #000000; /* Black */
            }
            p, label {
                color: #333333; /* Dark Gray */
            }
            div.stButton > button {
                background-color: #f0f0f0; /* Light Gray */
                color: #000000; /* Black */
                border: 1px solid #cccccc; /* Light Gray */
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 16px;
            }
            div.stButton > button:hover {
                background-color: #cccccc; /* Light Gray */
                color: #000000; /* Black */
            }
            img {
                border: 5px solid #f0f0f0; /* Light Gray */
                border-radius: 10px;
            }
            section[data-testid="stSidebar"] {
                background-color: #f0f0f0; /* Light Gray */
                color: #000000; /* Black */
            }
            </style>
        """, unsafe_allow_html=True)

    # Layout: File uploader and filter options
    upload_col, filter_col = st.columns([1, 2])
    with upload_col:
        st.subheader("Upload Your Image")
        image_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"], help="Supports PNG, JPG, and JPEG formats.")
    
    with filter_col:
        st.subheader("Choose a Filter")
        filters = {
            "Watercolor Sketch": "🖌️",
            "Pencil Sketch": "✏️",
            "Cartoon Effect": "🎨",
            "Sepia Effect": "📜",
            "HDR Effect": "🌄",
            "Sharpen Effect": "🔍"
        }
        option = None
        for filter_name, emoji in filters.items():
            if st.button(f"{emoji} {filter_name}"):
                option = filter_name

    # Display filter previews
# Display filter previews vertically
if image_file is not None:
    st.subheader("Filter Previews")
    image = Image.open(image_file)
    image_np = np.array(image)

    filter_functions = [
        ("Watercolor Sketch", convertto_watercolorsketch),
        ("Pencil Sketch", pencilsketch),
        ("Cartoon Effect", cartoon_effect),
        ("Sepia Effect", sepia_effect),
        ("HDR Effect", hdr_effect),
        ("Sharpen Effect", sharpen_effect)
    ]

    for filter_name, filter_func in filter_functions:
        st.markdown(f"### {filter_name}")
        filtered_img = filter_func(image_np)
        st.image(Image.fromarray(filtered_img), use_container_width=True, caption=filter_name)

    # Process and display the selected filter
    if option:
        st.subheader(f"{option} Result")
        filter_map = {
            'Watercolor Sketch': convertto_watercolorsketch,
            'Pencil Sketch': pencilsketch,
            'Cartoon Effect': cartoon_effect,
            'Sepia Effect': sepia_effect,
            'HDR Effect': hdr_effect,
            'Sharpen Effect': sharpen_effect
        }
        final_image = filter_map[option](image_np)
        col1, col2 = st.columns(2)
        with col1:
            st.header("Original Image")
            st.image(image, use_container_width=True)
        with col2:
            st.header("Processed Image")
            st.image(final_image, use_container_width=True)

        # Download button
        buf = BytesIO()
        Image.fromarray(final_image).save(buf, format="JPEG")
        byte_im = buf.getvalue()
        st.download_button(
            label="Download Processed Image",
            data=byte_im,
            file_name=f"{option.lower().replace(' ', '_')}.jpg",
            mime="image/jpeg"
        )

        
    # Add feedback section
    st.sidebar.subheader("Feedback")
    feedback = st.sidebar.text_area("Share your feedback about the app!")
    if st.sidebar.button("Submit Feedback"):
        st.sidebar.success("Thank you for your feedback!")

if __name__ == '__main__': 
    main()
