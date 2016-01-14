import twtt



if __name__ == "__main__":
    #print(twtt.strip_urls("Hi my name www.google.ca/search/asdfasdfas/asdfasdf is @Jesse, #name, #herpes Http://www.asdf.cin/asdfa </p>"))
    print(twtt.html_char_to_ascii("Hi my name www.google.ca/search/sdfasdf is &#64;Jesse, &#35;name, &amp;herpes "))
