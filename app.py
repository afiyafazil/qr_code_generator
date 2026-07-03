import streamlit as st
import segno  # A simple, easy library to generate QR codes instantly

# 1. Page layout and styling setup
st.set_page_config(page_title="QR Code Studio", page_icon="🔮", layout="centered")

st.title("🔮 Instant QR Code Generator Studio")
st.write("Convert any plain text, phone number, or website URL link into a scannable QR Code!")

# 2. Capture user string inputs dynamically from the web page text box
user_input_text = st.text_input(
    "Paste your website link or text here:",
    placeholder="e.g., https://github.com/rehanu04"
)

# Advanced styling customization switches using our sidebar tools
st.sidebar.header("🎨 Design Customization")
qr_color = st.sidebar.color_picker("Pick QR Code Line Color:", "#000000")
bg_color = st.sidebar.color_picker("Pick Background Canvas Color:", "#FFFFFF")

# 3. Action Execution Button Gate
if st.button("✨ Generate Scannable QR Code"):
    if user_input_text.strip() == "":
        st.warning("⚠️ Action Required: Please type or paste a valid text/link first!")
    else:
        st.success("🎉 QR Code Compiled Successfully!")
        
        # Live processing: Generate the QR code data using our imported library tool
        compiled_qr = segno.make(user_input_text)
        
        # Save the generated matrix data directly into a temporary image file path string
        temp_filename = "my_generated_qr.png"
        compiled_qr.save(temp_filename, scale=10, dark=qr_color, light=bg_color)
        
        # Display the output image structure visually in the web dashboard screen area
        st.image(temp_filename, caption="🎯 Scan this QR code now using your mobile phone camera!")
        
        # Provide a clean download button so students can save their generated image files
        with open(temp_filename, "rb") as image_file:
            st.download_button(
                label="📥 Download QR Code Image",
                data=image_file,
                file_name="campus_qr_code.png",
                mime="image/png"
            )
message.txt
'message.txt' has been moved from My Drive to Saved from Chrome
