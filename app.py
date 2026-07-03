import io
import streamlit as st
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import segno

# -----------------------------------------------------------------------------
# CONSTANTS & CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Creative QR & Image Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Style Rules for High Scannability and Sleek UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    .section-card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CORE PROCESSING UTILITIES
# -----------------------------------------------------------------------------
def apply_advanced_filters(image: Image.Image, filter_type: str, intensity: float) -> Image.Image:
    """Applies high-fidelity creative transformations and traditional filters to photos."""
    out = image.convert("RGB")
    
    if filter_type == "Retro / 80s Vibe":
        # Boost warm tones and contrast for a classic analog aesthetic
        r, g, b = out.split()
        r = r.point(lambda p: min(255, int(p * 1.15 + 10)))
        g = g.point(lambda p: int(p * 0.95))
        b = b.point(lambda p: int(p * 0.85))
        out = Image.merge("RGB", (r, g, b))
        enhancer = ImageEnhance.Contrast(out)
        out = enhancer.enhance(1.25)
        
    elif filter_type == "Cinematic Dramatic":
        # Deepen shadows, cool down tones, high contrast
        r, g, b = out.split()
        r = r.point(lambda p: int(p * 0.85))
        b = b.point(lambda p: min(255, int(p * 1.1 + 5)))
        out = Image.merge("RGB", (r, g, b))
        out = ImageEnhance.Contrast(out).enhance(1.4)
        out = ImageEnhance.Brightness(out).enhance(0.9)
        
    elif filter_type == "Monochrome Classic":
        out = ImageOps.grayscale(out).convert("RGB")
        out = ImageEnhance.Contrast(out).enhance(1.3)
        
    elif filter_type == "Gaussian Blur":
        out = out.filter(ImageFilter.GaussianBlur(radius=intensity * 5))
        
    elif filter_type == "Edge Detection":
        out = out.filter(ImageFilter.FIND_EDGES)
        
    # Extra generic enhancement adjustments linked to intensity slider if not explicit blur
    if filter_type not in ["Gaussian Blur"]:
        if intensity != 1.0:
            out = ImageEnhance.Color(out).enhance(intensity)
            
    return out

def generate_dynamic_qr(data: str, error_level: str, micro: bool, scale: int, dark_color: str, light_color: str, background_img: Image.Image = None) -> Image.Image:
    """Generates standalone or composite background QR codes dynamically using Segno engine."""
    if not data.strip():
        data = "https://github.com/afiyafazil/qr_code_generator"
        
    qr = segno.make(data, error=error_level, micro=micro)
    
    out_buffer = io.BytesIO()
    if background_img:
        # Scale background to reasonable preview sizes
        bg_processed = background_img.convert("RGB").resize((400, 400), Image.Resampling.LANCZOS)
        qr.save(
            out_buffer,
            kind="png",
            scale=scale,
            dark=dark_color,
            light=None,  # Transparent light modules to reveal background photo artwork
            finder_dark=dark_color,
            data_dark=dark_color
        )
        qr_img = Image.open(out_buffer).convert("RGBA")
        
        # Superimpose the transparent module QR code on top of the image artwork
        bg_rgba = bg_processed.resize(qr_img.size).convert("RGBA")
        combined = Image.alpha_composite(bg_rgba, qr_img)
        return combined.convert("RGB")
    else:
        qr.save(
            out_buffer,
            kind="png",
            scale=scale,
            dark=dark_color,
            light=light_color
        )
        return Image.open(out_buffer)

# -----------------------------------------------------------------------------
# APPLICATION FRONTEND PIPELINE
# -----------------------------------------------------------------------------
def main():
    st.markdown('<div class="main-header">Creative Studio & QR Matrix Workbench</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Production workspace providing real-time photo processing pipelines and matrix barcode synthesis.</div>', unsafe_allow_html=True)
    
    # Navigation tabs defining separate workspaces
    tab_photo, tab_qr = st.tabs(["📸 Advanced Image Filtering Engine", "🔗 Dynamic QR Generation Studio"])
    
    # ---- TAB 1: ADVANCED IMAGE FILTERING ----
    with tab_photo:
        st.subheader("Photo Transform & Look Pipeline")
        col_p1, col_p2 = st.columns([1, 2])
        
        with col_p1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Bring your artwork (JPEG/PNG)", type=["png", "jpg", "jpeg"], key="photo_upload")
            
            selected_filter = st.selectbox(
                "Select Creative Look / Preset",
                ["Original (No Filter)", "Retro / 80s Vibe", "Cinematic Dramatic", "Monochrome Classic", "Gaussian Blur", "Edge Detection"]
            )
            
            intensity = st.slider("Look Factor / Saturation Scale", min_value=0.0, max_value=3.0, value=1.0, step=0.1)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_p2:
            if uploaded_file:
                input_image = Image.open(uploaded_file)
                st.image(input_image, caption="Uploaded Original Base", use_container_width=True)
                
                if selected_filter != "Original (No Filter)":
                    processed_image = apply_advanced_filters(input_image, selected_filter, intensity)
                    st.image(processed_image, caption=f"Processed View: {selected_filter}", use_container_width=True)
                    
                    # Ready pipeline for local machine export download
                    img_byte_arr = io.BytesIO()
                    processed_image.save(img_byte_arr, format="PNG")
                    st.download_button(
                        label="💾 Export Processed Master Image",
                        data=img_byte_arr.getvalue(),
                        file_name="studio_processed_master.png",
                        mime="image/png"
                    )
            else:
                st.info("💡 Please upload an image artwork on the left workspace panel to activate the filtering rendering pipeline.")

    # ---- TAB 2: DYNAMIC QR MATRIX BARCODE GENERATOR ----
    with tab_qr:
        st.subheader("QR Vector Synthesis Configuration")
        col_q1, col_q2 = st.columns([1, 1])
        
        with col_q1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            qr_data = st.text_area("Target String Vector Payload (URL, Text)", value="https://github.com/afiyafazil/qr_code_generator")
            
            col_nested_1, col_nested_2 = st.columns(2)
            with col_nested_1:
                dark_color = st.color_picker("Matrix Code Fill Color", value="#000000")
                error_level = st.selectbox("ECC Resilience Budget", ["L", "M", "Q", "H"], index=2)
            with col_nested_2:
                light_color = st.color_picker("Background Safe Color", value="#FFFFFF")
                scale = st.slider("Pixel Layout Block Size (Scale)", min_value=1, max_value=20, value=8)
                
            use_micro = st.checkbox("MicroQR Variant Matrix Optimization")
            
            st.markdown("---")
            st.markdown("**Visual Blend Component (Optional)**")
            qr_bg_file = st.file_uploader("Layer Artwork behind code matrix blocks", type=["png", "jpg", "jpeg"], key="qr_bg_upload")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_q2:
            bg_img_input = Image.open(qr_bg_file) if qr_bg_file else None
            
            try:
                final_qr = generate_dynamic_qr(
                    data=qr_data,
                    error_level=error_level,
                    micro=use_micro,
                    scale=scale,
                    dark_color=dark_color,
                    light_color=light_color,
                    background_img=bg_img_input
                )
                
                st.image(final_qr, caption="Generated Dynamic Matrix Barcode Output", width=380)
                
                qr_byte_arr = io.BytesIO()
                final_qr.save(qr_byte_arr, format="PNG")
                st.download_button(
                    label="📥 Download Vector Optimized QR Code Asset",
                    data=qr_byte_arr.getvalue(),
                    file_name="matrix_studio_qr.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Matrix Configuration Fault: {str(e)}. Ensure dataset strings conform to MicroQR capacities or reduce error budgets.")

if __name__ == "__main__":
    main()
