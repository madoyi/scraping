from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# timing for the entire process

start = time.time()

def parse_jobs (search_keyword, num_of_jobs, path):

    

    # initializing the chromedriver

    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(ChromeDriverManager().install())

    

    # setting the URL

    driver.get("https://www.naukri.com/")

    

    # getting the main window handle id (some of the code below is used to close the unwanted popups)

    Main_Window = driver.current_window_handle

    

    time.sleep(5)

    

    #getting all the open window handle id's to close additional popups that are appearing

    popup_windows = driver.window_handles




    #looping through all the open  windows and closing ones that are not needed

    for winId in popup_windows:

        if winId != Main_Window: 

            driver.switch_to.window(winId)

            driver.close()

    

    # switching to the main window

    driver.switch_to.window(Main_Window)

    

    time.sleep(5)

    

    #Entering the search keword and searching

    driver.find_element_by_class_name("sugInp").send_keys(search_keyword)

    driver.find_element_by_class_name("search-btn").click()

    

    # getting the current url which has a specific format which will be used later

    get_url = driver.current_url

    

    # getting the twoparts of the url by splitting with ?

    first_part = get_url.split("?")[0]

    second_part = get_url.split("?")[-1]

    

    # defining empty lists to store the parsed values

    Title =      []

    Company =    []

    Experience = []

    Salary =     []

    Location =   []

    Tags =       []

    Reviews =    []

    Ratings =    []

    Job_Type =   []

    Posted =     []




    

    # this is where parsing begins

    for i in range(1,int(num_of_jobs/20)+1):

        

        # printing the number of pages parsed

        print ("Page {} of {}".format(i,int(num_of_jobs/20)))

        

        # forming the new url with the help of two parts we defined earlier

        url = first_part+"-"+str(i)+"?"+second_part

    

        # opening the url

        driver.get(url)

        

        # giving some time so that all elements are loaded

        time.sleep(5)




        # getting job listing details

        job_list = driver.find_elements_by_class_name("jobTuple.bgWhite.br4.mb-8")




        

        # looping through all the job listings we have found in the above line of code.

        for element in job_list:

            

            # getting the Title of the Job

            try:

                title = element.find_element_by_class_name("title.fw500.ellipsis").text

                Title.append(title)

            except NoSuchElementException:

                Title.append(None)

            

            # getting the Company name

            try:

                company = element.find_element_by_class_name("subTitle.ellipsis.fleft").text

                Company.append(company)

            except NoSuchElementException:

                Company.append(None)

            

            # getting the Experience needed for the job

            try:

                experience = element.find_element_by_class_name("ellipsis.fleft.fs12.lh16").text

                Experience.append(experience)

            except NoSuchElementException:

                Experience.append(None)

            

            # getting the Salary details if any

            try:

                salary = element.find_element_by_class_name("fleft.grey-text.br2.placeHolderLi.salary").text

                Salary.append(salary)

            except NoSuchElementException:

                Salary.append(None)

            

            # getting the Location 

            try:

                location = element.find_element_by_class_name("fleft.grey-text.br2.placeHolderLi.location").text

                Location.append(location)

            except NoSuchElementException:

                Location.append(None)

            

            # getting the Tags

            try:

                tags = element.find_element_by_class_name("tags.has-description").text

                Tags.append(tags)

            except NoSuchElementException:

                Tags.append(None)

            

            # getting the number of Reviews of the company

            try: 

                review = element.find_element_by_css_selector('a.reviewsCount.ml-5.fleft.blue-text').text

                Reviews.append(review)

            except NoSuchElementException:

                Reviews.append(None)

            

            # getting the Rating of the company

            try:

                rating = element.find_element_by_css_selector("span.starRating.fleft.dot").text

                Ratings.append(rating)

            except NoSuchElementException:

                Ratings.append(None)

            

            # getting the Job Type, eg: Hotness, Preferred etc

            try: 

                job_type = element.find_element_by_css_selector('div.jobType.type.fleft.br2.mr-8').text

                Job_Type.append(job_type)

            except NoSuchElementException:

                Job_Type.append(None)

            

            # getting the number of days before which the job was posted

            try: 

                days = element.find_element_by_css_selector('div.type.br2.fleft.grey').text

                Posted.append(days)

            except NoSuchElementException:

                try:

                    days = element.find_element_by_css_selector('div.type.br2.fleft.green').text

                    Posted.append(days)

                except NoSuchElementException:

                    Posted.append(None)

    

    # initializing empty dataframe 

    df = pd.DataFrame()

    

    # assigning values to dataframe columns

    df['Title'] =      Title

    df['Company'] =    Company

    df['Experience'] = Experience

    df['Location'] =   Location

    df['Tags'] =       Tags

    df['Ratings'] =    Ratings

    df['Reviews'] =    Reviews

    df['Salary'] =     Salary

    df['Job_Type'] =   Job_Type

    df['Posted'] =     Posted

    

    # end time to complete the process

    end = time.time()

    print ("Time Taken to Parse {} jobs is:{} seconds".format(num_of_jobs,(end-start)))

    

    # quitting the driver (browser)

    driver.quit()

    

    # returning the dataframe formed

    return df




dataframe = parse_jobs("Machine Learning", 20000, "C:/Users/kulka/Desktop/Project")

dataframe.to_csv("Raw_Data.csv",index=None)