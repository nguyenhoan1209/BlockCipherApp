import time
import streamlit as st
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os
import tempfile
from io import BytesIO
from streamlit_option_menu import option_menu
from PIL import Image
import base64


st.set_page_config(page_title="BlockCipherApp", layout="wide")

col1, col2 = st.columns([3, 1])
# Define AES modes
MODES = {
    "ECB": AES.MODE_ECB,
    "CBC": AES.MODE_CBC,
    "CTR": AES.MODE_CTR,
    "CFB": AES.MODE_CFB,
    "OFB": AES.MODE_OFB,
}


def encrypt_file(file_path, key, mode, iv=None):
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, mode)
    else:
        cipher = AES.new(key, mode, iv)

    with open(file_path, "rb") as f:
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

    with open(file_path, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = cipher.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data


def search():
    st.markdown(
        """
            <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <style>
                body {
                font-family: serif0;
                }

                * {
                box-sizing: border-box;
                }

                form.example input[type=text] {
                padding: 10px;
                font-size: 17px;
                border: 1px solid grey;
                float: left;
                width: 80%;
                background: #f1f1f1;
                }

                form.example button {
                float: left;
                width: 20%;
                padding: 10px;
                background: #545454;
                color: white;
                font-size: 17px;
                border: 1px solid grey;
                border-left: none;
                cursor: pointer;
                }

                form.example button:hover {
                background: #545454;
                }

                form.example::after {
                content: "";
                clear: both;
                display: table;
                }
            </style>
            </head>
            <body>
            """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
            <form class="example" action="" style="margin:auto;max-width:300px">
            <input type="text" placeholder="Search.." name="search2">
            <button type="submit"><i class="fa fa-search"></i></button>
            </form>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
                <head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
                </head>
                """,
        unsafe_allow_html=True,
    )


def list_author():
    st.markdown(
        """
                <style>
                .c {
                    margin-top: 100px ;
                    }
                </style>

                <div class="c"></div>
                """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
                <style>
                .faded-text {
                    color: rgba(0, 0, 0, 0.5);
                    text-align: right;
                }
                </style>
                """,
        unsafe_allow_html=True,
    )

    st.markdown('<h6 class="faded-text">Nhóm sinh viên:</h6>', unsafe_allow_html=True)
    st.markdown(
        """
                <style>
                .styled-metric {
                    background-color: #f0f2f6;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 18px;
                    color: rgba(0, 0, 0, 0.5);
                    display: flex;
                    align-items: center;
                }
                .styled-metric i {
                    margin-right: 10px;
                    font-size: 20px;
                }
                </style>
                """,
        unsafe_allow_html=True,
    )

    # Display the styled metrics with Facebook icons
    st.markdown(
        '<div class="styled-metric"><i class="far fa-user"></i> Nguyễn Văn Hoàn</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="styled-metric"><i class="far fa-user"></i>Nguyễn Đức Hiếu</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="styled-metric"><i class="far fa-user"></i>Nguyễn T.Huy Hoàng</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="styled-metric"><i class="far fa-user"></i> Vũ Nhật Minh</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="styled-metric"><i class="far fa-user"></i> Hoàng Văn Tú</div>',
        unsafe_allow_html=True,
    )


def main():
    # Streamlit app

    with st.sidebar:
        st.markdown("#### Chọn chức năng ####")
        selected = option_menu(
            "Main Menu",
            ["Mã hóa", "Giải mã"],
            icons=["lock", "key"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#fafafa"},
                "icon": {"color": "black", "font-size": "15px"},
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "f0f0f0",
                    "color": "#545454",
                },
            },
        )

    # User input
    if selected == "Mã hóa":
        with col1:
            col1.title("Block Cipher Encryption")
            uploaded_en_file = st.file_uploader(
                "Tải lên file để mã hóa", type=["txt", "enc"]
            )
            key_length = st.selectbox("Chọn độ dài khóa:", [128, 192, 256])
            mode = st.selectbox("Chọn chế độ mã khối:", list(MODES.keys()))
            key_input = st.text_input("Nhập khóa bí mật (hex format):")

            # Initialize key and IV
            key = None
            iv = None

            # Render IV input if required by the selected mode
            if mode in ["CBC", "CTR", "CFB", "OFB"]:
                iv_input = st.text_input("Nhập giá trị IV (hex format):")
                try:
                    iv = bytes.fromhex(iv_input) if iv_input else None
                except ValueError:
                    st.warning("Giá trị IV chưa đúng. Vui lòng nhập lại")
            if key_input:
                try:
                    key = bytes.fromhex(key_input)
                    if len(key) * 8 != key_length:
                        st.warning(f"Giá trị khóa bí mật phải là {key_length} bits.")
                        key = None
                except ValueError:
                    st.warning("Giá trị khóa chưa đúng. Vui lòng nhập lại")
            # Encrypt
            # Encrypt button
            if st.button("Encrypt"):
                if uploaded_en_file and key is not None:
                    try:
                        # Save the uploaded file to a temporary location
                        temp_dir = tempfile.TemporaryDirectory()
                        temp_file_path = os.path.join(
                            temp_dir.name, uploaded_en_file.name
                        )
                        with open(temp_file_path, "wb") as temp_file:
                            temp_file.write(uploaded_en_file.read())

                        # Encrypt the file and measure the time
                        start_time = time.time()
                        encrypted_data = encrypt_file(
                            temp_file_path, key, MODES[mode], iv
                        )
                        end_time = time.time()

                        # Display encryption time
                        encryption_time = end_time - start_time
                        st.info(f"Thời gian mã hóa: {encryption_time:.4f} giây")

                        encrypted_file = BytesIO(encrypted_data)

                        st.success("Mã hóa thành công!")
                        st.info("Đã tạo file mã hóa.Bấm để tải xuống.")
                        st.download_button(
                            label="Download Encrypted File",
                            data=encrypted_file,
                            file_name=f"encrypted_{uploaded_en_file.name}",
                            mime="application/octet-stream",
                        )

                        # Clean up the temporary directory
                        temp_dir.cleanup()
                    except Exception as e:
                        st.error(f"Mã hóa thất bại: {str(e)}")
                else:
                    st.warning("Hãy tải file và nhập khóa !!!")
        with col2:

            search()
            list_author()

    elif selected == "Giải mã":
        col1.title("Block Cipher Decryption")
        with col1:
            uploaded_de_file = st.file_uploader(
                "Tải file lên để giải mã", type=["txt", "enc"]
            )
            key_length = st.selectbox("Chọn độ dài khóa :", [128, 192, 256])
            mode = st.selectbox("Chọn chế độ :", list(MODES.keys()))
            key_input = st.text_input("Nhập khóa bí mật :")

            # Initialize key and IV
            key = None
            iv = None

            # Render IV input if required by the selected mode
            if mode in ["CBC", "CTR", "CFB", "OFB"]:
                iv_input = st.text_input("Nhập giá trị IV (hex format):")
                try:
                    iv = bytes.fromhex(iv_input) if iv_input else None
                except ValueError:
                    st.warning("Giá trị IV chưa đúng. Vui lòng nhập lại")

            # Validate and convert the key
            if key_input:
                try:
                    key = bytes.fromhex(key_input)
                    if len(key) * 8 != key_length:
                        st.warning(f"Khóa phải dài {key_length} bits.")
                        key = None
                except ValueError:
                    st.warning("Giá trị khóa chưa đúng. Vui lòng nhập lại")

            # Decrypt button
            if st.button("Decrypt"):
                if uploaded_de_file and key is not None:
                    try:
                        # Save the uploaded file to a temporary location
                        temp_dir = tempfile.TemporaryDirectory()
                        temp_file_path = os.path.join(
                            temp_dir.name, uploaded_de_file.name
                        )
                        with open(temp_file_path, "wb") as temp_file:
                            temp_file.write(uploaded_de_file.read())

                        # Decrypt the file and measure the time
                        start_time = time.time()
                        decrypted_data = decrypt_file(
                            temp_file_path, key, MODES[mode], iv
                        )
                        end_time = time.time()

                        # Display decryption time
                        decryption_time = end_time - start_time
                        st.info(f"Thời gian giải mã: {decryption_time:.4f} giây")

                        decrypted_file = BytesIO(decrypted_data)

                        st.success("Giải mã thành công!")
                        st.info("Đã tạo file giải mã. Bấm để tải")
                        st.download_button(
                            label="Download Decrypted File",
                            data=decrypted_file,
                            file_name=f"decrypted_{uploaded_de_file.name}",
                            mime="application/octet-stream",
                        )

                        # Clean up the temporary directory
                        temp_dir.cleanup()
                    except Exception as e:
                        st.error(f"Giải mã thất bại: {str(e)}")
                else:
                    st.warning("Vui lòng tải lên file và nhập khóa")

        with col2:
            search()
            list_author()


if __name__ == "__main__":
    main()
