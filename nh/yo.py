from pdfminer.high_level import extract_text


fData = extract_text("C:/Dennis/Covid19/covid19viz/nh/data_raw/nh_covid19_20200827.pdf")
with open("C:/Dennis/Covid19/covid19viz/nh/bill827.txt", 'wb') as f:
    f.write(fData)
    f.close()