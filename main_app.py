import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="Effex - Image Filters", layout="wide", initial_sidebar_state="expanded")

# Load CSS
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback CSS if file not found
        st.markdown("""
        <style>
        body { font-family: 'Helvetica Neue', sans-serif; }
        .stApp { padding: 2rem; }
        h1 { font-size: 3rem; font-weight: bold; color: #1e1e2d; }
        </style>
        """, unsafe_allow_html=True)

# --- Image Processing Functions ---

def apply_watercolor(inp_img):
    """Applies a watercolor effect to the image."""
    watercolor = cv2.stylization(inp_img, sigma_s=150, sigma_r=0.25)
    # Enhance details for a more artistic look
    watercolor = cv2.detailEnhance(watercolor, sigma_s=10, sigma_r=0.15)
    return watercolor

def apply_pencil_sketch(inp_img):
    """Converts the image to a more realistic pencil sketch."""
    gray_img = cv2.cvtColor(inp_img, cv2.COLOR_BGR2GRAY)
    inv_gray_img = 255 - gray_img
    blurred_img = cv2.GaussianBlur(inv_gray_img, (21, 21), 0)
    inv_blurred_img = 255 - blurred_img
    pencil_sketch = cv2.divide(gray_img, inv_blurred_img, scale=256.0)
    return cv2.cvtColor(pencil_sketch, cv2.COLOR_GRAY2BGR)

def apply_cartoon(inp_img):
    """Applies a cartoon effect to the image."""
    # Reduce the color palette
    color = cv2.bilateralFilter(inp_img, 9, 300, 300)
    # Detect edges
    gray = cv2.cvtColor(inp_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    # Combine color and edges
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

def apply_sepia(inp_img):
    """Applies a vintage sepia effect to the image."""
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    sepia_img = cv2.transform(inp_img, sepia_filter)
    sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
    # Add a subtle vignette
    rows, cols, _ = sepia_img.shape
    kernel_x = cv2.getGaussianKernel(cols, 200)
    kernel_y = cv2.getGaussianKernel(rows, 200)
    kernel = kernel_y * kernel_x.T
    mask = 255 * kernel / np.linalg.norm(kernel)
    vignette = np.copy(sepia_img)
    for i in range(3):
        vignette[:,:,i] = vignette[:,:,i] * mask
    return vignette


def apply_hdr(inp_img):
    """Applies an HDR effect to the image."""
    lab = cv2.cvtColor(inp_img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    enhanced_lab = cv2.merge((l, a, b))
    return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

def apply_sharpen(inp_img):
    """Applies an unsharp masking sharpen effect."""
    blurred = cv2.GaussianBlur(inp_img, (0, 0), 3)
    sharpened = cv2.addWeighted(inp_img, 1.5, blurred, -0.5, 0)
    return sharpened

# --- Main Application ---

def main():
    """Main function for the Streamlit app."""
    local_css("styles.css")

    st.markdown("<h1 style='text-align: center;'>Effex 🎨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Transform your images with artistic filters.</p>", unsafe_allow_html=True)

    # Sidebar for theme and file upload
    st.sidebar.header("Controls")
    dark_mode = st.sidebar.checkbox("Dark Mode", value=True)
    if dark_mode:
        st.markdown('<body class="dark-mode"></body>', unsafe_allow_html=True)

    uploaded_image = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        img_np = np.array(img)

        st.subheader("Original vs. Processed")
        col1, col2 = st.columns(2)
        with col1:
            st.image(img, caption="Original Image", use_container_width=True)

        # Filters
        filters = {
            "Watercolor": apply_watercolor,
            "Pencil Sketch": apply_pencil_sketch,
            "Cartoon": apply_cartoon,
            "Sepia": apply_sepia,
            "HDR": apply_hdr,
            "Sharpen": apply_sharpen,
        }

        selected_filter = st.radio("Choose a filter", list(filters.keys()), horizontal=True)

        if selected_filter:
            with st.spinner("Applying filter..."):
                processed_img = filters[selected_filter](img_np)
                with col2:
                    st.image(processed_img, caption=f"{selected_filter} Effect", use_container_width=True)

                # Download filtered image
                buf = BytesIO()
                processed_img_pil = Image.fromarray(processed_img)
                if processed_img_pil.mode == 'RGBA':
                    processed_img_pil = processed_img_pil.convert('RGB')
                processed_img_pil.save(buf, format="JPEG")
                st.download_button(
                    "Download Processed Image",
                    data=buf.getvalue(),
                    file_name=f"{selected_filter.lower().replace(' ', '_')}_effect.jpg",
                    mime="image/jpeg"
                )

    # Feedback section
    st.sidebar.subheader("Feedback")
    feedback = st.sidebar.text_area("What do you think?")
    if st.sidebar.button("Submit Feedback"):
        st.sidebar.success("Thank you for your feedback!")

if __name__ == "__main__":
    main()
