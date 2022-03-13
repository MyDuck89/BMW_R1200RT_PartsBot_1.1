import requests

from bs4  import BeautifulSoup as bs

# parse a groups
def get_group(html_text): 
    group_out = {}
    soup = bs(html_text, "lxml")
    group_mames = soup.find_all(attrs={"class": "etk-hg-link"})
    group_code = soup.find_all("a", href = True)
    
    for group, code in zip (group_mames, group_code[34:]):
        code_clear = code["href"][:-1]
        group_out[group.text.strip()] = code_clear
    return(group_out)

    
# parse subgroups
def get_subgroup(html_text):
    subgroup_out = {}
    soup = bs(html_text, "lxml")
    subgroup_names = soup.find_all(attrs={"class": "etk-node-link"})
    subgroup_code = soup.find_all("a", href = True)
    
    for subgroup, subcode in zip (subgroup_names, subgroup_code[35:]):
        subcode_clear = subcode["href"][:-1]
        subgroup_out[subgroup.text.strip()[7:]] = subcode_clear
    return(subgroup_out)

    
# parse scheme    
def get_scheme(html_text): # sheme of construction
    soup = bs(html_text, "lxml")
    scheme = soup.find("div", class_="etk-spares-wrapper")\
        .find("img")["src"]
    scheme_link = "https://cats.parts" + scheme
    return(scheme_link)
    #print(sheme_link)   
     
# parse list of parts
def get_parts(html_text):
    parts_out = {}
    soup = bs(html_text, "lxml")
    cat_numbers = soup.find_all(attrs={"class": "etk-spares-partnr"})
    part_names = soup.find_all(attrs={"class": "etk-spares-name"})
    positions = soup.find_all(attrs={"class": "etk-spares-num"})
    
    for c_number, p_name, posit in zip(cat_numbers, part_names, positions):
        if c_number.text.strip() != "Номер":
            if p_name.text.strip() != "Наименование":
                if posit.text.strip() != "№":
                    catnumber = c_number.text.strip()
                    partname = p_name.text.strip()
                    position = posit.text.strip()
                    key_string = f"Поз.{position} {partname}"
                    
                    parts_out[key_string] = catnumber
    return(parts_out)

# make a link to the exist.ru site from the parts catalog number
def get_exist_link(catnumber):
    catnumber_string = catnumber.split(" ")
    string_to_exist = "+".join(catnumber_string)
    exist_link = "https://exist.ru/Price/?pcode="\
                        + string_to_exist
    return(exist_link)

# make a link to the cats.parts site from the parts catalog number
def get_cats_link(catnumber):
    catnumber_string = catnumber.split(" ")
    string_to_catsparts = "".join(catnumber_string)
    cats_link = "https://cats.parts/$"\
                        + string_to_catsparts
    return(cats_link)

# make a link to the zzap.ru site from the parts catalog number
def get_zzap_link(catnumber):
    catnumber_string = catnumber.split(" ")
    string_to_zzap = "".join(catnumber_string)
    zzap_link = "https://www.zzap.ru/public/search.aspx#rawdata="\
                        + string_to_zzap
    return(zzap_link)
    

# aggregator of functions
def main():
    url = "https://cats.parts/moto/K26/51559/0:0:200502/11/11_3591/"
    html_text = requests.get(url).text
    catnumber = "12 72 7 674 454"
    
    #get_group(html_text)
    #get_subgroup(html_text)
    #get_scheme(html_text)
    #get_parts(html_text)
    #get_exist_link(catnumber)
    #get_cats_link(catnumber)
    get_zzap_link(catnumber)

if __name__ == "__main__":
    main()
