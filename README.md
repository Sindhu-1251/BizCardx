# BizCardx: Extracting Business Card Data with OCR

BizCardX is a powerful Streamlit application that makes business card data extraction simple and efficient using advanced OCR technology. Users can easily upload images of business cards to extract essential information such as company names, cardholder names, and contact details. Prioritizing data security and user authentication, BizCardX ensures that all data is stored securely. The streamlined management and user-friendly interface of Streamlit make BizCardX the ultimate solution for effortlessly managing business card information.

## Technologies Used
- Python
- EasyOCR
- Data Extraction
- MySQL
- Streamlit (GUI development)

## Packages

To run this project, you need to install the following packages:

```sh
pip install easyocr
pip install pandas
pip install numpy
pip install pymysql
pip install streamlit
pip install streamlit_option_menu
```

## Features

- **Text Extraction**: Extracts information from business card images using EasyOCR.
- **Image Preprocessing**: Utilizes OpenCV for resizing, cropping, and enhancing images.
- **Data Parsing**: Uses regular expressions (RegEx) to parse and extract specific fields like name, designation, company, and contact details.
- **Database Integration**: Stores extracted information in a MySQL database for easy retrieval and analysis.
- **Streamlit Interface**: Provides a user-friendly interface to upload images, extract information, and manage database entries.

## Usage

1. **Run the Streamlit application**:

    ```sh
    streamlit run bizcard.py
    ```
    
2. **Access the application** Clone the repository: git clone (https://github.com/Sindhu-1251/BizCardx) Run the Streamlit app: streamlit run Bizcardx.py Access the app in your browser at (http://localhost:8502).

3. **Upload a business card image** to extract information.

4. **Image Preprocessing**: The application preprocesses the image using OpenCV, including resizing, cropping, and enhancing.

5. **Text Extraction**: The processed image is passed to EasyOCR for text extraction.

6. **Display and Store Information**: Extracted information is displayed on the screen and stored in the MySQL database.

7. **Database Operations**: Use the provided options in the Streamlit interface to view, update, or analyze the extracted data stored in the database.
