import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import pymysql
import re
import io

Biz = Image.open(r"C://Users//sindh//OneDrive//Desktop//Pro_img//ocr-picture.webp")
st.set_page_config(page_title= "BizCardX: Extracting Business Card Data with OCR | Sindhu S", page_icon=Biz,
                   layout= "wide",
                   initial_sidebar_state= "expanded")
st.markdown("<h1 style='text-align: center; color: white;'>BizCardX: Extracting Business Card Data with OCR</h1>", unsafe_allow_html=True)

st.title(':blue[ BizCardX: Extracting Business Card Data with OCR ]')


def img_to_txt(path):

    input_img = Image.open(path)

    # Converting image to array format

    img_array = np.array(input_img)

    reader = easyocr.Reader(['en'])
    txt = reader.readtext(img_array, detail= 0)

    return txt, input_img


# funtion define
def get_data(res):

    # Initialize the data dictionary
    data = {
    "Company_name": [],
    "Card_holder": [],
    "Designation": [],
    "Mobile_number": [],
    "Email": [],
    "Website": [],
    "Area": [],
    "City": [],
    "State": [],
    "Pin_code": [],
    }

    city = ""  # Initialize the city variable
    for ind, i in enumerate(res):
        # To get WEBSITE_URL
        if "www " in i.lower() or "www." in i.lower():
            data["Website"].append(i)
        elif "WWW" in i:
            data["Website"].append(res[ind-1] + "." + res[ind])

        # To get EMAIL ID
        elif "@" in i:
            data["Email"].append(i)

        # To get MOBILE NUMBER
        elif "-" in i:
            data["Mobile_number"].append(i)
            if len(data["Mobile_number"]) == 2:
                data["Mobile_number"] = " & ".join(data["Mobile_number"])

        # To get COMPANY NAME
            
        elif ind == len(res) - 1:
            data["Company_name"].append(i)

        # To get CARD HOLDER NAME
        elif ind == 0:
            data["Card_holder"].append(i)

        # To get DESIGNATION
        elif ind == 1:
            data["Designation"].append(i)

        # To get AREA
        if re.findall("^[0-9].+, [a-zA-Z]+", i):
            data["Area"].append(i.split(",")[0])
        elif re.findall("[0-9] [a-zA-Z]+", i):
            data["Area"].append(i)

        # To get CITY NAME
        match1 = re.findall(".+St , ([a-zA-Z]+).+", i)
        match2 = re.findall(".+St,, ([a-zA-Z]+).+", i)
        match3 = re.findall("^[E].*", i)
        if match1:
            city = match1[0]  # Assign the matched city value
        elif match2:
            city = match2[0]  # Assign the matched city value
        elif match3:
            city = match3[0]  # Assign the matched city value

        # To get STATE
        state_match = re.findall("[a-zA-Z]{9} +[0-9]", i)
        if state_match:
            data["State"].append(i[:9])
        elif re.findall("^[0-9].+, ([a-zA-Z]+);", i):
            data["State"].append(i.split()[-1])
        if len(data["State"]) == 2:
            data["State"].pop(0)

        # To get PINCODE
        if len(i) >= 6 and i.isdigit():
            data["Pin_code"].append(i)
        elif re.findall("[a-zA-Z]{9} +[0-9]", i):
            data["Pin_code"].append(i[10:])

    data["City"].append(city)  # Append the city value to the 'city' array

    return data


# Streamlit Part

with st.sidebar:
    menu = option_menu("Menu",["Home","Upload Data","Modify Data","Delete Data"])

if menu == "Home":

        st.markdown("### :blue[Welcome to the Business Card Application!]")
        st.markdown('### Bizcard is a Python application designed to extract information from business cards. It utilizes various technologies such as :blue[Streamlit, Python, EasyOCR , PIL and MySQL] database to achieve this functionality.')
        st.write('### The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.')


        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        st.write('### :blue[Technologies Used]')
        st.write('### :white[Python]  :white[Streamlit] :white[EasyOCR]  :white[PIL(Python Imaging Library)]  :white[MySQL]')

elif menu == "Upload Data":
    image = st.file_uploader("Upload The Image", type = ["png","jpg","jpeg"])

    if image is not None:
        st.image(image, width=350)

        text_img, input_img = img_to_txt(image)

        extract_dict= get_data(text_img)

        if extract_dict:
            st.success("Text is Extracted successfully")

        df = pd.DataFrame(extract_dict)

        st.dataframe(df.T)

        button_1 = st.button("Save")

        if button_1:

            #SQL Connection

            mydb = pymysql.connect(
                host="localhost",
                user="root",
                password="123",
                database="bizcardx"
            )

            cursor = mydb.cursor()

            # Table Creation

            table_query = ("""CREATE TABLE IF NOT EXISTS bizcard_info(company_name VARCHAR(200),
                                                                    cardholder_name varchar(200),
                                                                    designation varchar(200),
                                                                    mobile_number VARCHAR(200),
                                                                    email VARCHAR(200),
                                                                    website VARCHAR(200),
                                                                    area TEXT,
                                                                    city VARCHAR(200),
                                                                    state VARCHAR(200),
                                                                    pincode VARCHAR(200))""")

            cursor.execute(table_query)
            mydb.commit()

            #Insert

            insert_query = "INSERT INTO bizcard_info(company_name,cardholder_name,designation,mobile_number,email,website,area,city,state,pincode)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            val = df.values.tolist()[0]

            cursor.execute(insert_query,val)

            mydb.commit()

            st.success("Saved Successfully")

    method = st.selectbox("Select the Method",["None","Preview"])

    if method == "Preview":

        #Select Query

        mydb = pymysql.connect(
                host="localhost",
                user="root",
                password="123",
                database="bizcardx" 
        )

        cursor = mydb.cursor()


        select_query = "SELECT * FROM bizcard_info"

        cursor.execute(select_query)
        table = cursor.fetchall()
        mydb.commit()

        table_df = pd.DataFrame(table, columns=("Company_Name", "Cardholder_Name", "Designation","Mobile_Number","Email","Website","Area","City","State","Pincode"))
        st.dataframe(table_df)




elif menu == "Modify Data":

    mydb = pymysql.connect(
                host="localhost",
                user="root",
                password="123",
                database="bizcardx"
        )

    cursor = mydb.cursor()


    select_query = "SELECT * FROM bizcard_info"

    cursor.execute(select_query)
    table = cursor.fetchall()
    mydb.commit()

    table_df = pd.DataFrame(table, columns=("Company_Name", "Cardholder_Name", "Designation","Mobile_Number","Email","Website","Area","City","State","Pincode"))

    col1, col2 = st.columns(2)

    with col1:

        selected_name = st.selectbox("Select the Name",table_df["Cardholder_Name"])
        
    df_1 = table_df[table_df["Cardholder_Name"] == selected_name]


    df_2 = df_1.copy()


    col1,col2 = st.columns(2)

    with col1:

        modify_name = st.text_input("NAME",df_2["Cardholder_Name"].unique()[0])
        modify_designation = st.text_input("DESIGNATION",df_2["Designation"].unique()[0])
        modify_company = st.text_input("COMPANY_NAME",df_2["Company_Name"].unique()[0])
        modify_contact = st.text_input("CONTACT",df_2["Mobile_Number"].unique()[0])
        modify_email = st.text_input("EMAIL",df_2["Email"].unique()[0])


        df_2["Cardholder_Name"] = modify_name
        df_2["Designation"] = modify_designation
        df_2["Company_Name"] = modify_company
        df_2["Mobile_Number"] = modify_contact
        df_2["Email"] = modify_email



    with col2:

        modify_website = st.text_input("WEBSITE",df_2["Website"].unique()[0])
        modify_area = st.text_input("AREA",df_2["Area"].unique()[0])
        modify_city = st.text_input("CITY",df_2["City"].unique()[0])
        modify_state = st.text_input("STATE",df_2["State"].unique()[0])
        modify_pincode = st.text_input("PINCODE",df_2["Pincode"].unique()[0])


        df_2["Website"] = modify_website
        df_2["Area"] = modify_area
        df_2["City"] = modify_city
        df_2["State"] = modify_state
        df_2["Pincode"] = modify_pincode


    st.dataframe(df_2)

    col1, col2 = st.columns(2)

    with col1:

        button_2 = st.button("Modify")

    if button_2:

        mydb = pymysql.connect(
                host="localhost",
                user="root",
                password="123",
                database="bizcardx"
        )

        cursor = mydb.cursor()

        cursor.execute(f"DELETE FROM bizcard_info WHERE Cardholder_Name = '{selected_name}' ")
        mydb.commit()


        insert_query = "INSERT INTO bizcard_info(company_name,cardholder_name,designation,mobile_number,email,website,area,city,state,pincode)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        val = df_2.values.tolist()[0]

        cursor.execute(insert_query,val)

        mydb.commit()

        st.success("Modifyed Successfully")

elif menu == "Delete Data":

    mydb = pymysql.connect(
                host="localhost",
                user="root",
                password="123",
                database="bizcardx"
        )

    cursor = mydb.cursor()

    col1,col2 = st.columns(2)

    with col1:

        select_query = "SELECT cardholder_name FROM bizcard_info"

        cursor.execute(select_query)
        table = cursor.fetchall()
        mydb.commit()

        names = []

        for i in table:

            names.append(i[0])

        name_select = st.selectbox("Select the Name",names)
        st.write("")
        st.write("")


    with col2:

        select_query = f"SELECT designation FROM bizcard_info WHERE cardholder_name = '{name_select}'"

        cursor.execute(select_query)
        table_1 = cursor.fetchall()
        mydb.commit()

        designation = []

        for j in table_1:

            designation.append(j[0])

        designation_select = st.selectbox("Select the Designation",designation)
        st.write("")
        st.write("")
    
    if name_select and designation_select:

        col1,col2,col3 = st.columns(3)

        with col1:

            st.write(f"Selected Name : {name_select}")
            st.write("")
            st.write("")
           
            

        with col2:

            st.write(f"Selected Designation : {designation_select}")
            st.write("")
            st.write("")
            

            remove = st.button("Delete",use_container_width=True)

            if remove:

                cursor.execute(f"DELETE FROM bizcard_info WHERE Cardholder_Name = '{name_select}' AND designation = '{designation_select}'")

                mydb.commit()

                st.warning("Deleted")
