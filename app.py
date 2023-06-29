import time
import streamlit as st
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os
import tempfile
from io import BytesIO
from streamlit.elements import image
from streamlit_option_menu import option_menu
from PIL import Image
import base64

icon = Image.open("icon_app.png")
st.set_page_config(page_title="BlockCipherApp",page_icon=icon,layout="wide")

col1,col2 = st.columns([3,1])
# Define AES modes
MODES = {
    "ECB": AES.MODE_ECB,
    "CBC": AES.MODE_CBC,
    "CTR": AES.MODE_CTR,
    "CFB": AES.MODE_CFB,
    "OFB": AES.MODE_OFB
}

def encrypt_file(file_path, key, mode, iv=None):
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, mode)
    else:
        cipher = AES.new(key, mode, iv)

    with open(file_path, 'rb') as f:
        plaintext = f.read()

    padded_data = pad(plaintext, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data

def decrypt_file(file_path, key, mode, iv=None):
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, mode)
    else:
        if iv is None:
            raise ValueError("IV is required for this decryption mode.")
        cipher = AES.new(key, mode, iv)

    with open(file_path, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = cipher.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data

def main():
    # Streamlit app
    
    with st.sidebar:
        st.markdown("#### Chọn chức năng ####")
        selected = option_menu("Main Menu", ["Mã hóa", "Giải mã"],
                               icons=['lock', 'key'],
                               menu_icon="cast", default_index=0, styles={
                "container": {"padding": "5!important", "background-color": "#fafafa"},
                "icon": {"color": "black", "font-size": "15px"},
                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            })

    # User input
    if selected == "Mã hóa":
        with col1:
            col1.title("Block Cipher Encryption")
            uploaded_en_file = st.file_uploader("Upload a file", type=["txt", "enc"])
            key_length = st.selectbox("Select key length:", [128, 192, 256])
            mode = st.selectbox("Select encryption:", list(MODES.keys()))
            key_input = st.text_input("Enter the encryption key (hex format):")

            # Initialize key and IV
            key = None
            iv = None

            # Render IV input if required by the selected mode
            if mode in ["CBC", "CTR", "CFB", "OFB"]:
                iv_input = st.text_input("Enter the IV (hex format):")
                try:
                    iv = bytes.fromhex(iv_input) if iv_input else None
                except ValueError:
                    st.warning("Invalid IV format. Please enter a valid IV in hex format.")
            if key_input:
                try:
                    key = bytes.fromhex(key_input)
                    if len(key) * 8 != key_length:
                        st.warning(f"Key length should be {key_length} bits.")
                        key = None
                except ValueError:
                    st.warning("Invalid key format. Please enter a valid key in hex format.")

            # Encrypt
            # Encrypt button
            if st.button("Encrypt"):
                if uploaded_en_file and key is not None:
                    try:
                        # Save the uploaded file to a temporary location
                        temp_dir = tempfile.TemporaryDirectory()
                        temp_file_path = os.path.join(temp_dir.name, uploaded_en_file.name)
                        with open(temp_file_path, "wb") as temp_file:
                            temp_file.write(uploaded_en_file.read())

                        # Encrypt the file and measure the time
                        start_time = time.time()
                        encrypted_data = encrypt_file(temp_file_path, key, MODES[mode], iv)
                        end_time = time.time()

                        # Display encryption time
                        encryption_time = end_time - start_time
                        st.info(f"Encryption time: {encryption_time:.4f} seconds")

                        encrypted_file = BytesIO(encrypted_data)

                        st.success("Encryption successful!")
                        st.text("Encrypted file created.")
                        st.download_button(
                            label="Download Encrypted File",
                            data=encrypted_file,
                            file_name=f"encrypted_{uploaded_en_file.name}",
                            mime='application/octet-stream'
                        )

                        # Clean up the temporary directory
                        temp_dir.cleanup()
                    except Exception as e:
                        st.error(f"Encryption error: {str(e)}")
                else:
                    st.warning("Please upload a file and enter a valid encryption key.")
        with col2:
            image = Image.open("logo_app_c.png")
            st.image(image=image)
            st.markdown(
                """
                <head>
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                </head>
                <style>
                    .a {
                        background-color: #f0f2f6;
                        padding: 20px;
                        text-align: center;
                    }
                    
                    .icon-list {
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        margin-top: 10px;
                    }

                    .icon-list-item {
                        margin: 10px;
                        text-align: center;
                        cursor: pointer;
                    }

                    .icon-list-item i {
                        font-size: 20px;
                        color: black;
                    }
                    .icon-list-item span {
                    color: black;
                    text-decoration: none;
                    font-weight: bold;
                    }
                </style>
                
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="a">
                    <h6>Liên hệ với chúng tôi</h6>
                    <div class="icon-list">
                        <div class="icon-list-item">
                            <a href="https://github.com" target="_blank">
                                <i class="fab fa-github"></i>
                                <span> Github</span>
                            </a>
                        </div>
                        <div class="icon-list-item">
                            <a href="https://twitter.com" target="_blank">
                                <i class="fab fa-twitter"></i>
                                <span> Twitter</span>
                            </a>
                        </div>
                        <div class="icon-list-item">
                            <a href="https://youtube.com" target="_blank">
                                <i class="fab fa-youtube"></i>
                                <span> Youtube</span>
                            </a>
                        </div>
                        <div class="icon-list-item">
                            <a href="https://facebook.com" target="_blank">
                                <i class="fab fa-facebook"></i>
                                <span> Facebook</span>
                            </a>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    elif selected == "Giải mã":
        col1.title("Block Cipher Decryption")
        with col1:
            uploaded_de_file = st.file_uploader("Upload a file to decryp", type=["txt", "enc"])
            key_length = st.selectbox("Select key length:", [128, 192, 256])
            mode = st.selectbox("Select decryption mode:", list(MODES.keys()))
            key_input = st.text_input("Enter the encryption key (hex format):")

            # Initialize key and IV
            key = None
            iv = None

            # Render IV input if required by the selected mode
            if mode in ["CBC", "CTR", "CFB", "OFB"]:
                iv_input = st.text_input("Enter the IV (hex format):")
                try:
                    iv = bytes.fromhex(iv_input) if iv_input else None
                except ValueError:
                    st.warning("Invalid IV format. Please enter a valid IV in hex format.")

            # Validate and convert the key
            if key_input:
                try:
                    key = bytes.fromhex(key_input)
                    if len(key) * 8 != key_length:
                        st.warning(f"Key length should be {key_length} bits.")
                        key = None
                except ValueError:
                    st.warning("Invalid key format. Please enter a valid key in hex format.")

            # Decrypt button
            if st.button("Decrypt"):
                if uploaded_de_file and key is not None:
                    try:
                        # Save the uploaded file to a temporary location
                        temp_dir = tempfile.TemporaryDirectory()
                        temp_file_path = os.path.join(temp_dir.name, uploaded_de_file.name)
                        with open(temp_file_path, "wb") as temp_file:
                            temp_file.write(uploaded_de_file.read())

                        # Decrypt the file and measure the time
                        start_time = time.time()
                        decrypted_data = decrypt_file(temp_file_path, key, MODES[mode], iv)
                        end_time = time.time()

                        # Display decryption time
                        decryption_time = end_time - start_time
                        st.info(f"Decryption time: {decryption_time:.4f} seconds")

                        decrypted_file = BytesIO(decrypted_data)

                        st.success("Decryption successful!")
                        st.text("Decrypted file created.")
                        st.download_button(
                            label="Download Decrypted File",
                            data=decrypted_file,
                            file_name=f"decrypted_{uploaded_de_file.name}",
                            mime='application/octet-stream'
                        )

                        # Clean up the temporary directory
                        temp_dir.cleanup()
                    except Exception as e:
                        st.error(f"Decryption error: {str(e)}")
                else:
                    st.warning("Please upload a file and enter a valid decryption key.")

if __name__ == "__main__":
    main()

